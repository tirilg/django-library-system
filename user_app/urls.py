from django.urls import path
from . import views

app_name = 'user_app'

urlpatterns = [
    path("", views.login, name="login"), 
    path("signup/", views.signup, name="signup"), 
    path("change_password/", views.change_password, name="change_password"), 
    path("logout/", views.logout, name="logout"), 
    path('delete_account', views.delete_account, name="delete_account"),
    path("profile/", views.profile, name="profile"),
    path("admin/", views.admin, name="admin"),
    path("loan/<str:type>/<int:id>", views.loan_item, name="loan_item"),
    path("return/<str:type>/<int:id>", views.return_item, name="return_item"),
]