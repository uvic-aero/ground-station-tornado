import uuid 
import asyncio
from .database import database

#DOCUMENT: gets all image_tags from data base on initialization and
#or when the get all image tags is called
#add_image_tag(uuid) sends image tag to db
#remove_image_tag(uuid) takes the uuid and removes all images with 
#that id from the db.


class ImageTag:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.image_tag_collection = self.loop.run_until_complete(database.find_all_image_tags())

    async def add_image_tag(self, image_id):
        result = await database.insert_image_tag(image_id)
    
    async def remove_image_tag(self, image_id):
        result = await database.remove_image_tag(image_id)
    
    async def get_image_tags(self):
        temp = await database.find_all_image_tags()
        print(temp)

<<<<<<< HEAD

=======
>>>>>>> crazy-imageTag-experiment
image_tag = ImageTag()