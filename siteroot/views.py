from django.shortcuts import render

def angular_frontend(request):
    return render(request, 'frontend.html')
