from django.shortcuts import render,redirect
from hobby_app.forms import UserForm
from django.contrib import auth
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
def index(request):
    formu = UserForm()
    form = {'form':formu}
    return render(request,'hobby_app/login.html',context=form)#Always use context=

def register(request):
    registered = False

    if request.method =='POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save(commit = False)
            user.set_password(user.password)
            user.save()

            registered = True

        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    #return redirect(index,{'form1':LoginForm,'form':user_form , 'registered':registered , 'errors':user_form.errors})
    return render(request,'hobby_app/login.html',{'form':user_form , 'registered':registered , 'errors':user_form.errors})

def user_login(request):
    if request.method=='POST':
        email = request.POST.get('Email')
        password = request.POST.get('Password')
        print(password)
        try:
            u = User.objects.get(email = email)
        except:
            u = None
        if u:
            print(u.password)
            user = authenticate(username = u.username, password = password)
            print(user)
            if user:
                login(request,user)
                fo = UserForm()
                form = {'form':fo}
                return render(request,'hobby_app/login.html',context=form)
            else:
                return HttpResponse("Wrong pass")
        else:
            return HttpResponse("Wrong email")



    else:
        return render(request,'hobby_app/login.html',{})
#View for logging out user
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
#This is the front page. Also used for logging out.
@login_required
def front(request):
    return render(request,'hobby_app/index.html',{})
