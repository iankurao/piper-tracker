from django.urls import path
from . import views
from .views import (ProductListView,
                    # ProductCreateView,
                    # ProductUpdateView,
                    # ProductDeleteView,
                    # UserProductListView,
                    )

urlpatterns = [
    path('',views.first_view,name='track-home'),
    path('all/', ProductListView.as_view(), name='track-list-all-products'),
    path('WhyToUse/', views.why, name='track-why'),
    path('benefits/', views.benefits, name='track-benefits'),
    path('announcements/', views.announce, name='track-announcements'),
    path('about/', views.about,name="track-about"),
]