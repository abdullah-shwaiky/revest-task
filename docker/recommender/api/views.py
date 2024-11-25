from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from . import models
from .serializers import ProductsSerializer
from rest_framework.response import Response
from rest_framework import status
import numpy as np
from pymongo import MongoClient
from datetime import datetime
import uuid
import redis
import json
# Create your views here.

# MongoDB Connection
client = MongoClient("mongodb://mongodb:27017/")
db = client["api_logs"]
logs_collection = db["logs"]
redis_conn = redis.Redis(host='redis', port=6379,db=0, decode_responses=True)


def log_request(input_data, output_data):
    request_id = str(uuid.uuid4())
    log_entry = {
        "timestamp": datetime.now(),
        "request_id": request_id,
        "input": input_data,
        "output": output_data
    }
    logs_collection.insert_one(log_entry)
    print(f"Log saved with request_id {request_id}")




class RecommenderView(APIView):
    def post(self, request):
        input_id = request.data.get('id')
        try:
            items = models.Products.objects.get(product_id=input_id)
            serializer = ProductsSerializer(items)
            items = models.Products.objects.all()
            results = ProductsSerializer(items, many = True).data
            indices = np.random.random_integers(0,len(results),5)
            items = redis_conn.get(input_id)
            if not items:
                items = {f'{i}':results[index] for i, index in enumerate(indices)}
                redis_conn.set(input_id, json.dumps(items, indent=4))
            else:
                items = json.loads(items)
            return Response(items.values())
        except:
            product_ids = ['FUR-BO-10001798', 'OFF-AR-10002833', 'TEC-PH-10001949']
            items = {}
            for i, id in enumerate(product_ids):
                items = {**items, f'{i}':ProductsSerializer(models.Products.objects.get(product_id = id)).data}
            return Response(items.values())
        finally:
            log_request(request.data, items)