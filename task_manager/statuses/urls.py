from django.urls import path

from task_manager.statuses import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='status_index'),
    path('create/', views.StatusCreateFormView.as_view(), name='status_create'),
    path('<int:pk>/update/', views.StatusUpdateFormView.as_view(), 
         name='status_update'),
    path('<int:pk>/delete/', views.StatusDeleteFormView.as_view(), 
         name='status_delete'),
    
]