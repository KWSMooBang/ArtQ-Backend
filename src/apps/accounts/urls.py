from django.urls import path
from .views import RegistrationView, LoginView


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LoginView.as_view(), name='logout'),  # Placeholder for logout view
]