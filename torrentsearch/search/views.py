from django.shortcuts import render, redirect, get_object_or_404
from .forms import SearchForm
from .models import Search, dropboxapitoken
from urllib.request import Request, urlopen
import re
import json
import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
import shutil


def home(request):
	return render(request, 'search/home.html')

def searching(request):
	form = SearchForm()
	params = {'form':form,
		'link':''}
	return render(request, 'search/searching.html', params)


def searchingerr(request, itemid):
	form = SearchForm()
	params = {'form':form,
		'link':'',
		'error':'Already exists do u want to check it or search again?.',
		'itemid':itemid,
		'exists':'Exists'}
	return render(request, 'search/searching.html', params)

def viewtorrent(request, itemid):
	torrObj = get_object_or_404(Search, pk=itemid)
	form = SearchForm(instance=torrObj)
	params = {'form':form,
		'torrent':torrObj}
	return render(request, 'search/viewtorrent.html', params)

def deleteTorrent(request, itemid):
	torrObj = get_object_or_404(Search, pk=itemid)
	if request.method == "POST":
		torrObj.delete()
		return redirect('searching')

def saveTorrent(request, itemid):
	torrObj = get_object_or_404(Search, pk=itemid)
	if request.method == "POST":
		torrObj.save()
		return redirect('searching')

def search_movie_series(request):
	if request.method == 'POST':
		names_list_final=[]
		form = SearchForm(request.POST or None)
		if form.is_valid():
			torr_name_og = form.cleaned_data.get('torrentSearch')
		dbtorrentexist = Search.objects.filter(torrentSearch=torr_name_og)
		if dbtorrentexist.exists():
			dbtorrent = get_object_or_404(Search, torrentSearch=torr_name_og)
			itemid = dbtorrent.pk
			return redirect('searchingerr', itemid=itemid)
		else:
			form.save()
			torr_name = torr_name_og.replace(" ", "%20")
			try:
				req = Request("https://thepiratebay0.org/search/"+torr_name+"/1/99/0", headers={'User-Agent': 'Mozilla/5.0'})
				web = urlopen(req)
			except:
				pass
			try:
				datos = web.read().decode()
				names_list = re.findall(r"(class=\"detLink\" title=(.*?)>)",datos)
				for name in names_list:
				    names_list_final.append(name[1][13:-1])
				link = names_list_final
			except:
				return "There is no torrent for the movie or series you choosed!"
			dbtorrent = get_object_or_404(Search, torrentSearch=torr_name_og)
			dbtorrent.torrentList = link
			dbtorrent.save()
			itemkey = dbtorrent.pk
			return redirect('search_magnetLink',ik=itemkey,name=torr_name_og)

def search_movie_series_(request):
	if request.method == 'POST':
		form = SearchForm(request.POST or None)
		if form.is_valid():
			torr_name_og = form.cleaned_data.get('torrentSearch')
		dbtorrentexist = Search.objects.filter(torrentSearch=torr_name_og)
		if dbtorrentexist.exists():
			dbtorrent = get_object_or_404(Search, torrentSearch=torr_name_og)
			itemid = dbtorrent.pk
			return redirect('searchingerr', itemid=itemid)
		else:
			form.save()
			torr_name = torr_name_og.replace(" ", "+")
			try:
				req = Request("https://1337x.to/search/"+torr_name+"/1/", headers={'User-Agent': 'Mozilla/5.0'})
				web = urlopen(req)
			except:
				req = Request("https://1377x.to/search/"+torr_name+"/1/", headers={'User-Agent': 'Mozilla/5.0'})
				web = urlopen(req)
			try:
				datos = web.read().decode()
				sear = re.search(r"<a href=\"/torrent/",datos )
				posini = sear.span()[0]
				datos_ = datos[posini:]
				link = re.findall(r"<a href=\"/torrent/(.*?)>",datos_)
			except:
				return "There is no torrent for the movie or series you choosed!"
			dbtorrent = get_object_or_404(Search, torrentSearch=torr_name_og)
			dbtorrent.torrentList = link
			dbtorrent.save()
			itemkey = dbtorrent.pk
			return redirect('search_magnetLink',ik=itemkey,name=torr_name_og)


def search_magnetLink_(request, ik, name):
	if request.method == "GET":
		torrObj = get_object_or_404(Search, pk=ik)
		z = []
		z = torrObj.torrentList
		e = []
		for item in z:
			newitem = re.sub(r"/", '#', item)
			e.append(newitem[:-1])
		params = {'links':e, 'torrent': torrObj}
		return render(request, 'search/torrentlinks.html', params)

def search_magnetLink(request, ik, name):
	if request.method == "GET":
		torrObj = get_object_or_404(Search, pk=ik)
		z = []
		z = torrObj.torrentList
		params = {'links':z, 'torrent': torrObj}
		return render(request, 'search/torrentlinks.html', params)

