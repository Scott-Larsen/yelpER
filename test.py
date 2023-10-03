from geopy.geocoders import Nominatim

address = "34.146759, -118.000373"
# address ="112, East Lemon Avenue, Monrovia, Los Angeles County, California, 91016"

geolocator = Nominatim(user_agent="YelpER")

location = geolocator.geocode(address)

print(location.latitude, location.longitude)
print(type(location.latitude), type(location.longitude))

# >>> from geopy.geocoders import Nominatim
# >>> geolocator = Nominatim(user_agent="specify_your_app_name_here")
# >>> location = geolocator.geocode("175 5th Avenue NYC")
# >>> print(location.address)
# Flatiron Building, 175, 5th Avenue, Flatiron, New York, NYC, New York, ...
# >>> print((location.latitude, location.longitude))
# (40.7410861, -73.9896297241625)
# >>> print(location.raw)
# {'place_id': '9167009604', 'type': 'attraction', ...}