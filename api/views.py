import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from api.public import upload_file_to_server, query_sparql, get_objects
from asgiref.sync import sync_to_async

def index(request):

    return render(request, "index.html")

@csrf_exempt
def upload(request):
    if request.method == 'POST' and request.FILES.get('file'):
        path = request.POST['path']
        file = request.FILES['file']
        status = upload_file_to_server(path, file)

    return HttpResponse(status)

@csrf_exempt
def sparqlQuery(request):
    query = json.loads(request.body.decode()).get('sparql')
    result = query_sparql(query)
    return HttpResponse(result)

