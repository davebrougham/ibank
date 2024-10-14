from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from . import auth_views

urlpatterns = [
    path('', views.home, name='home'),  # New home view
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
]