def obtainmagneturl(request, itemid, link):
	torrObj = get_object_or_404(Search, pk=itemid)
	dict_magnet_url = {}
	magnet_list_final = []
	names_list_final = []
	torr_name_og = torrObj.torrentSearch
	torr_name = torr_name_og.replace(" ", "%20")
	try:
		req = Request("https://thepiratebay0.org/search/"+torr_name+"/1/99/0", headers={'User-Agent': 'Mozilla/5.0'})
		web = urlopen(req)
	except:
		pass
	try:
		datos = web.read().decode()
		magnet_url_list = re.findall(r"(\"magnet:\?xt=urn:btih:(.*?)announce\")",datos)
		for magnet in magnet_url_list:
		    magnet_list_final.append(magnet[0][1:-1])
		names_list = re.findall(r"(class=\"detLink\" title=(.*?)>)",datos)
		for name in names_list:
		    names_list_final.append(name[1][13:-1])
		dict_magnet_url = dict(zip(names_list_final,magnet_list_final))
		link_ = dict_magnet_url[link]
		params = {'link':link_, 'torrObj':torrObj}
		torrObj.magnetlink = link_
		torrObj.save()
		return render(request, 'search/obtainmagneturl.html', params)
	except:
		params = {'error':'Issue with the torrent server'}
		return render(request, 'search/searching.html', params)

def obtainmagneturl_(request, itemid, link):
	torrObj = get_object_or_404(Search, pk=itemid)
	t= re.sub(r"#", "/", link)
	try:
	    req = Request("https://1337x.to/torrent/"+t, headers={'User-Agent': 'Mozilla/5.0'})
	    web = urlopen(req)
	except:
	    req = Request("https://1377x.to/torrent/"+t, headers={'User-Agent': 'Mozilla/5.0'})
	    web = urlopen(req)
	try:       
		datos = web.read().decode()
		sear = re.search(r"href=\"magnet:\?xt=urn:btih:",datos )
		posini = sear.span()[0]
		datos_ = datos[posini:]
		sear = re.search(r" onclick=",datos_)
		posfin = sear.span()[1]
		link_ = datos_[6:posfin-10]
		params = {'link':link_, 'torrObj':torrObj}
		torrObj.magnetlink = link_
		torrObj.save()
		return render(request, 'search/obtainmagneturl.html', params)
	except:
		params = {'error':'Issue with the torrent server'}
		return render(request, 'search/searching.html', params)


def dropboxupload(request, itemid):
	torrObj = get_object_or_404(Search, pk=itemid)
	full_dire = "C:\\Users\\016434613\\Desktop\\"+torrObj.torrentSearch+".txt"
	magneturl_ = torrObj.magnetlink 

	with open(full_dire,"w") as outfile:
		outfile.write(magneturl_)


	file_from = full_dire  
	file_to = r"C:\Users\016434613\Desktop\Shared Folder"

	shutil.copy(file_from, file_to)

	params = {'success':'File uploaded successfully','link':magneturl_,
		'torrObj':torrObj}
	return render(request, 'search/obtainmagneturl.html', params)


def dropboxupload_(request, itemid):
	torrObj = get_object_or_404(Search, pk=itemid)
	dbapi = get_object_or_404(dropboxapitoken, pk=1)
	full_dire = "C:\\Users\\016434613\\Desktop\\"+torrObj.torrentSearch+".txt"
	magneturl_ = torrObj.magnetlink 

	with open(full_dire,"w") as outfile:
		outfile.write(magneturl_)

	with dropbox.Dropbox(oauth2_refresh_token=dbapi.oauth2refreshtoken,
		app_key=dbapi.appkey,
		) as dbx:
		print("Successfully set up client!")

	file_from = full_dire  
	file_to = '/movies/'+torrObj.torrentSearch+'.txt'

	f = open(file_from, 'rb')
	dbx.files_upload(f.read(), file_to)

	params = {'success':'File uploaded successfully','link':magneturl_,
		'torrObj':torrObj}
	return render(request, 'search/obtainmagneturl.html', params)


#def subdropboxupload(request, itemid):
	# Tiene que abrir una nueva pagina que tenga un form para poder subir el file
	# y subir eso a la box acctg
#	torrObj = get_object_or_404(Search, pk=itemid)
#	dbapi = get_object_or_404(dropboxapitoken, pk=1)
	#full_dire = "C:\\Users\\016434613\\Desktop\\"+torrObj.torrentSearch+".txt"
	#magneturl_ = torrObj.magnetlink 

	#with open(full_dire,"w") as outfile:
	#	outfile.write(magneturl_)

#	with dropbox.Dropbox(oauth2_refresh_token=dbapi.oauth2refreshtoken,
#		app_key=dbapi.appkey,
#		) as dbx:
#		print("Successfully set up client!")

	#file_from = full_dire  
	#file_to = '/movies/'+torrObj.torrentSearch+'.txt'

	#f = open(file_from, 'rb')
	#dbx.files_upload(f.read(), file_to)

#	params = {'success':'File uploaded successfully','link':magneturl_,
#		'torrObj':torrObj}
#	return render(request, 'search/obtainmagneturl.html', params)


###############################
# Si quisiera armar lo del subtitulo con Opensubtitles se puede:
# https://www.opensubtitles.org/en/search2/sublanguageid-spa,spl/moviename-ted+lasso+s01e04
# lo de arriba es el link para hacer el query, desp hay que buscar el <a bnone [SXXEXX]>
# usar el href de eso, y desp buscar el <a download> y usar ese href, ahora para saber 
# con que ripeo me sirve... tengo que buscarlo en otro lado...
###############################



