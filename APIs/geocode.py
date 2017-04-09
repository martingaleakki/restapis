import httplib2
import json
from datetime import datetime


def getGeocodeLocation(inputString):
    # Use Google Maps to convert a location into Latitute/Longitute coordinates
    # FORMAT: https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=API_KEY
    google_api_key = "AIzaSyDQlqTwQpjEm2TyO05pKt3KF11CY58x2-w"
    locationString = inputString.replace(" ", "+")
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (locationString, google_api_key))
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    return (latitude, longitude)


def findARestaurant(mealType, location):
    latitude, longitude = getGeocodeLocation(location)
    foursquare_client_id = "KAKTHG0ZJDGFSIHTJ45LVFMOCNZ4W0IGT1RLSJHVVAILFEL0"
    foursquare_client_secret = "WAMXORRSH0KUNT0KAVKGGB301EEOT033UUZD5R2KI422WPPJ"
    foursquare_ll = str(latitude) + "," + str(longitude)
    foursquare_v = datetime.today().strftime('%Y%m%d')
    url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=%s&ll=%s&query=%s' % (
        foursquare_client_id,
        foursquare_client_secret,
        foursquare_v,
        foursquare_ll,
        mealType))
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    data = {}
    if result['response']['venues']:
        restaurant = result['response']['venues'][0]
        data["name"] = restaurant['name']
        data["address"] = ' '.join(restaurant['location']['formattedAddress'])
        venue_id = restaurant["id"]
        url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&client_secret=%s&v=%s' % (
            (venue_id, foursquare_client_id, foursquare_client_secret,foursquare_v)))
        result = json.loads(h.request(url, 'GET')[1])
        if result['response']['photos']['items']:
            firstpic = result['response']['photos']['items'][0]
            prefix = firstpic['prefix']
            suffix = firstpic['suffix']
            imageURL = prefix + "300x300" + suffix
        else:
            # 6.  if no image available, insert default image url
            imageURL = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"
        data["imageURL"] = imageURL
    return data