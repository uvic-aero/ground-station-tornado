from motor import motor_asyncio
from tornado import ioloop
import motor
import asyncio
import pprint
import time
import pymongo
from ast import literal_eval
from bson.objectid import ObjectId


class Database:
    def __init__(self):
        # Configure motor to use tornado's native asyncio loop
        self._client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017, io_loop=ioloop.IOLoop.instance().asyncio_loop)
        self._db = self._client.get_database('aero')
        self._image_collection = self._db.get_collection('images')
        self._telemetry_collection = self._db.get_collection('telemetry')
        self._image_tag_collection = self._db.get_collection('image_tags')
        self._log_collection = self._db.get_collection('logs')
        self._marker_collection = self._db.get_collection('markers')

        return None
        
    @property 
    def image_collection(self):
        return self._image_collection

    @property
    def telemetry_collection(self):
        return self._telemetry_collection


    # Prepare for returning as json; convert objectid
    def _transform_json(self, document):
        return {**document, **{'_id': str(document['_id'])}}

    # write new image to image collection: params(image object)
    async def insert_image(self, document):
        document['telemetry'] = str(document['telemetry'])
        result = await self._image_collection.insert_one(document)
        return result.inserted_id

    async def update_image(self, image_id, document):
        await self._image_collection.update_one({'_id': ObjectId(image_id)}, document)

    async def insert_telemetry(self, document):
        result = await self._telemetry_collection.insert_one(document)

    # returns all "image_objects" in the image collection
    async def do_find_images(self, callback):
        cursor = self._image_collection.find({})
        temp = []
        for document in await cursor.to_list(length=None):
            temp.append({**document, **{'_id': str(document['_id'])}})
        callback(temp)


    async def find_image_by_id(self, id, callback):
        result = await self._image_collection.find_one({"_id": ObjectId(id)})
        callback(result)

    # If image_id is a valid image id, then return the next 'count' images that have a timestamp
    # less than the image referenced by image_id
    # The purpose is for pagination. Assuming sorted by timestamp greatest to least,
    # if we load the newest 20 images, then this function would allow us to load the next 20 images
    # that come after the last image in the previous set. Newer images have a larger timestamp
    # This requires sorting by timestamp, searching for images with lesser timestamp than image_id, and limiting
    # the return to 'count' number of results
    # New: Now pulls related telemetry document
    async def get_next_images(self, _id = None, count = 15):
        if(_id == None):
            cursor = await self._image_collection.find_one({}, sort=[('timestamp', pymongo.DESCENDING)])
        else: 
            cursor = await self._image_collection.find_one({"_id": ObjectId(_id)})

        # check for cursor existince
        if cursor == None:
            return []
    
        result = await self._image_collection.find({'timestamp': {'$not': {'$gt': cursor['timestamp']}}}, sort=[('timestamp', pymongo.DESCENDING)], limit=count).to_list(length=None)

        telemetry_ids = [x['telemetry_id'] for x in result]
        image_ids = [str(x['_id']) for x in result]

        tel_result = await self._telemetry_collection.find({'_id': {'$in': telemetry_ids}}).to_list(length=None)
        tag_result = await self._image_tag_collection.find({'image_id': {'$in': image_ids}}).to_list(length=None)

        for res in result:
            res['telemetry'] = next((x for x in tel_result if x['_id'] == res['telemetry_id']), None)
            # TODO: currently, image_tag is stored as a string instead of ObjectId, replace to ObjectId eventually
            res['tagged'] = next((True for x in tag_result if x['image_id'] == str(res['_id'])), False)

        return result

    #Pass to sets of coordinate to retreive an group of images
    async def find_by_coordinates(self, coordinate_a = None, coordinate_b = None, callback = None):
        #coord_a is bottom left | coord_b is upper right
        if(coordinate_a == None or coordinate_b == None):
            return('Coordinate parameter is missing')
        cursor = self._image_collection.find({ 'location': { '$geoWithin':{ '$box': [ coordinate_a, coordinate_b ] } } })
        temp = []
        for document in await cursor.to_list(length=None):
            temp.append({**document, **{'_id': str(document['_id'])}})
        callback({'result': temp})

    # returns all telemetry objects in telemetry collection
    async def do_find_telemetry(self, callback):
        cursor = self._telemetry_collection.find({})
        temp = []
        for document in await cursor.to_list(length=None):
            temp.append({**document, **{'_id': str(document['_id'])}})
        callback(temp)

    async def get_nearest_telemetry(self, timestamp):

        cursor = self._telemetry_collection.aggregate([
            {'$project': {'diff': {'$abs': {'$subtract': [timestamp, '$timestamp']}}, 'timestamp': '$timestamp', 'lat': '$lat', 'lon': '$lon','alt': '$alt' }},
            {'$sort': {'diff': 1}},
            {'$limit': 1}
        ])
        await cursor.fetch_next
        return cursor.next_object()

    async def get_latest_telemetry_callback(self, callback):
        doc = await self._telemetry_collection.find_one({ "$query":{}, "$orderby":{ "_id": -1 }})
        callback(self._transform_json(doc))

    async def get_latest_telemetry(self):
        return await self._telemetry_collection.find_one({ "$query":{}, "$orderby":{ "_id": -1 }})

    # write new image tag to image_tag collection: params(uuid)
    async def insert_image_tag(self, tag_id):
        exists = await self._image_tag_collection.find_one({'image_id': tag_id})
        if exists is not None:
            return
        result = await self._image_tag_collection.insert({'image_id': tag_id})

    # remove specified image tag from image_tag collection: params(uuid)
    async def remove_image_tag(self, tag_id):
        result = await self._image_tag_collection.remove({'image_id': tag_id})

    # return a list of all image_tag objects from image_tag collection
    async def find_all_image_tags(self):
        cursor = self._image_tag_collection.find({})
        temp = []
        for document in await cursor.to_list(length=None):
            temp.append({**document, **{'_id': str(document['_id'])}})
        return temp
    
    async def insert_log(self, document):
        msg = document["message"]
        sys = document['system']
        ts = document['timestamp']
        result = await self._log_collection.insert({'timestamp': ts, 'message': msg, 'system': sys})

    #Mapping and Markers
    async def find_all_markers(self, callback = None):
        #Markers must hold some information(img path, telemetry, uid)
        #similar to do_find_telemetry() function
        cursor = self._image_collection.find({})
        temp = []
        for document in await cursor.to_list(length=None):
            #temp_telemetry = await self._telemetry_collection.find_one({'_id': ObjectId(document['telemetry_id'])})
            telemetry = literal_eval(document['telemetry'])
            
            telemetry['alt'] = 0

            temp.append(
                {
                    'position':{
                        'lat': telemetry['lat'],
                        'lng': telemetry['lon'],
                        'alt': telemetry['alt'],
                    },
                    'image_path': document['file_location'],
                }
            )
        callback(temp)


    #This function is designed to organize then return geoJson objects 
    #by combining thumbnails, markers (points) and images
    #Documentation on mongodb geoJson objects can be found here 
    # https://docs.mongodb.com/manual/reference/geojson/

    async def find_geoJson(self, callback = None):
        #Markers must hold some information(img path, telemetry, uid)
        #similar to do_find_telemetry() function
        cursor = self._telemetry_collection.find({})
        temp = []
        for document in await cursor.to_list(length=None):
            temp.append(
               {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                        document['lat'], document['lon']
                        ]
                    },
                    "properties": {
                        "thumbnail_path": "not implemented yet"
                    }
                }
            )
        
        callback(temp)

database = Database()

