from django.contrib.messages.api import error
from django.urls import path
from .views import *

urlpatterns = [
    path("",home,name='HOME'),
    path("login/",login_user,name='LOGIN'),
    path("register/",register,name='REGISTER'),
    path('logout/',logout_user,name='LOGOUT'),
    path("tokensend/",token_send,name='TOKENSEND'),
    path("success/",success,name='SUCCESS'),
    path("verify/<auth_token>",verify,name='VERIFY'),
    path("error/",error_page,name='ERROR'),
]