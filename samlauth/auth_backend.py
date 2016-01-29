from core.models import User

class SAMLServiceProviderBackend(object):

    def authenticate(self, saml_authentication=None):
        if not saml_authentication:  # Using another authentication method
            return None

        if saml_authentication.is_authenticated():
            attributes = saml_authentication.get_attributes()
            user_changed = False
            try:
                user = User.objects.get(username=saml_authentication.get_attributes()['uid'][0])
            except User.DoesNotExist:
                user = User(username=saml_authentication.get_attributes()['uid'][0])
                user.set_unusable_password()
                user.username = attributes['uid'][0]

            map_fields = {
                'realname': 'cn',
                'email': 'mail'
            }

            # ensure realname for users from webid don't contain unverified note
            if 'cn' in attributes:
                attributes['cn'][0] = attributes['cn'][0].replace(' (unverified)', '')

            for field, samlfield in map_fields.items():
                if getattr(user, field) != attributes[samlfield][0]:
                    setattr(user, field, attributes[samlfield][0])
                    user_changed = True

            if user_changed:
                user.save()

            return user
        return None


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None