from django.urls import path,include
from Guest import views
app_name="Guest"

urlpatterns = [
    path('Registration/', views.Registration, name='Registration'),
    path('recognize/', views.recognize, name='recognize'),
    path('data/', views.data, name='data'),
    path('whole/', views.whole, name='whole'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
]

