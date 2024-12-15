from geopy.distance import geodesic
from geopy.geocoders import Nominatim


def get_lat_long_nominatim(location):
    """
    Get the latitude and longitude of a location using OpenStreetMap's Nominatim API.

    :param location: A string representing the location (e.g., address or place name).
    :return: Tuple containing latitude and longitude.
    """
    geolocator = Nominatim(user_agent="geoapiExercises")

    # Geocode the location
    location_obj = geolocator.geocode(location)

    if location_obj:
        return (location_obj.latitude, location_obj.longitude)
    else:
        return None


def calculate_distance(point1, point2):
    """
    Calculate the geodesic distance between two points.

    :param point1: Tuple of (latitude, longitude) for the first point.
    :param point2: Tuple of (latitude, longitude) for the second point.
    :return: Distance in kilometers.
    """
    return geodesic(point1, point2).kilometers


# Example usage
if __name__ == '__main__':
    location1 = 'Phu Minh, Soc Son, Ha Noi'
    location2 = '3 Đ. Cầu Giấy, Ngọc Khánh, Đống Đa, Hà Nội'
    lat_long1 = get_lat_long_nominatim(location1)
    lat_long2 = get_lat_long_nominatim(location2)
    print(calculate_distance(lat_long1,lat_long2))


# distance_km = calculate_distance(point1, point2)
# print(f"Distance: {distance_km} km")



# Example usage




