from django.urls import path
from .views import TodoListCreate, TodoRetrieveUpdateDestroy, TodoToggleComplete, signup, login

urlpatterns = [
    path('todos/', TodoListCreate.as_view(), name='todo_list'),
    path('todos/<int:pk>/', TodoRetrieveUpdateDestroy.as_view(), name='todo_detail'),
    path('todos/<int:pk>/complete/', TodoToggleComplete.as_view(), name='todo_complete'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
]
