from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from bs4 import BeautifulSoup as bs
import requests
from .models import FrequentPaper,NewPaper, fetchinfo,conferencedata
import json
#-----for authentication-----
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
#-----for date-----
from datetime import datetime
from requests.exceptions import HTTPError
# Create your views here.

#-----SERC - serc@1234-----

gd = {}
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

#-----signout page added-----
def signout(request):
    logout(request)
    return redirect("/")

#-----paperData page added-----
def paperData(request,key = "machine learning"):
	
	
	return render(request,'paperData.html')



def getconferencedata(request):
	url1 = "http://www.conferenceranks.com/data/era2010.min.js"
	url2 = "http://www.conferenceranks.com/data/qualis2012.min.js"
	
	response = requests.get(url2).text
	#print(response.text[:89])
	#fre = response.text[89:-2]
	a=0
	b=0
	ls = []
	
	while(1):	
		a = response.find("{",a+1)
		b = response.find("}",b+1)
		#print(a," ",b)
		if a == -1 :
			break
		else:			
			jdata = json.loads(response[a:b+1])	
			c = conferencedata(name = jdata["name"] ,abbrv = jdata["abbrv"], rank = jdata["rank"],ptype = "qualis")
			c.save()
	#print(response)
	#jsonr = response.json()
	#return JsonResponse(res)
	print(conferencedata.objects.all())
	return HttpResponse("success")

def dbp(request,key = "cryptography"):
	query = ""
	key = key.replace(" ","+").lower()
	url = "https://api.semanticscholar.org/graph/v1/paper/search?query="+key+"&limit=100&offset=0&fields=title,authors,venue,year,citationCount,influentialCitationCount,url,isOpenAccess"
	response = requests.get(url)
	jsonr = response.json()
	data = jsonr['data']
	for x in data:
		pid_var = x["paperId"]
		papername_var = x["title"]
		auth_var =""
		for y in x["authors"]:
			auth_var = auth_var+", "+y['name']
		if "venue" in x:
			conf_var = x["venue"]
		else:
			conf_var = "NULL"
		cit_var = int(x["citationCount"])
		inflc_var = int(x["influentialCitationCount"] )
		rank_var = random.choices(["A","B","C","D","E"])[0]
		url_var = x["url"]		
		b = fetchinfo(keyword ="asd",paperid = pid_var,papername = papername_var,rank =rank_var, authors = auth_var, conference = conf_var,url = url_var, citations = cit_var,infcitations =  inflc_var )
		b.save()
	return JsonResponse(x)
	
def del_all(self):
	conferencedata.objects.all().delete()
	fetchinfo.objects.all().delete()
	return HttpResponse("deleted")    

def printconf(request):	
	res =dict()
	res["data"] = []
	data = conferencedata.objects.all()
	for x in data:
		res["data"].append({"name":x.name,"rank":x.rank,"type":x.ptype,})
	return JsonResponse(res)


def search(request,key):

	global gd
	url = "https://arxiv.org/archive/cs"
	page = requests.get(url)
	gd['soup']  = bs(page.text,"html.parser")	
	soup = gd['soup']
	a = soup.find_all("ul")
	z = a[3].find_all("li")
	print(z[0].find("b"))
	m = z[0].find_all("a")
	return HttpResponse(m)


