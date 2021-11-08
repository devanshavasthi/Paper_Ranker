from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from ranker.models import fetchinfo

from bs4 import BeautifulSoup as bs
import selenium
import requests
from .models import FrequentPaper,NewPaper

#-----for authentication-----
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
#-----for date-----
from datetime import datetime
from requests.exceptions import HTTPError
import random

# Create your views here.

#-----SERC - serc@1234-----

def index(request):
	return render(request,'index.html')

#-----new html page added-----
def paper(request):
	#-----Adding data from POST request-----
	if request.method == "POST":
		papername = request.POST.get('name')
		authors = request.POST.get('author')
		conference = request.POST.get('conference')
		rank = request.POST.get('rank')
		paper = NewPaper(papername=papername, authors=authors, conference=conference, rank=rank, date = datetime.today())
		paper.save()
	return render(request,'paper.html')

#-----signin page added-----
def signin(request):
	#-----login credentials-----
	if request.method=="POST":
		username = request.POST.get('username')
		password = request.POST.get('password')


		#-----if user has entered correct credentials-----
		user = authenticate(username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect("/paper")

		else:
			return render(request, 'signin.html')

	return render(request,'signin.html')

def signout(request):
    logout(request)
    return redirect("/")


def search(request,key):
	

	'''url = "https://arxiv.org/archive/cs"
	page = requests.get(url)
	gd['soup']  = bs(page.text,"html.parser")	
	soup = gd['soup']
	a = soup.find_all("ul")
	z = a[3].find_all("li")
	print(z[0].find("b"))
	m = z[0].find_all("a")
	return HttpResponse(m)'''

def dbp(request,key = "machine+learning"):
	query = ""
	key = key.replace(" ","+").lower()
	url = "https://api.semanticscholar.org/graph/v1/paper/search?query="+key+"&limit=100&offset=100&fields=title,authors,venue,year,citationCount,influentialCitationCount,url,isOpenAccess"
	response = requests.get(url)
	jsonr = response.json()
	data = jsonr['data']
	for x in data:
		print(x)
		pid = x["paperId"]
		papername = x["title"]
		auth =""
		for y in x["authors"]:
			auth = auth+", "+y['name']
			authors = auth
		if "venue" in x:
			conf = x["venue"]
		else:
			conf = "NULL"
		cit = int(x["citationCount"])
		infc = int(x["influentialCitationCount"] )
		rank = random.choices(["A","B","C","D","E"])[0]
		url = x["url"]		
		print(x["isOpenAccess"] ,type(x["isOpenAccess"] ))
		b = fetchinfo(keyword ="asd",paperid = pid,papername = papername,rank =rank, authors = auth, conference = conf,url = url, citations = cit,infcitations =  infc )
		b.save()
	return JsonResponse(x)
	
def del_all(self):
	fetchinfo.objects.all().delete()
	return HttpResponse("deleted")    
