from django.http import HttpResponse

def home(request):
    # Create a json response welcome message
    return HttpResponse('Welcome to the firma API')