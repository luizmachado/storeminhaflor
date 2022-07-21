from django.urls import path
from . import views


app_name = 'order'

urlpatterns = [
    path('', views.PayOrder.as_view(), name='pay'),
    path('saveorder', views.SaveOrder.as_view(), name='saveorder'),
    path('detail/<int:pk>', views.DetailOrder.as_view(), name='detail'),
]