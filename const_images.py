import os
import django
import requests
from bs4 import BeautifulSoup

# Установка настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from backend.constellations.models import Constellation

# Массив названий созвездий
constellations = [
    "Andromeda" , "Antlia" , "Apus" , "Aquarius" , "Aquila" ,
    "Ara" , "Aries" , "Auriga" , "Boötes" , "Caelum" , "Camelopardalis" ,
    "Cancer" , "Canes Venatici" , "Canis Major" , "Canis Minor" ,
    "Capricornus" , "Carina" , "Cassiopeia" , "Centaurus" ,
    "Cepheus" , "Cetus" , "Chamaleon" , "Circinus" , "Columba" , "Coma Berenices" ,
    "Corona Australis" , "Corona Borealis" , "Corvus" , "Crater" , "Crux" ,
    "Cygnus" , "Delphinus" , "Dorado" , "Draco" , "Equuleus" ,
    "Eridanus" , "Fornax" , "Gemini" , "Grus" , "Hercules" , "Horologium" ,
    "Hydra" , "Hydrus" , "Indus" , "Lacerta" , "Leo" , "Leo Minor" , "Lepus" ,
    "Libra" , "Lupus" , "Lynx" , "Lyra" , "Mensa" , "Microscopium" , "Monoceros" ,
    "Musca" , "Norma" , "Octans" , "Ophiucus" , "Orion" ,
    "Pavo" , "Pegasus" , "Perseus" , "Phoenix" , "Pictor" ,
    "Pisces" , "Pisces Austrinus" , "Puppis" , "Pyxis" , "Reticulum" , "Sagitta" ,
    "Sagittarius" , "Scorpius" , "Sculptor" , "Scutum" , "Serpens" , "Sextans" ,
    "Taurus" , "Telescopium" , "Triangulum" , "Triangulum Australe" ,
    "Tucana" , "Ursa Major" , "Ursa Minor" , "Vela" , "Virgo" ,
    "Volans" , "Vulpecula"
]
manual_image_urls ={
    "Andromeda": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Andromeda_IAU.svg/435px-Andromeda_IAU.svg.png",
    "Aquarius" : "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Aquarius_IAU.svg/435px-Aquarius_IAU.svg.png",
    "Aquila" : "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Aquila_IAU.svg/800px-Aquila_IAU.svg.png",
    "Ara" : "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Ara_IAU.svg/435px-Ara_IAU.svg.png",
    "Aries": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Aries_IAU.svg/435px-Aries_IAU.svg.png",
    "Auriga":"https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Auriga_IAU.svg/435px-Auriga_IAU.svg.png",
    "Carina":"https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Carina_IAU.svg/435px-Carina_IAU.svg.png",
    "Cassiopeia": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Cassiopeia_IAU.svg/800px-Cassiopeia_IAU.svg.png",
    "Cepheus":"https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Cepheus_IAU.svg/800px-Cepheus_IAU.svg.png",
    "Chamaleon":"https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Chamaeleon_IAU.svg/800px-Chamaeleon_IAU.svg.png",
    "Crater": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Crater_IAU.svg/800px-Crater_IAU.svg.png",
    "Cygnus": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Cygnus_IAU.svg/800px-Cygnus_IAU.svg.png",
    "Draco": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Draco_IAU.svg/435px-Draco_IAU.svg.png",
    "Gemini": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Gemini_IAU.svg/800px-Gemini_IAU.svg.png",
    "Grus" : "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Grus_IAU.svg/800px-Grus_IAU.svg.png",
    "Horologium": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Horologium_IAU.svg/800px-Horologium_IAU.svg.png",
    "Hydra": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Hydra_IAU.svg/1280px-Hydra_IAU.svg.png",
    "Leo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Leo_IAU.svg/800px-Leo_IAU.svg.png",
    "Libra":"https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Libra_IAU.svg/800px-Libra_IAU.svg.png",
    "Mensa":"https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Mensa_IAU.svg/800px-Mensa_IAU.svg.png",
    "Norma":"https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Norma_IAU.svg/800px-Norma_IAU.svg.png",
    "Orion":"https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Orion_IAU.svg/800px-Orion_IAU.svg.png",
    "Pavo":"https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Pavo_IAU.svg/800px-Pavo_IAU.svg.png",
    "Phoenix":"https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Phoenix_IAU.svg/800px-Phoenix_IAU.svg.png",
    "Pisces":"https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Pisces_IAU.svg/800px-Pisces_IAU.svg.png",
    "Sculptor" : "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Sculptor_IAU.svg/800px-Sculptor_IAU.svg.png",
    "Scutum" : "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Scutum_IAU.svg/800px-Scutum_IAU.svg.png",
    "Taurus" : "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Taurus_IAU.svg/800px-Taurus_IAU.svg.png",
    "Vela" : "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Vela_IAU.svg/800px-Vela_IAU.svg.png",
    "Virgo" : "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Virgo_IAU.svg/1024px-Virgo_IAU.svg.png",
    "Sagittarius" : "https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Sagittarius_IAU.svg/800px-Sagittarius_IAU.svg.png",
    "Pisces Austrinus":"https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Piscis_Austrinus_IAU.svg/800px-Piscis_Austrinus_IAU.svg.png",
    "Eridanus":"https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Eridanus_IAU.svg/435px-Eridanus_IAU.svg.png",
    "Ophiucus":"https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Ophiuchus_IAU.svg/800px-Ophiuchus_IAU.svg.png"
}
def get_image_url_from_wikipedia(constellation_name):
    search_url = f"https://en.wikipedia.org/wiki/{constellation_name.replace(' ', '_')}"
    response = requests.get(search_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')


        infobox = soup.find('table', {'class': 'infobox'})
        if infobox:

            image = infobox.find('img')
            if image and image.has_attr('src'):
                return f"https:{image['src']}"


        content_images = soup.find_all('img')
        for image in content_images:
            if image.has_attr('alt') and 'constellation' in image['alt'].lower():
                if image.has_attr('src') and image['src'].startswith('//upload.wikimedia.org/wikipedia/commons'):
                    return f"https:{image['src']}"

    return None


for constellation_name in constellations:
    if constellation_name in manual_image_urls:
        image_url = manual_image_urls[constellation_name]
    else:
        image_url = get_image_url_from_wikipedia(constellation_name)

    if image_url:
        try:
            constellation = Constellation.objects.get(name=constellation_name)
            constellation.image_url = image_url
            constellation.save()
            print(f"Updated {constellation_name} with image URL: {image_url}")
        except Constellation.DoesNotExist:
            print(f"Constellation {constellation_name} not found in database.")
    else:
        print(f"Image not found for {constellation_name}")
