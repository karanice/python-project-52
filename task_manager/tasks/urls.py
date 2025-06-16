from django.urls import path

from task_manager.tasks import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='task_index'),
    path('create/', views.TaskCreateFormView.as_view(), name='task_create'),
    path('<int:pk>/update/', views.TaskUpdateFormView.as_view(), 
         name='task_update'),
    path('<int:pk>/delete/', views.TaskDeleteFormView.as_view(), 
         name='task_delete'),
    path('<int:pk>', views.TaskDetailView.as_view(), name='task_detail'),
]