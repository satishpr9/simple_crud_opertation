from apps import views
from django.urls import path


urlpatterns=[
    path("",views.index,name="index"),
    #authentication
    path('register/', views.register, name="register"),
    path("login/",views.login_request, name="login"),
    path("logout/",views.logout_request, name="logout"),
    path("category",views.category,name="category"),
    path("delete/<str:id>/",views.delete, name="delete"),
    path('<str:username>',views.profile, name="profile"),
    path("update_profile/",views.update_profile, name="updateprofile"),

    #payment
    path('paynow/', views.homepage, name='paynow'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    
]