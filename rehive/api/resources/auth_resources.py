from .base_resources import ResourceList, Resource, ResourceCollection


class AuthResources(Resource, ResourceCollection):

    def __init__(self, client):
        self.client = client
        self.endpoint = ''
        self.resources = (
            APIAuthPassword,
            APIAuthEmail,
            APIAuthMobile,
            APIAuthTokens,
            APIAuthMFA
        )
        super(AuthResources, self).__init__(client, self.endpoint)
        self.create_resources(self.resources)

    def login(self, user, company, password):
        data = {
            "user": user,
            "company": company,
            "password": password,
        }
        response = self.post(data, 'login')
        return response

    def register(self,
                 first_name,
                 last_name,
                 email,
                 company,
                 password1,
                 password2,
                 **kwargs):
        data = {
           "first_name": first_name,
           "last_name": last_name,
           "email": email,
           "company": company,
           "password1": password1,
           "password2": password2
        }
        response = self.post(data, 'register', **kwargs)
        return response

    def register_company(self,
                         first_name,
                         last_name,
                         email,
                         company,
                         password1,
                         password2,
                         terms_and_conditions,
                         **kwargs):
            data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "company": company,
                "password1": password1,
                "password2": password2,
                "terms_and_conditions": terms_and_conditions
            }
            response = self.post(data, 'company/register/', **kwargs)
            return response

    def logout(self):
        self.client.token = None
        return self.post({}, 'logout')

    def logout_all(self):
        self.client.token = None
        return self.post({}, 'logout/all')

    @classmethod
    def get_resource_name(cls):
        return 'auth'


class APIAuthPassword(Resource):

    def reset_password(self, user, company):
        data = {
            "user": user,
            "company": company
        }
        return self.post(data, 'reset')

    def reset_password_confirm(self, new_password1, new_password2, uid, token):
        data = {
            "new_password1": new_password1,
            "new_password2": new_password2,
            "uid": uid,
            "token": token
        }
        return self.post(data, 'reset/confirm')

    def change(self, old_password, new_password1, new_password2):
        data = {
            "old_password": old_password,
            "new_password1": new_password1,
            "new_password2": new_password2
        }
        return self.post(data, 'change')

    @classmethod
    def get_resource_name(cls):
        return 'password'


class APIAuthEmail(Resource):

    def resend_email_verification(self, email, company):
        data = {
            "email": email,
            "company": company
        }
        return self.post(data, 'verify/resend')

    def verify(self, key):
        data = {
            "key": key
        }
        return self.post(data, 'verify')

    @classmethod
    def get_resource_name(cls):
        return 'email'


class APIAuthMobile(Resource):

    def resend_mobile_verification(self, mobile, company):
        data = {
            "mobile": mobile,
            "company": company
        }
        return self.post(data, 'verify/resend')

    def verify(self, otp):
        data = {
            "otp": otp
        }
        return self.post(data, 'verify')

    @classmethod
    def get_resource_name(cls):
        return 'mobile'


class APIAuthTokens(Resource):

    def create(self, password):
        data = {"password": password}
        return self.post(data)

    def delete(self, token_key):
        return super().delete(token_key)

    def verify(self, token):
        data = {
            "token": token
        }
        return self.post(data, 'verify')

    @classmethod
    def get_resource_name(cls):
        return 'tokens'


class APIAuthMFA(Resource):

    def authorize_number(self, mobile):
        data = {
            "mobile_number": mobile
        }
        return self.post(data, 'sms')

    def send_sms(self, mobile):
        data = {
            "mobile_number": mobile
        }
        return self.post(data, 'sms/send')

    def authorize_token(self, **kwargs):
        return self.post({}, 'token', **kwargs)

    def verify(self, token):
        data = {
            "token": token
        }
        return self.post(data, 'verify')

    @classmethod
    def get_resource_name(cls):
        return 'mfa'
