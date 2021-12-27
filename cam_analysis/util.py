from geopy.geocoders import Nominatim

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"

# https://github.com/geopy/geopy#geocoding
def get_canton_from_latlon(latitude, longitude, user_agent=None):
    if user_agent is None:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    geolocator = Nominatim(user_agent=user_agent)
    location = geolocator.reverse(
        query=(latitude, longitude),
        exactly_one=True,
        timeout=10,
    )
    loc_addr_ = location.address.replace(" ", "").split(",")
    canton = loc_addr_[-3]
    return canton.split("/")[0], location.address
