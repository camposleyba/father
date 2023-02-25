from django.shortcuts import render
from .forms import SearchForm
from .models import Search
from urllib.request import Request, urlopen
import re


def home(request):
	return render(request, 'search/home.html')

def searching(request):
	form = SearchForm()
	params = {'form':form}
	return render(request, 'search/searching.html', params)


def search_movie_series(request):
	form = SearchForm(request.POST or None)
	if form.is_valid():
		torr_name = form.cleaned_data.get('torrentSearch')
	torr_name = torr_name.replace(" ", "+")
	try:
		req = Request("https://1337x.to/search/"+torr_name+"/1/", headers={'User-Agent': 'Mozilla/5.0'})
		web = urlopen(req)
	except:
		req = Request("https://1377x.to/search/"+torr_name+"/1/", headers={'User-Agent': 'Mozilla/5.0'})
		web = urlopen(req)
	datos = web.read().decode()
	try:
		sear = re.search(r"<a href=\"/torrent/",datos )
		posini = sear.span()[0]
		datos_ = datos[posini:]
		link = re.findall(r"<a href=\"/torrent/(.*?)>",datos_)
#		search_magnetLink(link)
	except:
		return "There is no torrent for the movie or series you choosed!"
	params = {'link':link}
	return render(request, 'search/searching.html', params)

def search_magnetLink(request, l):
    z=[]
    for e in l:
        z.append(str(l.index(e))+' - '+e)
    p = "\n".join(z)
    a = int(input("\nChoose with a number which link to use starting from 0: "+"\n\n"+p+"\n\n"))
    t = l[a]
    try:
        request = Request("https://1337x.to/torrent/"+t, headers={'User-Agent': 'Mozilla/5.0'})
        web = urlopen(request)
    except:
        request = Request("https://1377x.to/torrent/"+t, headers={'User-Agent': 'Mozilla/5.0'})
        web = urlopen(request)       
    datos = web.read().decode()
    sear = re.search(r"href=\"magnet:\?xt=urn:btih:",datos )
    posini = sear.span()[0]
    datos_ = datos[posini:]
    sear = re.search(r" onclick=",datos_)
    posfin = sear.span()[1]
    link_ = datos_[6:posfin-10]
    params = {'link':link_}
    return render(request, 'search/searching.html', params)