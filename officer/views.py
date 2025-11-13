from django.urls import reverse_lazy
from django.views import generic, View
from main.models import Document, Organization, Events, CustomUser, Budget, EventAttendance
from django.shortcuts import HttpResponse, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone


class OrganizationView(generic.TemplateView):
    template_name = 'officer/Organizer.html'