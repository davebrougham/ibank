from django.urls import path
from bank import views

urlpatterns = [
    path(r"", views.ideas, name="ideas"),
    path(r"ideas/", views.ideas, name="ideas"),
    path(r"cleanup/", views.cleanup, name="cleanup"),
    path(r"data/", views.data, name='data'),
    path('update-idea/<int:idea_id>/', views.update_idea, name='update_idea'),
    path('delete-idea/<int:idea_id>/', views.delete_idea, name='delete_idea'),
]
