from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import joblib
from django.shortcuts import render
import folium
from geopy.geocoders import Nominatim
from geopy.geocoders import ArcGIS

def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method =='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            return HttpResponse("Please check password and confirm password")
        else:
            create_user = User.objects.create_user(username, email, password1)
            create_user.save()
            return redirect("login")
    
    return render(request, 'signup.html')


def login(request):
    if (request.method =='POST'):
        Username = request.POST.get('username')
        password = request.POST.get('pass')
        user = authenticate(request, username=Username, password=password)
        if user:
            

            return redirect("home")
        else:
            return HttpResponse("Incorrect")
        
    return render(request, 'login.html', {'message': "Please Login!"})


def logout(request):
    logout(request)
    return redirect("login")

def result(request):
    model = joblib.load('model.sav')
    lis = []
    lis.append(request.GET['Pregnancies'])
    lis.append(request.GET['Glucose'])
    lis.append(request.GET['BloodPressure'])
    lis.append(request.GET['SkinThickness'])
    lis.append(request.GET['Insulin'])
    lis.append(request.GET['BMI'])
    lis.append(request.GET['DiabetesPedigreeFunction'])
    lis.append(request.GET['Age'])
    print(lis)
    ans = 0
    res = [eval(i) for i in lis]
    ans = model.predict([res])
    if(ans [0]==1):
        return render(request,'result.html',{'ans':'You have Predicted Diabetic'}) 
    else:
        return render(request,'result.html',{'ans':'You cannot have Diabetic'})
    
