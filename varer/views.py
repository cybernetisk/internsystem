from django.shortcuts import render_to_response

def angular_frontend(request):
    return render_to_response('frontend.html')
