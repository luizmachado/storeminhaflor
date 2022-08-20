from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.ListProducts.as_view(), name='list'),
    path('<slug>', views.DetailProducts.as_view(), name='detail'),
    path('addcart/', views.AddCart.as_view(), name='addcart'),
    path('removefromcart/', views.RemoveFromCart.as_view(), name='removefromcart'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('ordersummary/', views.OrderSummary.as_view(), name='ordersummary'),
    path('search/', views.ProductSearch.as_view(), name='search'),
]
