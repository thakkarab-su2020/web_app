from django.shortcuts import render

posts = 'This is a basic signin signup web application'
	


def home(request):
	return render(request,'ui/home.html',{'title':'Home page'})

def about(request):
	context={
		'posts': posts ,
		'title' : 'About Us page',
		
	}
	return render(request,'ui/about.html',context)
