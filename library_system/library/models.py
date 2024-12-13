from django.db import models
from django.utils.timezone import now

class SubscriptionPlan(models.Model):
    """
    Represents a library subscription plan with borrowing limits.

    Attributes:
        name (str): Name of the subscription plan
        book_limit (int): Maximum number of books that can be borrowed simultaneously
        magazine_limit (int): Maximum number of magazines that can be borrowed simultaneously
    """
    name = models.CharField(max_length=50)
    book_limit = models.IntegerField()
    magazine_limit = models.IntegerField()
    
    def __str__(self):
        return self.name

class User(models.Model):
    """
    Represents a library user with their borrowing status and limits.

    Attributes:
        name (str): User's full name
        age (int): User's age, used for content restrictions
        subscription_plan (SubscriptionPlan): Foreign key to user's subscription plan
        borrowed_books (int): Current number of books borrowed by the user
        borrowed_magazines (int): Current number of magazines borrowed by the user
        monthly_transactions (int): Count of transactions made in the current month

    Note:
        - borrowed_books and borrowed_magazines are constrained by subscription_plan limits
        - monthly_transactions has a system-wide limit of 10 per month
    """
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    borrowed_books = models.IntegerField(default=0)
    borrowed_magazines = models.IntegerField(default=0)
    monthly_transactions = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class Item(models.Model):
    """
    Represents a library item (book or magazine) that can be borrowed.

    Attributes:
        title (str): Title of the item, must be unique
        genre (str): Genre/category of the item
        item_type (str): Type of item - either 'book' or 'magazine'
        is_available (bool): Current availability status of the item

    Note:
        - Some genres may have age restrictions (e.g., Crime genre for 18+)
        - item_type choices are limited to 'book' or 'magazine'
    """
    ITEM_TYPE_CHOICES = [
        ("book", "Book"),
        ("magazine", "Magazine"),
    ]
    title = models.CharField(max_length=200, unique=True)
    genre = models.CharField(max_length=50)
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    is_available = models.BooleanField(default=True)    
    
    def __str__(self):
        return self.title

class Transaction(models.Model):
    """
    Records all borrowing and returning transactions in the library.

    Attributes:
        user (User): Foreign key to the user making the transaction
        item (Item): Foreign key to the item being borrowed/returned
        action (str): Type of transaction - either 'borrow' or 'return'
        timestamp (datetime): When the transaction occurred

    Note:
        - Transactions are used to track borrowing history
        - Transactions help maintain monthly transaction limits
        - Automatic timestamp is added when transaction is created
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=[("borrow", "Borrow"), ("return", "Return")])
    timestamp = models.DateTimeField(default=now)    
    
    def __str__(self):
        return f"{self.user}- {self.item}"