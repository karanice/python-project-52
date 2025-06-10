from django.urls import path
from task_manager.users import views

urlpatterns = [
    path('', views.UserIndexView.as_view()),
    # path('create/'), # GET, POST страница регистрации нового пользователя
    # path('<int:pk>/update/'), # GET, POST страница редактирования пользователя
    # path('<int:pk>/delete/'), #GET, POST страница удаления пользователя
]