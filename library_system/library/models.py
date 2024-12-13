from django.db import models
from django.utils.timezone import now

# This represents a library subscription plan with borrowing limits
class SubscriptionPlan(models.Model):
   
  
    name = models.CharField(max_length=50)
    book_limit = models.IntegerField()
    magazine_limit = models.IntegerField()
    
    def __str__(self):
        return self.name


# This represents a library user with their borrowing status and limits
class User(models.Model):
    
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    borrowed_books = models.IntegerField(default=0)
    borrowed_magazines = models.IntegerField(default=0)
    monthly_transactions = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

# This represents a library book or magazine that can be borrowed
class Item(models.Model):
    
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

# This represents  records of  all borrowing and returning transactions in the library
class Transaction(models.Model):

  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=[("borrow", "Borrow"), ("return", "Return")])
    timestamp = models.DateTimeField(default=now)    
    
    def __str__(self):
        return f"{self.user}- {self.item}"