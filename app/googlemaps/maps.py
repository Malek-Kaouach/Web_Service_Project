import googlemaps
from ..config import settings


#Google Cloud API KEY
API_KEY=settings.api_key



#get current location based on IP adress when the location is empty as an input

def get_current_location():

    gmaps = googlemaps.Client(key=API_KEY)
    geocode_result = gmaps.geolocate()

    lat = geocode_result['location']['lat']
    lng = geocode_result['location']['lng']
    maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
    
    return lat, lng, maps_link



#transform the location inserted into link to google maps search

def get_google_maps_link(location: str) -> str:
    # Clean the location string by removing any leading/trailing spaces
    location = location.strip()

    # Replace any spaces with the plus (+) symbol for the URL
    location = location.replace(' ', '+')

    # Construct the Google Maps link
    google_maps_link = f"https://www.google.com/maps/search/?api=1&query={location}"

    return google_maps_link



