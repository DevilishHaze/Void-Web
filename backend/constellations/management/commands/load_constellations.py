# load_constellations.py

from django.core.management.base import BaseCommand
from backend.constellations.models import Constellation
from astropy.coordinates import get_constellation
from astropy.coordinates import SkyCoord
from astropy import units as u

class Command(BaseCommand):
    help = 'Load constellations into the database'

    def handle(self, *args, **kwargs):
        # Define RA and Dec ranges to cover all constellations
        ra_list = [i for i in range(0, 360, 10)]  # RA from 0 to 360 degrees in steps of 10 degrees
        dec_list = [i for i in range(-90, 91, 10)]  # Dec from -90 to 90 degrees in steps of 10 degrees
        constellations = set()

        for ra in ra_list:
            for dec in dec_list:
                coord = SkyCoord(ra=ra*u.degree, dec=dec*u.degree)
                const_name = get_constellation(coord)
                constellations.add((const_name, ra, dec))

        for const_name, ra, dec in constellations:
            constellation, created = Constellation.objects.get_or_create(
                name=const_name,
                defaults={'ra': ra, 'dec': dec}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added constellation {constellation.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Constellation {constellation.name} already exists'))
