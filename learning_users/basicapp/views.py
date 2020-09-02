from django.shortcuts import render
from basicapp.forms import UserForm, UserProfileInfoForm

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(req):
    return render(req, 'basicapp/index.html')

@login_required
def special(req):
    return HttpResponse('You are logged in, Nice :D')

@login_required
def user_logout(req):
    logout(req)
    return HttpResponseRedirect(reverse('index'))

def register(req):
    registered = False
    if req.method == 'POST':
        user_form = UserForm(data=req.POST)
        profile_form = UserProfileInfoForm(data=req.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in req.FILES:
                profile.profile_pic = req.FILES['profile_pic']
            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(req, 'basicapp/registration.html', {'user_form':user_form,
                                                    'profile_form':profile_form,
                                                    'registered': registered})

def user_login(req):
    if req.method == 'POST':
        username = req.POST.get('username') # This is what we named the input type in the html page
        pswd = req.POST.get('password')

        user = authenticate(username=username, password=pswd)

        if user:
            if user.is_active:
                login(req, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account is not active')
        else:
            print('Someone trued to ogin and failed')
            print('Username: {} and Password: {}'.format(username, pswd))
            return HttpResponse('Invalid login details supplied')
    else:
        return render(req, 'basicapp/login.html', {})
