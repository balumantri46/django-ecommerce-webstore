from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('list/',views.prdlist,name='prdlist'),
    path('',views.home,name='home'),
    path('auth/',views.auth,name='auth'),
    path('logout/', LogoutView.as_view(next_page='auth'), name='u_logout'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/', views.product_list, name='product_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)