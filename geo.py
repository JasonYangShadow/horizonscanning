from geopy.geocoders import Nominatim

def GetLongLatFromName(name):
    geolocator = Nominatim(user_agent="horizenscanning")
    location = geolocator.geocode(name)
    return (location.address, location.latitude, location.longitude)

def GetAddressFromLongLat(latitude, longtitude):
    geolocator = Nominatim(user_agent="horizenscanning")
    location = geolocator.reverse(str.format("{},{}",latitude, longtitude))
    return location.address
