import random
from faker import Faker
from faker.providers import BaseProvider

fake = Faker()


class CoreProvider(BaseProvider):
    def region(self):
        regions = ['UW', 'UE', 'NR', 'BR', 'BE', 'AHAFO', 'AR', 'ER', 'WR', 'GR', 'SR', 'OTI', 'VR', 'CR', 'NER', 'WNR']
        return random.choice(regions)

    def city(self):
        cities = ['Wa', 'Nadowli', 'Kaleo', 'Jirapa', '', 'Tumu', 'Gwollu', 'Hamile', 'Sombo', 'Babile']
        return random.choice(cities)


fake.add_provider(CoreProvider)
