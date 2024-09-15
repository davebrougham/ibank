from django.urls import path
from . import views

urlpatterns = [
    path(r"", views.dashboard, name="dashboard"),
    path(r"dashboard/", views.dashboard, name="dashboard"),
    path(r"workshop/", views.workshop, name="workshop"),
    path(r"create/", views.create, name='create'),
    path('update-idea/<int:idea_id>/', views.update_idea, name='update_idea'),
    path('delete-idea/<int:idea_id>/', views.delete_idea, name='delete_idea'),
    path('idea/<int:idea_id>/', views.idea_detail, name='idea_detail'),
    # path('idea/<int:idea_id>/add-link/', views.add_link, name='add_link'),
    # path('delete-link/<int:link_id>/', views.delete_link, name='delete_link'),
    # path('update-notes/<int:idea_id>/', views.update_notes, name='update_notes'),
]
