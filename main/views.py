from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import datetime
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm


def user_login(request):
    if request.method == 'POST':
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)
        if user is not None:
            # Save session as cookie to login the user
            login(request, user)
            # Success, now let's login the user.
            return render(request, 'main/index.html')
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'main/login.html', {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, 'main/login.html')


def logout_view(request):
    logout(request)
    return render(request, 'main/login.html')


def user_register(request):
    # if this is a POST request we need to process the form data
    template = 'main/signup.html'
   
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Passwords do not match.'
                })
            else:
                # Create the user:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                
                user.save()
               
                # Login the user
                #login(request, user)
               
                # redirect to accounts page:
                return render(request,'main/index.html')

   # No post data availabe, let's just show the page.
    else:
        form = RegisterForm()

    return render(request, template, {'form': form})
# Create your views here.
@login_required(login_url='/login/')
def getresults(request):
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
			nowdate = datetime.datetime.now()
			print(title.strip())
			print(present_price)
			nowdate = str(nowdate)
			content = {
			'nowdate':nowdate,
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
		return render(request,'main/index.html',{'context':content})
	return render(request,'main/index.html')
