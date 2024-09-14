from django.urls import path
from bank import views

urlpatterns = [
    path(r"", views.dashboard, name="dashboard"),
    path(r"dashboard/", views.dashboard, name="dashboard"),
    path(r"workshop/", views.workshop, name="workshop"),
    path(r"create/", views.create, name='create'),
    path('update-idea/<int:idea_id>/', views.update_idea, name='update_idea'),
    path('delete-idea/<int:idea_id>/', views.delete_idea, name='delete_idea'),
]
