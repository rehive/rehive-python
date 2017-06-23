from .base_resources import ResourceList, Resource, ResourceCollection


class UserResources(Resource, ResourceCollection):

    def __init__(self, client):
        self.client = client
        self.endpoint = ''
        self.resources = (
            APIUserAddress,
            APIUserEmail,
            APIUserMobiles,
            APIUserNotifications
        )
        super(UserResources, self).__init__(client, self.endpoint)
        self.create_resources(self.resources)

    @classmethod
    def get_resource_name(cls):
        return 'user'


class APIUserAddress(Resource):

    @classmethod
    def get_resource_name(cls):
        return 'address'


class APIUserEmail(Resource):

    def create(self, email):
        return super().create(email=email)

    def make_primary(self, email):
        return self.patch(email, primary=True)

    @classmethod
    def get_resource_name(cls):
        return 'emails'


class APIUserMobiles(Resource):

    def create(self, number):
        return super().create(email=email)

    def make_primary(self, number):
        return self.patch(number, primary=True)

    @classmethod
    def get_resource_name(cls):
        return 'mobiles'


class APIUserNotifications(Resource):

    def enable_sms(self, id):
        return self.update(id, sms_enabled=True)

    def disable_sms(self, id):
        return self.update(id, sms_enabled=False)

    def enable_email(self, id):
        return self.update(id, email_enabled=True)

    def disable_email(self, id):
        return self.update(id, email_enabled=False)

    @classmethod
    def get_resource_name(cls):
        return 'notifications'
