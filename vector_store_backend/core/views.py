import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

FASTAPI_URL = "http://localhost:8001"

@csrf_exempt
def search_vectors(request):
    if request.method == "POST":
        data = json.loads(request.body)
        response = requests.post(f"{FASTAPI_URL}/search", json=data)
        return JsonResponse(response.json())

@csrf_exempt
def insert_vectors(request):
    if request.method == "POST":
        data = json.loads(request.body)
        response = requests.post(f"{FASTAPI_URL}/insert", json=data)
        return JsonResponse(response.json())
