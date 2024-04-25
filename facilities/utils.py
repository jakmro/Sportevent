from django.conf import settings
import requests
import json


def geocode(location):
    location_url_format = location.replace(' ', '+')

    res = requests.get(
        f'https://maps.googleapis.com/maps/api/geocode/json?address={location_url_format}&key={settings.GOOGLE_API_KEY}'
    )
    response = json.loads(res.text)

    try:
        latitude = response['results'][0]['geometry']['location']['lat']
        longitude = response['results'][0]['geometry']['location']['lng']
    except IndexError:
        latitude, longitude = None, None

    return latitude, longitude
