from django.urls import path

from customer.views import CreateCustomer
from . import views


app_name = 'order'

urlpatterns = [
    path('', views.PayOrder.as_view(), name='pay'),
    path('close', views.CloseOrder.as_view(), name='close'),
    path('detail/<int:pk>', views.DetailOrder.as_view(), name='detail'),
]