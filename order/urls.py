from django.urls import path

from customer.views import CreateCustomer
from . import views


app_name = 'order'

urlpatterns = [
    path('', views.PayOrder.as_view(), name='pay'),
    path('saveorder', views.SaveOrder.as_view(), name='saveorder'),
    path('detail/<int:pk>', views.DetailOrder.as_view(), name='detail'),
]