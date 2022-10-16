from urllib.request import Request
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse


from AssetTransportation.models import RequestDetails
from AssetTransportation.serializers import AssetSerializer

# Create your views here.

@csrf_exempt
def assetRequest(request, id=0):
    if request.method=='GET':
        allassets = RequestDetails.objects.all()
        allassets_serilizer = AssetSerializer(allassets, many=True)
        return JsonResponse(allassets_serilizer.data, safe=False)
    elif request.method=='POST':
        all_asset_data = JSONParser.parse(request)
        all_asset_serilizer = AssetSerializer(data = all_asset_data)
        if all_asset_serilizer.is_valid():
            all_asset_serilizer.save()
            return JsonResponse("Added Succesfully",safe=False)
        return JsonResponse("Failed to Add", safe = False)
    elif request.method=='PUT':
        all_asset_data = JSONParser.parse(request)
        all_asset = RequestDetails.object.get(RequestId = all_asset_data['RequestId'])
        allassets_serilizer = AssetSerializer(all_asset, data=all_asset_data)
        if allassets_serilizer.is_valid():
            allassets_serilizer.save()
            return JsonResponse("Update Succesfully",safe=False)
        return JsonResponse("Failed to Update", safe = False)
    elif request.method == 'DELETE':
        asset_data = RequestDetails.object.get(RequestId=id)
        asset_data.delete()
        return JsonResponse("Delete Successfull",safe=False)
