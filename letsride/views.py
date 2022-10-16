from urllib.request import Request
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from letsride.controllers import generic_controller

@csrf_exempt
def riderInfo(request, id=0):
    if request.method=='GET':
        return generic_controller.first_function(id)
    elif request.method=='POST':
        all_asset_data = JSONParser().parse(request)
        print(all_asset_data)
        return JsonResponse(all_asset_data, safe=False)

@csrf_exempt
def createOrder(request):
    if request.method == 'POST':
        order_details = JSONParser().parse(request)
        if order_details['requester_id']==None or order_details['requester_id']==0:
            return JsonResponse("Please help register your account", safe = False)
        if order_details['origin_address']!=None and order_details['delivery_address']!=None and order_details['no_of_items']!=None:
            #print(order_details['asset_type'],len(order_details['asset_type']))
            if str(order_details['asset_type']) not in ["LAPTOP", "TRAVEL_BAG", "PACKAGE"]:
                return JsonResponse("Please select correct asset Type", safe = False)
            if order_details['asset_senstivity'] not in ["HIGHLY_SENSITIVE", "SENSITIVE", "NORMAL"]:
                return JsonResponse("Please select correct asset senstivity", safe = False)
            #Login to valididate receiver details by regex
            return generic_controller.creater_order(order_details)
        return JsonResponse("Failed to accept order", safe=False)

@csrf_exempt
def createRiderTravel(request):
    if request.method == 'POST':
        order_details = JSONParser().parse(request)
        if order_details['customer_id']==None or order_details['customer_id']==0:
            return JsonResponse("Please help register your account", safe = False)
        if order_details['source_address']!=None and order_details['destination_address']!=None and order_details['no_of_items']!=None and order_details['no_of_items']!=0:
            if str(order_details['travel_medium']) not in ["BUS", "CAR", "TRAIN"]:
                return JsonResponse("Please select correct travel medium", safe = False)
            
            return generic_controller.creater_travel_details(order_details)
        return JsonResponse("Failed to accept order", safe=False)

