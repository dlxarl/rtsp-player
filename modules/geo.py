import requests
import socket
from PIL import Image, ImageTk
from io import BytesIO

flag_cache = {}

FILE_OVERRIDES = {
    "United States": "usa",
    "United Kingdom": "uk",
    "Russia": "russian",
    "China": "china",
    "France": "france",
    "Spain": "spain",
    "Hong Kong": "hong-kong",
    "England": "england",
}


def get_ip_from_url(url):
    try:
        clean_url = url.replace("rtsp://", "")
        if "@" in clean_url:
            host = clean_url.split("@")[1]
        else:
            host = clean_url

        host = host.split(":")[0].split("/")[0]
        return socket.gethostbyname(host)
    except:
        return None


def get_country_name(ip):
    if not ip:
        return None
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=2)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                return data['country']
    except:
        pass
    return None


def get_flag_icon(country_name):
    if not country_name:
        return None

    if country_name in flag_cache:
        return flag_cache[country_name]

    filename = FILE_OVERRIDES.get(country_name, country_name)

    url = f"https://rene-crevel.com/images/country-flag-16X16/{filename}.png"

    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            img_data = response.content
            image = Image.open(BytesIO(img_data))
            photo = ImageTk.PhotoImage(image)
            flag_cache[country_name] = photo
            return photo
        else:
            print(f"Flag not found for: {country_name} -> {url}")
    except:
        pass
    return None