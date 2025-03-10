import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

FASTAPI_URL = "http://localhost:8001"

@csrf_exempt
def get_details(request):
    if request.method == "POST":
        data = json.loads(request.body)
        response = requests.get(f"{FASTAPI_URL}/details", json=data)
        return JsonResponse(response.json())

@csrf_exempt
def get_resources(request):
    if request.method == "GET":
        response = requests.get(f"{FASTAPI_URL}/resources")
        return JsonResponse(response.json())

@csrf_exempt
def create_collection(request):
    if request.method == "POST":
        data = json.loads(request.body)
        response = requests.post(f"{FASTAPI_URL}/collection", json=data)
        return JsonResponse(response.json())

@csrf_exempt
def delete_collection(request):
    if request.method == "POST":
        data = json.loads(request.body)
        response = requests.delete(f"{FASTAPI_URL}/collection", json=data)
        return JsonResponse(response.json())

@csrf_exempt
def search_vectors(request):
    if request.method == "POST":
        data = json.loads(request.body)
        response = requests.post(f"{FASTAPI_URL}/search", json=data)
        return JsonResponse(response.json())

@csrf_exempt
def insert_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        response = requests.post(f"{FASTAPI_URL}/data", json=data)
        return JsonResponse(response.json())

@csrf_exempt
def delete_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        response = requests.delete(f"{FASTAPI_URL}/data", json=data)
        return JsonResponse(response.json())
