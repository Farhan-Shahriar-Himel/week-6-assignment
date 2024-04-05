from django.urls import path 
from . import views

urlpatterns = [
    path('registration/', views.registrationClass.as_view(), name='registration'),
    path('login/', views.LoginClass.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.ProfileClass.as_view(), name='profile'),
    path('edit_profile/<int:pk>/', views.EditProfileClass.as_view(), name='edit_profile'),
    path('change_pass/', views.ChangePassClass.as_view(), name="change_pass"),
    path('deposit/', views.deposit.as_view(), name='deposit'),
    path('withdraw/', views.withdraw.as_view(), name='withdraw'),
    path('return_book/<int:id>', views.return_book, name='return_book'),
]
