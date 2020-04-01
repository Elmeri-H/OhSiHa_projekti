from django.urls import path
from . import views
from .views import home, create_spot, update_spot, delete_spot

urlpatterns = [ 
    path('signup/', views.SignUp, name='signup'),
    path('', home, name='home'),
    path('new', create_spot, name='create_spot'),
    path('update/<int:id>/', update_spot, name='update_spot'),
    path('delete/<int:id>/', delete_spot, name='delete_spot'),
]