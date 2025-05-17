from django.shortcuts import render, redirect
from .models import Car, Bid
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    cars = Car.objects.all()
    return render(request, 'home.html', {"cars": cars})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        User.objects.create_user(
            username = username,
            password = password
        )
        return redirect('login')
    return render(request, 'signup.html')
    

def user_logout(request):
    logout(request)
    return redirect('home')

def add_car(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        starting_bid = request.POST.get('starting_bid')
        end_auction = request.POST.get('auction_end')
        image = request.FILES.get('image')
        Car.objects.create(
            title = title,
            description = description,
            starting_bid = starting_bid,
            end_auction = end_auction,
            image = image,
            owner = request.user
        )
        return redirect('home')
 
    return render(request, 'add_car.html')

@login_required
def car_detail(request, id):
    car = Car.objects.filter(id=id).first()
    bids = car.bids.all().order_by('-amount')
    remaining_time = max((car.end_auction - now()).total_seconds(), 0)
    error_message = None
    auction_active = remaining_time > 0
    winner = None

    if not auction_active and bids.exists():
        winner = bids.order_by('-amount').first().user
        car.winner = winner
        car.save()
    
    if request.method == 'POST':
        if not auction_active:
            error_message = "The auction has ended. No more bids are accepted."
        else:
            amount = request.POST.get('amount')
            if float(amount) > car.starting_bid:
                Bid.objects.create(
                    car = car,
                    user = request.user,
                    amount = amount 
                )
            else:
                error_message = f"Your bid must be higher than ${car.starting_bid:.2f}."

    context = {
        'car': car,
        'bids' : bids,
        'remaining_time' : remaining_time,
        'error_message' : error_message,
        'auction_active' : auction_active,
        'winner' : winner
    }
    return render(request, "car_detail.html", context)