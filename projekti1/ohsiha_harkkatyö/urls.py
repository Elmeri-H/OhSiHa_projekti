from django.urls import path
from . import views
from .views import list_questions, create_question, update_question, delete_question

urlpatterns = [ 
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('', list_questions, name='list_questions'),
    path('new', create_question, name='create_question'),
    path('update/<int:id>/', update_question, name='update_question'),
    path('delete/<int:id>/', delete_question, name='delete_question'),
]