from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.middleware.csrf import get_token

@api_view()
def me(request):
    if request.user.is_authenticated():
        # prepare data from SAML
        metadata = None
        if 'samlUserdata' in request.session and len(request.session['samlUserdata']) > 0:
            metadata = request.session['samlUserdata']

        return Response({
            'loggedIn': True,
            'details': {
                'username': request.user.username,
                'realname': request.user.realname,
                'email': request.user.email
            },
            'metadata': metadata,
            'csrfToken': get_token(request)
        })
    else:
        return Response({
            'loggedIn': False,
            'csrfToken': get_token(request)
        })
