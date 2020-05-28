from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth import update_session_auth_hash,login,authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from blog.views import home
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			user = authenticate(username=username,password=password)
			login(request,user)
			messages.success(request, "Account created for {}!  And you are now logged in!".format(username))
			return redirect('profile')
	else:
		form = UserRegisterForm()

	return render(request,'users/register.html',{'form':form})


@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		if u_form.is_valid():
			u_form.save()
			messages.success(request, "Account has been updated")
			return redirect('profile')
	else:
		u_form = UserUpdateForm( instance=request.user)

		
	context = {
	'u_form': u_form,
	}

	return render(request,'users/profile.html',context)

@login_required
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm( data=request.POST, user=request.user)
		
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, "Your Password has been updated!")
			return redirect('profile')
		else:
			
			return render(request,'users/change_password.html',{'form':form})
	else:
		
		form = PasswordChangeForm(user=request.user)
		return render(request,'users/change_password.html',{'form':form})



