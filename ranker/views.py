from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.conf import settings
from itertools import islice
from django.views.generic import TemplateView, ListView
from .models import FrequentPaper,NewPaper, fetchinfo,conferencedata,Mkeyword
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth.models import User
from django.db.models import Max
from django.contrib.auth import logout, authenticate, login
from datetime import datetime
from requests.exceptions import HTTPError
import random
import time
import csv
import os
import json
import requests


# Create your views here.

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
		url = request.POST.get('url')
		paper = NewPaper(papername=papername, authors=authors, conference=conference, rank=rank,url = url, date = datetime.today())
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

class frequentView(ListView):
    template_name = 'paperData.html'

    def get_queryset(self): # new
        
        return paperData
        
def paperData():
	obj = Mkeyword.objects.aggregate(Max('frequency'))
	maxf =obj["frequency__max"] 
	obj = Mkeyword.objects.filter(frequency = maxf).first()
	if(obj==None):
		return []
	kname = obj.keyword
	context =[]
	dbres = fetchinfo.objects.filter(keyword=kname)
	for x in dbres:
		tmp = [x.papername,x.authors[:20],x.rank,x.url,x.conference]
		context.append(tmp)
	return context


def printconf(request):	
	res =dict()
	res["data"] = []
	data = conferencedata.objects.all()
	for x in data:
		res["data"].append({"name":x.name,"rank":x.rank,"type":x.ptype,})
	return JsonResponse(res)



def getconferencedata(request):
	urls = ["http://www.conferenceranks.com/data/era2010.min.js" ,
		"http://www.conferenceranks.com/data/qualis2012.min.js"]
	
	url1= os.path.join(settings.STATIC_ROOT, 'data/CORE.csv')
	url2= os.path.join(settings.STATIC_ROOT, 'data/CJ.csv')
	
	files = [url1 , url2]
	
	fp = open(os.path.join(settings.BASE_DIR, files[0]))
	csvr = csv.reader(fp)
	c = (conferencedata(name = row[1] ,abbrv = row[2], rank = row[4],ptype = row[3]) for row in csvr)

	while True:
		batch = list(islice(c,1000))
		if not batch:
			break
		conferencedata.objects.bulk_create(batch,1000)
	fp = open(os.path.join(settings.BASE_DIR, files[1]))
	csvr = csv.reader(fp)
	c = (conferencedata(name = row[1] ,abbrv = None, rank = row[3],ptype = row[2]) for row in csvr)

	while True:
		batch = list(islice(c,1000))
		if not batch:
			break
		conferencedata.objects.bulk_create(batch,1000)
		
	urls =[[urls[1],'qualis2012']]
	for url in urls:
		continue
		response = requests.get(url[0]).text
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
				c = conferencedata(name = jdata["name"] ,abbrv = jdata["abbrv"], rank = jdata["rank"],ptype = url[1])
				c.save()
	return HttpResponse("success")
	
	
	
class SearchResultsView(ListView):
    template_name = 'paperData.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        
        return search(query)
        

def search(key = "machine learning",key2 =3 ):
	
	
	context =[]
	keyword = key
	keyword = keyword.lower()
	for x in keyword.split():
		mg = NewPaper.objects.filter(papername__contains=x)
		if len(mg):
			mg =mg.first()
			tmp = [mg.papername,mg.authors[:20],mg.rank,mg.url,mg.conference]
			if tmp not in context:
				context.append(tmp)
	
	if Mkeyword.objects.filter(keyword=keyword).exists():
		startpage = Mkeyword.objects.filter(keyword=keyword).first().pages
	else:
		sb = Mkeyword(keyword=keyword,pages =0)
		sb.save()
		startpage=0
	
	key = keyword.replace(" ","+").lower()
	tot = dict()
	total =0
	count =0
	ttime = time.time()
	for mx in range(startpage, startpage+key2):
		val = str(mx*100)
		url = "https://api.semanticscholar.org/graph/v1/paper/search?query="+key+"&limit=100&offset="+val+"&fields=title,authors,venue,year,citationCount,influentialCitationCount,url,isOpenAccess"
	
		response = requests.get(url)
		if  response.status_code != 200:
			print("not 200 ",mx)
			continue
		else:
			print(mx)
		
		jsonr = response.json()
		data = jsonr['data']
		
		for x in data:
			pid_var = x["paperId"]
			if fetchinfo.objects.filter(paperid=pid_var).exists():
				res = fetchinfo.objects.filter(paperid=pid_var).first()
				context.append([res.papername,res.authors[:20],res.rank,res.conference])
				continue
			else:
				total +=1
			papername_var = x["title"]
			auth_var =""
			for y in x["authors"]:
				auth_var = auth_var+", "+y['name']
			auth_var = auth_var[1:]
			if "venue" in x:
				conf_var = x["venue"]
			else:
				conf_var = "NULL"
			cit_var = int(x["citationCount"])
			inflc_var = int(x["influentialCitationCount"] )
			url_var = x["url"]	
			rank_var = "Asd"
			if(conf_var!= "" and  conf_var!= "NULL"):
				if conferencedata.objects.all().filter(name=conf_var): 
					rank_var = conferencedata.objects.filter(name=conf_var).first().rank
				elif conferencedata.objects.all().filter(abbrv=conf_var) :
					rank_var = conferencedata.objects.filter(abbrv=conf_var).first().rank					
				else:
					if conf_var in tot:
						tot[conf_var] +=1
					else:
						tot[conf_var] =1
					continue			
				count+=1
				if len(rank_var) > 2:
					continue	
				
				
				rank_var = rank_var[0]
				b = fetchinfo(keyword =keyword,paperid = pid_var,papername = papername_var,rank =rank_var, authors = auth_var, conference = conf_var,url = url_var, citations = cit_var,infcitations =  inflc_var )
				b.save()
		if count >10:
			
			obj =Mkeyword.objects.filter(keyword=keyword).first()
			obj.pages= mx+1
			obj.frequency = obj.frequency+1
			obj.save()
			break
	
	dbres = fetchinfo.objects.filter(keyword=keyword)
	for x in dbres:
		if len(x.rank) >3 :
			continue
		tmp = [x.papername,x.authors[:20],x.rank,x.url,x.conference]
		context.append(tmp)
	
	context.sort(key = lambda x : x[2] )
	print("time taken : ",time.time() - ttime)

	return context
	


def del_all(self):
	conferencedata.objects.all().delete()
	fetchinfo.objects.all().delete()
	return HttpResponse("deleted")    




