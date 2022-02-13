
from .import views
from django.contrib.auth import views as auth_views
from django.urls import path,include
from django.conf.urls.static  import static
from django.conf  import settings
urlpatterns = [
    path('',views.home,name='home' ),
    path('supplier_register/',views.supplier_register,name='supplier_register' ),
    path('supplier_profile/',views.supplier_profile,name='supplier_profile' ),
    path('supplier_login/',views.supplier_login,name='supplier_login' ),
    path('post_deal/',views.post_deal,name='deal_post' ),
    path('showdeal/<str:sid>',views.showdeal,name='showdeal' ),
    path('add_to_cart/<int:deal_id>/', views.add_to_cart, name='add_to_cart'),
    path('editdeal/<int:id>/', views.edit_deal, name='edit_deal'),
    path('checkout/<int:amount>/',views.checkout,name='checkout'),
    path('cart/', views.cart, name='cart'),
    path('uprofile/', views.uprofile, name='uprofile'),
    path('myposteddeals/', views.myposteddeals, name='myposteddeals'),
    path('searchbyloc/', views.searchbyloc, name='searchbyloc'),
    path('changepassword/', views.change_pass, name='change_pass'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.register, name='register'),
    path('paymenthistory/', views.paymenthistory, name='paymenthistory'),
    path('dealbycat/<int:id>/', views.dealbycat, name='dealbycat'),
    path('cart/delete/', views.cart_delete, name='cart_delete'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
