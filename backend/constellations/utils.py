import astropy.coordinates as coord
from astropy import units as u
from astropy.time import Time
from backend.constellations.models import Constellation


def get_visible_constellations(longitude , latitude , ):
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
        if constellation_altaz.alt.degree > 0:  # Если созвездие выше горизонта
            visible_constellations.append(constellation)

    return visible_constellations