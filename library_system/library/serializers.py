from rest_framework import serializers

class OrderSerializer(serializers.Serializer):
    """
    Serializer for handling item borrowing requests.

    Fields:
        title (str): The title of the item to be borrowed

    Example:
        {
            "title": "The Great Gatsby"
        }

    Note:
        - Used in the order endpoint of LibraryViewSet
        - Validates the presence and format of the title field
    """
    title = serializers.CharField()

class ReturnSerializer(serializers.Serializer):
    """
    Serializer for handling item return requests.

    Fields:
        titles (list): List of titles to be returned

    Example:
        {
            "titles": ["The Great Gatsby", "Time Magazine"]
        }

    Note:
        - Used in the return endpoint of LibraryViewSet
        - Accepts multiple titles for batch returns
        - Each title must be a valid string
    """
    titles = serializers.ListField(child=serializers.CharField())

    
    