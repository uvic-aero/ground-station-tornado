class Subscriptions:

    def __init__(self):
        # List of valid subscription types
        self._subscription_types = ['images', 'telemetry']

        # A map of subscription type to a list of subscribers
        self._subscriptions = {_type: [] for _type in self._subscription_types}

    def subscribe(self, client, subscription_type: str):
        if subscription_type not in self._subscription_types:
            return

        new_identity = client.get_identity()

        for subscriber in self._subscriptions[subscription_type]:
            if subscriber.get_identity == new_identity:
                return

        self._subscriptions[subscription_type].append(client)

    def unsubscribe(self, client, subscription_type: str=None):

        identity = client.get_identity()

        # If no type is specified, the client is removed from all active subscriptions
        if subscription_type is None:
            for _type in self._subscriptions:
                subscriber = next((sub for sub in self._subscriptions[_type] if sub.get_identity() == identity), None)

                if subscriber is not None:
                    self._subscriptions[_type].remove(subscriber)
        elif subscription_type in self._subscription_types:
            subscriber = next((sub for sub in self._subscriptions[subscription_type]
                               if sub.get_identity() == identity), None)

            if subscriber is not None:
                self._subscriptions[subscription_type].remove(subscriber)

    def get_subscribers(self, subscription_type: str=None) -> list:

        # If a specific type is not specified, returns all subscribers
        if subscription_type is None:

            # Pull the subscribers across all types
            subscribers = [(sub for sub in self._subscriptions[_type]) for _type in self._subscription_types]

            # The set conversion will remove duplicate subs
            return list(set(subscribers))

        elif subscription_type in self._subscription_types:
            return self._subscriptions[subscription_type]

        return []

subscriptions = Subscriptions()


class Publisher:

    def __init__(self):
        pass

    def publish(self, subscription: str, data: object):
        pass

    def publish_all(self, data: object):
        pass

publisher = Publisher()
