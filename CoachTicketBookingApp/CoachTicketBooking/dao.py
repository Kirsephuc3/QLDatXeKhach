from .models import *
from django.db.models import Q, Count


def load_user(params={}):
    q = User.objects.filter()

    username = params.get('username')
    if username:
        q = q.filter(username__icontains=username)

    role = params.get('role')
    if role:
        q = q.filter(role=role)

    user_id = params.get('id')
    if user_id:
        q = q.filter(id=user_id)

    name = params.get('name')
    if name:
        q = q.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))

    active = params.get('active')
    if active:
        q = q.filter(active=active)

    return q


def load_trip(params={}):
    q = Trip.objects.all()

    depart = params.get('depart')
    if depart:
        q = q.filter(route__depart=depart)

    dest = params.get('dest')
    if dest:
        q = q.filter(route__dest=dest)

    departure_date = params.get('departure_date')
    if departure_date:
        q = q.filter(departure_date=departure_date)

    return q

def load_seller(params={}):
    q = TicketSeller.objects.all()

    depart = params.get('depart')
    if depart:
        q = q.filter(route__depart=depart)

    dest = params.get('dest')
    if dest:
        q = q.filter(route__dest=dest)

    departure_date = params.get('departure_date')
    if departure_date:
        q = q.filter(departure_date=departure_date)

    return q