from django.urls import path
from . import views
from .views import home, create_spot, update_spot, delete_spot, show_chart1, show_chart2, show_chart3

urlpatterns = [ 
    path('signup/', views.SignUp, name='signup'),
    path('', home, name='home'),
    path('new', create_spot, name='create_spot'),
    path('update/<int:id>/', update_spot, name='update_spot'),
    path('delete/<int:id>/', delete_spot, name='delete_spot'),
    path('chart1', show_chart1, name='show_chart1'),
    path('chart2', show_chart2, name='show_chart2'),
    path('chart3', show_chart3, name='show_chart3'),
]