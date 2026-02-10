from django.http import HttpResponse

def index(request):
    return HttpResponse("Rango says hello world!")

def about(request):
    return HttpResponse("Rango says here is the about page.")
