from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class Auction_list(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    auction_list = models.CharField(max_length=64, default='')
    starting_bid = models.IntegerField(default=0)
    description = models.CharField(max_length=64, default='')
    category = models.CharField(max_length=64, default='')
    list_name = models.CharField(max_length=64, default='')
    url = models.CharField(null=True, blank=True, max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True,null=True, blank=True)
class Bids(models.Model):

    list_id = models.ForeignKey(Auction_list, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null=True)
    your_bids = models.FloatField(default=0)
class Comments(models.Model):
    comment_list_id = models.ForeignKey(Auction_list, on_delete=models.CASCADE, related_name="comment_list_id", null=True, blank=True)
    comments = models.CharField(max_length=64, default='')
    timestamp = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    comment_user_id =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user_id", null=True, blank=True)

class Watchlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank =True, null =True)
    auction_list_id = models.ForeignKey(Auction_list, on_delete=models.CASCADE)
    

class Closed_listing(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE, related_name="user_id", null=True, blank=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='winner_id', null=True, blank=True)
    auction_list = models.CharField(max_length=64, default='')
    starting_bid = models.IntegerField(default=0)
    description = models.CharField(max_length=64, default='')
    category = models.CharField(max_length=64, default='')
    list_name = models.CharField(max_length=64, default='')
    url = models.CharField(null=True, blank=True, max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    bids = models.FloatField(default=0)

