from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup as bs
import selenium
import requests

# Create your views here.


gd = {}
def index(request):
	return render(request,'ranker/index.html')


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


