from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns=[
    path('list/',views.prdlist,name='prdlist'),
    path('',views.home,name='home'),
    path('auth/',views.auth,name='auth'),
    path('logout/', LogoutView.as_view(next_page='auth'), name='u_logout'),
]