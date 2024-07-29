from django.shortcuts import render, redirect
from .models import Contact, Listing, Realtor
from django.core.paginator import Paginator
# from django.core.mail import send_mail
from django.contrib import messages, auth
from django.contrib.auth.models import User

price_choices = {
    "10000000": '₹10,000,000',
    "20000000": '₹20,000,000',
    "30000000": '₹30,000,000',
    "40000000": '₹40,000,000',
    "50000000": '₹50,000,000',
    "60000000": '₹60,000,000',
    "70000000": '₹70,000,000',
    "80000000": '₹80,000,000',
    "90000000": '₹90,000,000',
    "100000000": '₹100,000,000',
}

bedroom_choices = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
}

state_choices = {
    "Andaman and Nicobar Islands": "Andaman and Nicobar Islands",
    "Andhra Pradesh": "Andhra Pradesh",
    "Arunachal Pradesh": "Arunachal Pradesh",
    "Assam": "Assam",
    "Bihar": "Bihar",
    "Chandigarh": "Chandigarh",
    "Chhattisgarh": "Chhattisgarh",
    "Delhi": "Delhi",
    "Goa": "Goa",
    "Gujarat": "Gujarat",
    "Haryana": "Haryana",
    "Himachal Pradesh": "Himachal Pradesh",
    "Jammu and Kashmir": "Jammu and Kashmir",
    "Jharkhand": "Jharkhand",
    "Karnataka": "Karnataka",
    "Kerala": "Kerala",
    "Ladakh": "Ladakh",
    "Lakshadweep": "Lakshadweep",
    "Madhya Pradesh": "Madhya Pradesh",
    "Maharashtra": "Maharashtra",
    "Manipur": "Manipur",
    "Meghalaya": "Meghalaya",
    "Mizoram": "Mizoram",
    "Nagaland": "Nagaland",
    "Odisha": "Odisha",
    "Puducherry": "Puducherry",
    "Punjab": "Punjab",
    "Rajasthan": "Rajasthan",
    "Sikkim": "Sikkim",
    "Tamil Nadu": "Tamil Nadu",
    "Telangana": "Telangana",
    "Tripura": "Tripura",
    "Uttar Pradesh": "Uttar Pradesh",
    "Uttarakhand": "Uttarakhand",
    "West Bengal": "West Bengal"
}


def index(request):
    listings = Listing.objects.order_by(
        "-list_date").filter(is_published=True)[:3]
    realtor = Realtor.objects.all()
    mvp_realtors = realtor.filter(is_mvp=True)
    context = {
        'listings': listings,
        'realtors': realtor,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'is_mvp': mvp_realtors
    }
    return render(request, 'index.html', context)


def about_us(request):
    realtor = Realtor.objects.all()
    mvp_realtors = realtor.filter(is_mvp=True)
    context = {
        'realtors': realtor,
        'is_mvp': mvp_realtors
    }
    return render(request, 'about_us.html', context)


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    context = {
        'listing': listing,
    }
    return render(request, 'listing.html', context)


def listing_index(request):
    listings = Listing.objects.order_by("-list_date").filter(is_published=True)
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paginated_listings = paginator.get_page(page)
    context = {
        'listings': paginated_listings
    }
    return render(request, 'listings.html', context)


def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(
                description__icontains=keywords)

    # City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    # State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedroom = request.GET['bedrooms']
        if bedroom:
            queryset_list = queryset_list.filter(bedrooms__lte=bedroom)

    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET
    }
    return render(request, 'search.html', context)


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            print(username, password)
            return redirect(index)
        else:
            messages.info(request, "Invalid username or password")
            return redirect(login)
    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        print(first_name, last_name, username, email, password, password2)
        if User.objects.filter(username=username).exists():
            messages.info(
                request, "Username already exists. Try with different username.")
            return redirect(register)
        else:
            if password == password2:
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.set_password(password)
                user.save()
                auth.login(request=request, user=user)
                return redirect(index)
            else:
                messages.info(
                    request, "Password does not match!")
            return redirect(register)

    else:
        return render(request, 'register.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
    return redirect(index)


def dashboard(request):
    user_contacts = Contact.objects.order_by(
        '-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts': user_contacts
    }
    return render(request, 'dashboard.html', context)


def contact(request):
    if request.method == "POST":
        listing_id = request.POST.get('listing_id')
        listing = request.POST.get('listing')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        user_id = request.POST.get('user_id')
        realtor_email = request.POST.get('realtor_email')

        contact = Contact(
            listing=listing,
            listing_id=listing_id,
            name=name,
            email=email,
            phone=phone,
            message=message,
            user_id=user_id
        )
        contact.save()
        # send_mail(
        #     subject="Property Listing Inquiry",
        #     message=f"There has been an inquiry for {listing}. Sign into the admin panel for more info.",
        #     from_email="fakeashking1956@gmail.com",
        #     recipient_list=[realtor_email, 'fakeashking1956@gmail.com'],
        #     fail_silently=False
        # )
        messages.success(
            request, "Your request has been submitted, a realtor will get back to you soon.")
        print(listing_id, listing, name, email,
              phone, message, user_id, realtor_email)
    # Make sure 'listing_index' is a valid URL name
    return redirect(listing_index)
