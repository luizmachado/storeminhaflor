from django.urls import path
from . import views


app_name = 'order'

urlpatterns = [
    path('pay/<int:pk>', views.PayOrder.as_view(), name='pay'),
    path('saveorder/', views.SaveOrder.as_view(), name='saveorder'),
    path('list/', views.ListOrder.as_view(), name='list'),
    path('detail/<int:pk>', views.DetailOrder.as_view(), name='detail'),
]