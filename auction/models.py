from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Car(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    starting_bid = models.DecimalField(max_digits=5, decimal_places=2)
    end_auction = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='buyer')
    is_auction_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name = 'bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car} - {self.user} - {self.amount}"
    