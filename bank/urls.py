from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from . import auth_views
from django.contrib.auth import views as django_auth_views

urlpatterns = [
    path('', views.home, name='home'), 
    path('dashboard/', login_required(views.dashboard), name='dashboard'),
    path('create/', views.create, name='create'),
    path('update-idea/<int:idea_id>/', views.update_idea, name='update_idea'),
    path('delete-idea/<int:idea_id>/', views.delete_idea, name='delete_idea'),
    path('idea/<int:idea_id>/', views.idea_detail, name='idea_detail'),
    path('update-idea-order/', views.update_idea_order, name='update_idea_order'),
    path('label/<str:label_name>/', views.label_ideas, name='label_ideas'),
    path('register/', auth_views.register_view, name='register'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('generate-name/<int:idea_id>/', views.generate_name, name='generate_name'),
    path('generate-plan/<int:idea_id>/', views.generate_plan, name='generate_plan'),
    path('landing/', views.landing_page, name='landing_page'),
    path('forgot-password/', auth_views.forgot_password_view, name='forgot_password'),
    path('reset/<uidb64>/<token>/', django_auth_views.PasswordResetConfirmView.as_view(template_name='reset_password_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', django_auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'), name='password_reset_complete'),
   
]
