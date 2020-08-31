import urllib
import urllib.request as urllib2
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Auction_list, Comments, Bids, Watchlist, Closed_listing
import requests
from django.db.models import Max
from django.contrib import messages
from django import template





# Credit for the Net Nijia Youtuber
def dl_jpg(url, file_path, file_name):
    full_path = file_path + file_name + '.jpg'
    urllib.request.urlretrieve(url, full_path)

def findLenOfWat(user_id):
    lenOfwat = 0

    # Try and see if there is element inside of watchlist model
    try:
        watchlist = Watchlist.objects.filter(user_id = user_id)
        lenOfwat = watchlist.count()
    except Exception as error:
        pass
    return lenOfwat

def index(request):
    if request.method == "GET":
        auction = Auction_list.objects.all()
        return render(request, "auctions/index.html",{
            "datas": auction,
            "lenOfWat": findLenOfWat(request.user)
        })
    else:
        post_data = request.POST
        auction_list = Auction_list.objects.filter(list_name__startswith = str(post_data["object_id"]))
        winner = User.objects.get(username = post_data["winner"])
        for l in auction_list:
            closed_listing = Closed_listing(user_id = request.user, winner = winner,
            auction_list = l.auction_list, description= l.description, category = l.category, list_name = l.list_name,
            url = l.url, starting_bid = l.starting_bid, bids= post_data["bid"])
            closed_listing.save()
            l.delete()
        return render(request, "auctions/closed.html",{
            "datas": Closed_listing.objects.all(),
            "lenOfWat": findLenOfWat(request.user)
        })
        






def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        auction = Auction_list.objects.all()
        render(request, "auctions/index.html", {
            "data": auction
        })
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create(request):
    if request.method =="POST":
        url = str(request.POST["image_url"])
        t = True
        try:
            if requests.get(url).status_code != requests.codes.ok: #pylint: disable=no-member
                #  Error handling here
                t = False
                exit(1)
        except Exception as error:
            t = False
            pass
        l = Auction_list.objects.all()
        #might be possible model has no records so make sure to handle None
        next_id = l.aggregate(Max('id'))['id__max'] + 1 if l else 1
        if t:
            auction = Auction_list(user_id = request.user , list_name = str(str(request.user.id)+ str(next_id)), url= str(str(request.user.id)+ str(next_id)+".jpg"), auction_list=request.POST["list_name"], starting_bid=request.POST["bid"],category = request.POST["category"].strip().capitalize(), description=request.POST["description"])
            auction.save()
            
            dl_jpg(url ,'media/auctions/', str(str(request.user.id)+str(auction.id)))
        else:
            auction = Auction_list(user_id = request.user , list_name = str(str(request.user.id)+ str(next_id)), auction_list=request.POST["list_name"], starting_bid=request.POST["bid"],category = request.POST["category"].strip().capitalize(), description=request.POST["description"])
            auction.save()
            
            
        
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html",{
        "lenOfWat": findLenOfWat(request.user)
    })



def item(request, item):
    if request.method =="GET":
        datas = Auction_list.objects.filter(list_name__startswith= str(item))
        bids={}
        length = 0
        highest = 0
        for data in datas:
            d = data.id
            highest= data.starting_bid
            user_id = data.user_id
            starting_bid = data.starting_bid
            data = data
        
        if Bids.objects.count() ==  0:
            length = 0
        
        try:
            bids = Bids.objects.filter(list_id = d)
            length = bids.count()
            for bid in bids:
                if highest < bid.your_bids:
                    highest = bid.your_bids
        except Exception as error:
            pass
        currentb = highest
        mini = float(highest) + 0.01
        highest+=1
        high = "{highest:.2f}"

        # The Length of watchlist
        lenOfWat = findLenOfWat(request.user)
        
        # Instance of comments model
        comments = Comments.objects.filter(comment_list_id = data).order_by('timestamp')



        if request.user == user_id:
            bs = Bids.objects.filter(your_bids = currentb)
            for bid in bs:
                user_id = bid.user_id
            return render(request, "auctions/item.html",{
                "datas":datas,
                "bids":bids,
                "length":length,
                "bidder_id":user_id,
                "bidder": user_id.username,
                "lenOfWat": lenOfWat,
                "currentb": currentb,
                "item":item,
                "comments":comments
            })
        else:
            return render(request, "auctions/item.html",{
                "datas":datas,
                "bids":bids,
                "length":length,
                "highest": high.format(highest = highest),
                "min": float(high.format(highest = mini)),
                "lenOfWat": lenOfWat,
                "item":item,
                "comments":comments
                
            })
    else:
        # GET the post data
        post_data = request.POST
        # create instance of auction_lists
        list_id = Auction_list.objects.get(id = post_data["list_id"])
        # create instance of user_id
        user_id = User.objects.get(id = request.user.id)
        # Check for the highest bid in Bids model
        li = Bids.objects.filter(list_id = list_id)
        maxi = 0
        for l in li:
            if l.your_bids > maxi:
                maxi = l.your_bids
        
        if float(post_data["bids"]) <= maxi:
            messages.warning(request,"Please Enter A Higher Bid Than %.2f" % maxi)
        else:
            bids = Bids(user_id = user_id, your_bids = float(post_data["bids"]), list_id = list_id)
            bids.save()
            messages.success(request, 'Place Bid Successful')
        
        # Copy from if statement to render item.html page
        
        
        return HttpResponseRedirect(f"/listing/{post_data['list_name']}")
        


