#from django.db import connection
from django.http import HttpResponse

#cursor = connection.cursor()

def index(request):
    return HttpResponse("hello word")
