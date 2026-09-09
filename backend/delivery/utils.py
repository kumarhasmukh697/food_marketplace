import math
from .models import DeliveryPartnerProfile 

def calculate_distance( latitude1, longitude1, latitude2, longitude2):
    """
    Calculate distance between two GPS coordinates
    using the Haversine formula.

    Returns distance in kilometers.
    """

    latitude1 = float(latitude1)
    longitude1 = float(longitude1)
    latitude2 = float(latitude2)
    longitude2 = float(longitude2)

    earth_radius = 6371.0

    lat1 = math.radians(latitude1)
    lat2 = math.radians(latitude2)

    delta_lat = math.radians(latitude2 - latitude1)
    delta_lon = math.radians(longitude2 - longitude1)

    a = (
        math.sin(delta_lat / 2) ** 2
        +
        math.cos(lat1)
        *
        math.cos(lat2)
        *
        math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2( math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * c
    return distance






def find_nearest_delivery_partner( vendor_latitude, vendor_longitude):

    available_partners = ( DeliveryPartnerProfile.objects.select_related("user").select_for_update()
        .filter(is_online=True, is_available=True, current_latitude__isnull=False, current_longitude__isnull=False,)
    )

    if not available_partners.exists():
        return None

    nearest_partner = None
    shortest_distance = None

    for partner in available_partners:
        distance = calculate_distance( vendor_latitude, vendor_longitude, partner.current_latitude, partner.current_longitude,)

        if ( shortest_distance is None or distance < shortest_distance):
            shortest_distance = distance
            nearest_partner = partner
    return nearest_partner, shortest_distance