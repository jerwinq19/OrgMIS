from django.urls import path
from . import views


urlpatterns = [
    path('organization/', views.OrganizationView.as_view(), name="org_view")
]
