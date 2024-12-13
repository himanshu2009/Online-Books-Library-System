from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import OrderSerializer, ReturnSerializer
from .models import Item,User,Transaction,SubscriptionPlan
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class LibraryViewSet(viewsets.ViewSet):
    """
    ViewSet for handling library operations including borrowing and returning items.
    
    This viewset provides endpoints for:
    - Ordering (borrowing) library items
    - Returning library items
    
    All operations require user authentication.
    """

    @action(detail=False, methods=['post'], url_path='order')
    def order(self, request):
        """
        Handles the borrowing of library items.

        Parameters:
            request (Request): HTTP request object containing:
                - title (str): The title of the item to borrow

        Returns:
            Response: JSON response with success/error message
                200: Item borrowed successfully
                400: Monthly limit reached or borrowing limit exceeded
                401: Authentication required
                403: Age restriction violation
                404: Item not found or not available

        Enforces:
            - User authentication
            - Monthly transaction limits (10 per month)
            - Item-specific borrowing limits based on subscription plan
            - Age restrictions for certain genres
        """
        auth_user = request.user
        try:
            user = User.objects.get(name=auth_user.username)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        if not auth_user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.validated_data['title']
        #user = request.user

        # Check transaction limit
        if user.monthly_transactions >= 10:
            return Response({"error": "Monthly transaction limit reached."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            item = Item.objects.get(title=title, is_available=True)
        except Item.DoesNotExist:
            return Response({"error": "Item not available."}, status=status.HTTP_404_NOT_FOUND)
        
        # Check borrowing limits and eligibility
        if item.item_type == "book":
            if user.borrowed_books >= user.subscription_plan.book_limit:
                return Response({"error": "Book borrowing limit exceeded."}, status=status.HTTP_400_BAD_REQUEST)
            if item.genre == "Crime" and user.age < 18:
                return Response({"error": "Crime books are restricted to users 18+."}, status=status.HTTP_403_FORBIDDEN)
            user.borrowed_books += 1

        elif item.item_type == "magazine":
            if user.borrowed_magazines >= user.subscription_plan.magazine_limit:
                return Response({"error": "Magazine borrowing limit exceeded."}, status=status.HTTP_400_BAD_REQUEST)
            user.borrowed_magazines += 1
        # Update records
        item.is_available = False
        user.monthly_transactions += 1
        item.save()
        user.save()
        Transaction.objects.create(user=user, item=item, action="borrow")

        return Response({"message": "Item borrowed successfully."}, status=status.HTTP_200_OK)    
    
    @action(detail=False, methods=['post'], url_path='return')
    def return_items(self, request):
        """
        Handles the return of borrowed library items.

        Parameters:
            request (Request): HTTP request object containing:
                - titles (list): List of titles to return

        Returns:
            Response: JSON response with success/error message
                200: Items returned successfully
                401: Authentication required
                404: User not found or item not found/not borrowed

        Notes:
            - Updates item availability status
            - Updates user's borrowed items count
            - Creates transaction records for returns
        """
        auth_user = request.user
        try:
            user = User.objects.get(name=auth_user.username)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if not auth_user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ReturnSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        titles = serializer.validated_data['titles']
        #user = request.user

        for title in titles:
            try:
                item = Item.objects.get(title=title, is_available=False)
            except Item.DoesNotExist:
                return Response({"error": f"Item '{title}' not found or not borrowed."}, status=status.HTTP_404_NOT_FOUND)

            # Update records
            if item.item_type == "book":
                user.borrowed_books -= 1
            elif item.item_type == "magazine":
                user.borrowed_magazines -= 1

            item.is_available = True
            item.save()
            Transaction.objects.create(user=user, item=item, action="return")

        user.save()
        return Response({"message": "Items returned successfully."}, status=status.HTTP_200_OK)