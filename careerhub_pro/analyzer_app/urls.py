from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('base/', views.base, name='base'),

    # Auth routes
    path('login/', views.login_view, name='login'),  
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),

    # Resume upload & report
    path('upload/', views.upload_resume, name='upload_resume'),
    path('success/', views.resume_success, name='resume_success'),
    path('report/<int:resume_id>/', views.resume_report, name='resume_report'),
]
