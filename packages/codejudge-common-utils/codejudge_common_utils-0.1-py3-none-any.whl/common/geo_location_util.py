import reverse_geocoder as rg

from restapi.common.list_util import ListUtil


class GeoLocationUtil:

    @classmethod
    def find_reverse_geocode(cls, latitude, longitude):
        coordinates = (latitude, longitude)
        locations = rg.search(coordinates)
        city = 'Unknown'
        state = 'Unknown'
        country = 'Unknown'
        if ListUtil.is_valid(locations):
            location = locations[0]
            city = location['name']
            state = location['admin1']
            country = location['cc']
        return dict(city=city, state=state, country=country)

    @classmethod
    def geo_location_key(cls, location_addr):
        return location_addr['city'] + ' | ' + location_addr['state'] + ' | ' + location_addr['country']
