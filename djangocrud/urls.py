from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.singout, name='logout'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    path('signin/', views.signin, name='signin'),
    path('task/create/', views.createTask, name='create_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/complete', views.task_complete, name='task_complete'),
    path('task/<int:task_id>/delete', views.task_delete, name='task_delete'),
]
