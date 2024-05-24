import astropy.coordinates as coord
from astropy import units as u
from astropy.time import Time
from backend.constellations.models import Constellation
import  numpy as np

def calculate_airmass(altitude):
    altitude = u.Quantity(altitude,u.deg)
    altitude_rad = altitude.to(u.rad).value
    return 1.0 /(np.sin(altitude_rad)+0.50572*(6.07995 + altitude.value)**(-1.6364))  # формула Кошенака 0.50572, 6.07995 и -1.6364 это константы для вычисления


def get_visible_constellations(longitude , latitude , min_altitude= 15 ):

    now = Time.now()

    # Преобразование  координат долготы и широты в небесные координаты
    observer_location = coord.EarthLocation(lon=longitude * u.degree , lat=latitude * u.degree)
    observer_skycoord = coord.AltAz(location=observer_location , obstime=now)

    # Загрузика списка созвездий
    constellations = Constellation.objects.all()

    # Проверка на видимость
    visible_constellations = []
    for constellation in constellations:
        constellation_skycoord = coord.SkyCoord(ra=constellation.ra * u.degree , dec=constellation.dec * u.degree , frame='icrs')
        constellation_altaz = constellation_skycoord.transform_to(observer_skycoord)
        if constellation_altaz.alt.degree > min_altitude:           # Если созвездие выше указанного минимального значения в 15 градусов
            airmass_value = calculate_airmass(constellation_altaz.alt.degree)
            if airmass_value < 3:
                visible_constellations.append(constellation)

    return visible_constellations