from django.urls import path
from task_manager.users import views

urlpatterns = [
    path('', views.UserIndexView.as_view(), name='user_index'),
    path('create/', views.UserFormCreateView.as_view(), name='user_create'), # GET, POST страница регистрации нового пользователя
    path('<int:id>/update/', views.UserFormUpdateView.as_view(), name='user_update'), # GET, POST страница редактирования пользователя
    # path('<int:id>/delete/', views.UserFormDeleteView.as_view(), name='user_delete'), #GET, POST страница удаления пользователя
]