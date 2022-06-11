from django.urls import path
from . import views



app_name = 'customer'

urlpatterns = [
    path('', views.CreateCustomer.as_view(), name='create'),
    path('update/', views.UpdateCustomer.as_view(), name='update'),
    path('login/', views.LoginCustomer.as_view(), name='login'),
    path('logout/', views.LogoutCustomer.as_view(), name='logout'),
]