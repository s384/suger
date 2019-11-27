from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'core/index.html')

def user(request):
    return render(request, 'core/user.html')

def typeUser(request):
    return render(request, 'core/type.html')

def job(request):
    return render(request, 'core/job.html')

def turn(request):
    return render(request, 'core/turn.html')