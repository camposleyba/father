from urllib.request import Request, urlopen
import re

def search_movie_series(addr):
    try:
        request = Request("https://1337x.to/search/"+addr+"/1/", headers={'User-Agent': 'Mozilla/5.0'})
        web = urlopen(request)
    except:
        request = Request("https://1377x.to/search/"+addr+"/1/", headers={'User-Agent': 'Mozilla/5.0'})
        web = urlopen(request)
    datos = web.read().decode()
    try:
        sear = re.search(r"<a href=\"/torrent/",datos )
        posini = sear.span()[0]
        datos_ = datos[posini:]
        sear = re.search(r"\/\">",datos_ )
        posfin = sear.span()[1]
        link = datos_[10:posfin-2]
        return link
    except:
        return "There is no torrent for the movie or series you choosed!"

def search_magnetLink(l):
    try:
        request = Request("https://1337x.to/"+l, headers={'User-Agent': 'Mozilla/5.0'})
        web = urlopen(request)
    except:
        request = Request("https://1377x.to/"+l, headers={'User-Agent': 'Mozilla/5.0'})
        web = urlopen(request)       
    datos = web.read().decode()
    sear = re.search(r"href=\"magnet:\?xt=urn:btih:",datos )
    posini = sear.span()[0]
    datos_ = datos[posini:]
    sear = re.search(r" onclick=",datos_)
    posfin = sear.span()[1]
    link_ = datos_[6:posfin-10]
    return link_

def search_torrentLink(l):
    request = Request("https://1337x.to/"+l, headers={'User-Agent': 'Mozilla/5.0'})
    web = urlopen(request)
    datos = web.read().decode()
    return datos