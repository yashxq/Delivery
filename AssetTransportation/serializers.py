from rest_framework import serializers
from AssetTransportation.models import RequestDetails

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestDetails
        fields = ('RequestId','AddressFrom','AddressTo','ClientID','ReceiverID','ExecutiveID','Status','AssetSensitivity','AssetType')