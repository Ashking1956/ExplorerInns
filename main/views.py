from django.shortcuts import render
from .models import Listing, Realtor
from django.core.paginator import Paginator

price_choices = {
    "100000": '$100,000',
    "200000": '$200,000',
    "300000": '$300,000',
    "400000": '$400,000',
    "500000": '$500,000',
    "600000": '$600,000',
    "700000": '$700,000',
    "800000": '$800,000',
    "900000": '$900,000',
    "1000000": '$1,000,000',
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
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District Of Columbia",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
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
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)
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
            queryset_list = queryset_list.filter(
                city__iexact=city)

    # State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(
                state__iexact=state)

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedroom = request.GET['bedrooms']
        if bedroom:
            queryset_list = queryset_list.filter(
                bedrooms__lte=bedroom)

    # Bedrooms
    if 'price' in request.GET:
        temp = request.GET['price']
        if temp:
            queryset_list = queryset_list.filter(
                price__lte=temp)

    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values' : request.GET
    }
    return render(request, 'search.html', context)


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')