def watchlist(request):
    if request.method == "POST":
        lenOfwat = 0
        post_data = request.POST
        auction_list = Auction_list.objects.get(list_name__startswith= str(f"{post_data['list_name']}"))

        # Try and see if there is element inside of watchlist model
        
        try:
            watchlist = Watchlist.objects.filter(user_id = request.user).filter(auction_list_id = auction_list)
            lenOfwat = watchlist.count()
        except Exception as error:
            pass
        if lenOfwat == 0:
            watchlist = Watchlist(user_id = request.user, auction_list_id = auction_list)
            watchlist.save()
            messages.success(request, 'Added To Watchlist')
        else:
            Watchlist.objects.filter(user_id = request.user).filter(auction_list_id = auction_list).delete()
            messages.success(request, 'Removed From Watchlist')
 
        return HttpResponseRedirect(f"/listing/{post_data['list_name']}")
        
    else:
        return render(request, "auctions/watchlist.html",{
            "lenOfWat": findLenOfWat(request.user),
            "datas": Watchlist.objects.filter(user_id = request.user)
        })



def closed(request):
    if request.method =="GET":
        return render(request, "auctions/closed.html",{
            "datas": Closed_listing.objects.filter(winner = request.user),
            "lenOfWat": findLenOfWat(request.user)
        })


def getItemFromClosed(request, item):
    datas = Closed_listing.objects.filter(winner = request.user).filter(list_name__startswith= str(item))
    
    for data in datas:
        starting_bid = data.starting_bid
        winner_name = data.winner
        auction_name = data.auction_list
        bid_amount = data.bids
        messages.success(request, f"Congratulations! You have won the auction of {auction_name} with the bid of {bid_amount}")
    return render(request, "auctions/closeditem.html",{
        "datas":datas,
        "lenOfWat": findLenOfWat(request.user)
    })



def comment(request):
    if request.method =="POST":
        post_data = request.POST
        auction_lists = Auction_list.objects.get(list_name = str(post_data["id"]))
        comment = Comments(comment_list_id = auction_lists, comments = post_data["input"], comment_user_id= request.user)
        comment.save()
        return HttpResponseRedirect(f"/listing/{post_data['id']}")
    else:
        pass

def category(request):
    if request.method == "GET":
        auction_lists = Auction_list.objects.all()
        lists = []

        # Add categories to lists
        for auction_list in auction_lists:
            lists.append(auction_list.category.capitalize())
        
        # Removes any duplicates from the lists by converting it to dict
        # dict will automatically removes duplicates
        lists = list( dict.fromkeys(lists))

        # Change blank category to be called no category listed
        for l in range(len(lists)):
            if lists[l] == "":
                lists[l] = "No Category Listed"
        


        return render(request,"auctions/category.html",{
            "lenOfWat": findLenOfWat(request.user),
            "listOfcategory": lists
        })
    else:
        if request.POST['category_type'] == "No":
            return HttpResponseRedirect("/category/no_category_listed")
        return HttpResponseRedirect(f"/category/{request.POST['category_type']}")

def getCategory(request, category):
    if request.method == "GET":
        if category == "no_category_listed":
            return render(request,"auctions/getCategory.html",{
            "datas":Auction_list.objects.filter(category = ""),
            "category": "No Category Listed"
            })

        
        return render(request,"auctions/getCategory.html",{
            "datas":Auction_list.objects.filter(category__startswith = category),
            "category": category
        })