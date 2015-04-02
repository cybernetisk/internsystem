from django.shortcuts import render

def angular_frontend(request):
    # prepare data from SAML
    attributes = None
    if 'samlUserdata' in request.session and len(request.session['samlUserdata']) > 0:
        attributes = request.session['samlUserdata']

    return render(request, 'frontend.html', {'saml_attributes': attributes})
