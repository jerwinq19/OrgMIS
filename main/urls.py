from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # auth login
    path('', LoginView.as_view(template_name="app/login.html"), name="login_view"),
    path('register/', views.RegisterView.as_view(), name="register_view"),
    path('logout/', LogoutView.as_view(next_page="login_view"), name="logout_view"),
    
    # operations
    path('attend/<int:pk>/', views.AttendView.as_view(), name="attend_view"),
    
    
    # pages view
    path('home/', views.HomeView.as_view(), name="home_view"),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name="profile")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)