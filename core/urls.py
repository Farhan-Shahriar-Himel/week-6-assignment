from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('<slug:slug>/', views.home, name='homepage_with_slug'),
    path('details/<int:pk>/', views.detailsShow, name='details'),
    path('account/', include('account.urls')),
    path('borrowed/<int:id>/', views.borrowed, name='borrowed'),
]
