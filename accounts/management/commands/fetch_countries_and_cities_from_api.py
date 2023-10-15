from requests import get

from django.conf import settings
from django.core.management import BaseCommand

from accounts.models import City, Country


class Command(BaseCommand):
    help = "Fetches countries and cities data from an API"

    def handle(self, *args, **options):
        """Fetches the data from the API, processes it, and saves it to the database

        It uses the get() method from the requests library to fetch the data,
        and the process_records() method to process and save the data to the database.
        """

        dataset = "geonames-all-cities-with-a-population-1000"
        url = f"{settings.OPENDATASOFT_BASE_URL}/api/explore/v2.1/catalog/datasets/{dataset}/records"
        params = {
            "select": "name,cou_name_en",
            "order_by": "-population",
            "limit": 100,
            "refine": 'timezone:"Europe"',
        }
        headers = {"User-Agent": settings.USER_AGENT}
        response = get(url, params=params, headers=headers)
        response.raise_for_status()

        records = response.json()["results"]
        countries, cities = self.handle_records(records)

        self.stdout.write(
            self.style.SUCCESS("cities and countries uploaded successfully.")
        )

    def handle_records(self, records):
        """This method takes a list of dict objects as an argument and processes the data by creating Country
        and City objects and saving them to the database.

        It first creates Country objects for each unique country name in the data, and then creates City objects
        for each city name in the data, assigning the corresponding Country object to each City object.
        It uses the bulk_create() method to save the objects to the database in bulk, which reduces number
        of requests to database.
        """

        countries = []
        countries_appended = []
        for record in records:
            country_name = record["cou_name_en"]
            if country_name and country_name not in countries_appended:
                country = Country(name=country_name)
                countries.append(country)
                countries_appended.append(country_name)
        Country.objects.bulk_create(countries)
        countries = {country.name: country for country in Country.objects.all()}
        cities = []
        for record in records:
            country_name = record["cou_name_en"]
            city_name = record["name"]
            if country_name and city_name:
                city = City(name=city_name, country_id=countries[country_name].pk)
                cities.append(city)
        City.objects.bulk_create(cities)
        return countries, cities
