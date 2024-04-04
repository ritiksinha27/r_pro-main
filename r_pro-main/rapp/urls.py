from django.urls import path
from rapp.views import *

urlpatterns = [
    path("", home, name='home'),
    path('about_us/',about_us,name='about_us'),
    path('causes/',causes,name='causes'),
    path('que/',depressionque,name='depressionque'),
    path('faq/',faq,name='faq'),
    path('information/',information,name='information'),
    path('lifestyle_changes/',lifestyle_changes,name='lifestyle'),
    path('result/',result,name='result'),
    # path('symp/',symptoms,name='symptoms'),
    path('calming_video/',calming_video,name='calming_video'),
    
    path('login/',login_user, name='login'), # url for login
    path('logout/',logout_user, name='logout'),
    path('register/',register_user, name='register'),
]
