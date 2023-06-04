from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from api.public import upload_file_to_server, query_sparql
import json
import os

def index(request):

    return render(request, "index.html")

@csrf_exempt
def upload(request):
    status = 'No file uploaded'

    if request.method == 'POST' and request.FILES.get('file'):
        path = request.POST['path']
        file = request.FILES['file']

        try:
            save_directory = os.path.join("/home/knownow/KnowNow/", path)
            file_path = os.path.join(save_directory, file.name)
            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            status = "file uploaded success"
        except:
            status = "file uploaded faild"

    return HttpResponse(status)

@csrf_exempt
def sparqlQuery(request):
    query = json.loads(request.body.decode()).get('sparql')
    print(query)
    result = query_sparql(query)
    print(result)
    return HttpResponse(result)