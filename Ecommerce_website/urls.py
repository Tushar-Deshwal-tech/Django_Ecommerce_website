from django.urls import path
from Ecommerce_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/<str:category>', views.products, name='products'),
    path('products/<str:category>/<int:id>/', views.item, name='item'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<str:category>/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<str:category>/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('add_cart_from_wishlist/<str:category>/<int:id>/', views.add_cart_from_wishlist, name='add_cart_from_wishlist'),
    path('remove_from_cart/<str:category>/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove_from_wishlist/<str:category>/<int:id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('orders/', views.orders, name='orders'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('login_page/', views.login_page, name='login_page'),
    path('login_verify/', views.login_verify, name='login_verify'),
    path('signup_page/', views.signup_page, name='signup_page'),
    path('signup_user/', views.signup_user, name='signup_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('review/', views.review, name='review'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('edit_page/', views.edit_page, name='edit_page'),
    path('show_products/<str:category>', views.show_products, name='show_products'),
    path('user_page/', views.user_page, name='user_page'),
    path('delete_user/<int:userid>/', views.delete_user, name='delete_user'),
]
