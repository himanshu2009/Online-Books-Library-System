from rest_framework import serializers

  # This serializer for handling item borrowing requests
class OrderSerializer(serializers.Serializer):
  
    title = serializers.CharField()

# This serializer for handling item return requests
class ReturnSerializer(serializers.Serializer):
    
    titles = serializers.ListField(child=serializers.CharField())

    
    