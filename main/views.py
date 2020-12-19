from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import datetime

# Create your views here.
def index(request):
	if request.POST.get('showprice'):
		try:
			URL = request.POST['url']
			print(URL)
			session = requests.session()
			session.headers['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"

			res = session.get(URL)

			soup = BeautifulSoup(res.content,'html.parser')
		
			try:
				title = soup.find(id="productTitle").get_text()
				price = soup.find(id="priceblock_ourprice").get_text()
			except:
				price = soup.find(id="priceblock_dealprice").get_text()
			price = price.replace(',','')
			present_price = float(price.strip()[2::])

			print(title.strip())
			print(present_price)
			print(datetime.datetime.now())
			content = {
			'url': URL,
			'title': title,
			'price':price
			}
		except:
			data = "Please check the link...!" 
			print(data)
			content = {
			'data': data
			}
		return render(request,'index.html',{'context':content})
	if request.POST.get('saveprice'):
		URL = request.POST.get('url')
		print(URL)
		content = {
		'url': URL
		}
		return render(request,'index.html',{'context':content})
	return render(request,'index.html')
