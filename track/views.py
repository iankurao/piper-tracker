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
from pricetracker import settings
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
    paginate_by=5 #how manyy pages you want to show on home page



class ProductCreateView(LoginRequiredMixin,CreateView):#<app>/<model>_form.html ....this view follow this convention
                                                    #LoginRequiredMixin this is written bcoz user will see post form only if he
                                                    #logged in otherwise if he try toa access that route blog/post/new then it will ask
                                                    #for login first
                                                    #we have done this ealier while showing profile and we had used decorators there..
                                                    #e cant use decorators with functions so we used it
    model = Product


    fields = ['product_url','desire_price']#this fields should be in your model Post
    context={

      'products':Product.objects.all(),
      'title':'Home'
    }

    def form_valid(self, form):
      f=self.new_product(form)
      if f==1:
          messages.success(self.request, f'Product Added successfully! We will notify you via email when price drop under your desire price')
          return HttpResponseRedirect(reverse('user-products', args=[self.request.user.username]))
      if f==0:
          messages.warning(self.request, f"Invalid URL or couldn't find proper price of product..try again")
          return HttpResponseRedirect(reverse('user-products', args=[self.request.user.username]))


     
    def new_product(self,form):

        from django.http import JsonResponse
        from django.views.decorators.csrf import csrf_exempt
        from scrapyd_api import ScrapydAPI
        from uuid import uuid4
        import time


        import sys
        #this path will remain in sys.path untill this program terminated
        sys.path.append("/app")
        sys.path.append("/app/scrapyproject")#in heroku we have base dir as /app
        sys.path.append("C:/Users/ian/Home/Documents/Django/piper-tracker/scrapyproject/scrapyproject")#for testing in my local
                                                                                   #system
         #this path will be used in scrapyproject.items,
        from scrapyproject.scrapyproject.spiders import autoscrap
        from scrapyproject.scrapyproject.pipelines import ScrapyprojectPipeline
        from scrapy import signals
        from twisted.internet import reactor
        from scrapy.crawler import Crawler,CrawlerRunner,CrawlerProcess
        from scrapy.settings import Settings
        from scrapy.utils.project import get_project_settings

        from crochet import setup#added this2 lines and removed reactor.run() and reacter().stop()
                              #since it was throwing error"Reactor not Restartable"after 2nd submission from
                              #front end...first submission works but when we do 2nd then reactor is already
                              #strated in first so you cant start it again since there is only one reactor in system


        #print(self.request.POST)





        setup()
        print('hello'*10)

        if form==-1:

          url=self.product_url

          settings = {
                  'url':url,
                  'USER_AGENT': 'scrapyproject (+http://www.yourdomain.com)',
                  'timepass':'kya chal raha hai bhai'
              }

          def spider_closing(spider):
              """Activates on spider closed signal"""
              print("Spiderclose"*10)
              #reactor.stop()

          crawler = Crawler(autoscrap.AutoScrap,settings)

          crawler.signals.connect(spider_closing, signal=signals.spider_closed)

          p_obj=self

          crawler.crawl(product_object=p_obj,check=1)

          while True:
                time.sleep(1)
                #print(crawler.stats.get_stats())
                try:
                  fr=crawler.stats.get_stats()['finish_reason']
                  if fr=='finished':
                    break
                except:
                  pass



        else:
          print("we are in else part")
          url = self.request.POST['product_url']
          d_price = self.request.POST['desire_price']


          settings = {
                  'url':url,
                  'USER_AGENT': 'scrapyproject (+http://www.yourdomain.com)',
                  'timepass':'kya chal raha hai bhai'
              }





          def spider_closing(spider):
              """Activates on spider closed signal"""
              print("Spiderclose"*10)
              #import sys        #here as well, we can see both path on terminal added to sys.path ,
                                 #we added both in track.views.it will remain untill program terminated.
              #print(sys.path)
              #reactor.stop()
          def if_spyder_open(spider):
            print("spyderOpen__"*10)

          u=self.request.user
          ulen1=len(u.product_set.all())

          crawler = Crawler(autoscrap.AutoScrap,settings)


          crawler.signals.connect(spider_closing, signal=signals.spider_closed)
          crawler.signals.connect(if_spyder_open,signal=signals.spider_opened)

          crawler.crawl(url=url,d_price=d_price,author=self.request.user,check=0,timepass='whats up..!!')


        #reactor.run()

          while True:
                print(crawler.stats.get_stats())
                time.sleep(1)
                #print(crawler.stats.get_stats())
                try:
                  fr=crawler.stats.get_stats()['finish_reason']
                  if fr=='finished':
                    break
                except:
                  pass
          ulen2=len(u.product_set.all()) #users total number of products in data base will increase here
                                         #after saving prodcut in database in pipeline.py
          if ulen2>ulen1:
             return 1
          elif ulen2==ulen1: #if it is remain equal it means something went wrong...either no proper price found
                                #or no proper url ..no proper price....then product will not store in database
                                #in pipeline.py
             return 0     



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



class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['title','desire_price']
    template_name = 'track/update_form.html'

    def form_valid(self, form):
        messages.success(self.request, f'Updated successfully!')
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):#this fucntion restric user to update others post..he can update only his own post not others
                        #UserPassesTestMixin thats why we write this
        product = self.get_object()
        if self.request.user == product.author:
            return True
        return False


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class UserProductListView(ListView):#when we click on title tis executed
    model = Product
    template_name = 'track/user_products.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))#this will get username presnet in
                                                                            #kwargs which is being
                                                                            #being passed from our route..if user is
                                                                            #not valid then error 404

        return Product.objects.filter(author=user).order_by('-date_posted')
