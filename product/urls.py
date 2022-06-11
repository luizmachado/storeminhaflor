from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.ListProducts.as_view(), name='list'),
    path('<slug>', views.DetailProducts.as_view(), name='detail'),
    path('addcart/', views.AddCart.as_view(), name='addcart'),
    path('removefromcart/', views.RemoveFromCart.as_view(), name='removefromcart'),
    #TODO: analyze if it is the best place, maybe in the order app
    path('cart/', views.Cart.as_view(), name='cart'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
]