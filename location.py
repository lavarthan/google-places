from geopy import geocoders


def get_location(place):
    geolocator = geocoders.GoogleV3('AIzaSyAU3Z7XiTGIorugANNLOj2snKJUrb8RyPk')
    location = geolocator.geocode(place)
    return str(location.latitude), str(location.longitude)
