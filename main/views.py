from django.urls import reverse_lazy
from django.views import generic, View
from .forms import RegisterForm
from .models import Document, Organization, Events, CustomUser, Budget, EventAttendance
from django.shortcuts import HttpResponse, get_object_or_404


class HomeView(generic.TemplateView):
    template_name = 'app/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Events.objects.all()
        return context

class ProfileView(generic.TemplateView):
    template_name = 'app/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = EventAttendance.objects.prefetch_related('attendee').all()
        context['total_attends'] = EventAttendance.objects.filter(attendee=self.request.user.pk).count()
        return context

class AttendView(View):
    def get(self, request, pk):
        if pk:
            event_instance = get_object_or_404(Events,pk=pk)
            EventAttendance.objects.create(event=event_instance, attendee=self.request.user)
            print("success")
        return HttpResponse(f'{self.request.user}')

class RegisterView(generic.FormView):
    template_name = 'app/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login_view')
    
    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return super().form_valid(form)
    