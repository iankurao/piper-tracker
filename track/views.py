from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product
from django.contrib.auth.models import User
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib import messages
from track.models import Product
# from pricetracker import settings
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from users.forms import UserRegisterForm

def home(request):
    context={

      'products':Product.objects.all(),
      'title':'Home'


    }
    return render(request,'track/home.html',context)#title is optional


class ProductListView(ListView):
    model = Product
    template_name = 'track/home.html'  # <app>/<model>_<viewtype>.html ...django searches for this covention template

    context_object_name = 'products'  #i dont understand where we defined this 'posts'...eariler home() was being called..there
                                    #'posts' was defined but now when we give route as blog/ it will come diretly to postview class
                                    #we never defining  'posts':Post.objects.all(),.....but still it works
    ordering = ['-date_posted']
    paginate_by=5 #how mnay pages you want to show on home page



def about(request):

  return render(request,'track/about.html',{'title':'about '})#title is optional

def first_view(request):

  return render(request,'track/first_view.html')
def why(request):

  return render(request,'track/why.html')
def benefits(request):

  return render(request,'track/benefits.html')
def announce(request):

  return render(request,'track/announcements.html')

