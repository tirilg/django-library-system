from django.urls import path
from . import views

app_name = 'user_app'

urlpatterns = [
    path("signup/", views.signup, name="signup"), 
    path("login/", views.login, name="login"), 
    path("logout/", views.logout, name="logout"), 
    path("profile/", views.profile, name="profile"),
    path("loan/<str:type>/<int:id>", views.loan_item, name="loan_item"),
    path("return/<str:type>/<int:id>", views.return_item, name="return_item"),
]