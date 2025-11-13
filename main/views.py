from django.urls import reverse_lazy
from django.views import generic, View
from .forms import RegisterForm
from .models import Document, Organization, Events, CustomUser, Budget, EventAttendance
from django.shortcuts import HttpResponse, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone


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
        user = self.request.user

        # All events the user attended
        user_attendances = EventAttendance.objects.filter(attendee=user)
        total_attends = user_attendances.count()

        # Total events overall (for attendance rate)
        total_events = Events.objects.count()
        attendance_rate = (total_attends / total_events * 100) if total_events > 0 else 0

        # Upcoming events (based on date)
        upcoming_events = Events.objects.filter(event_date__gte=timezone.now()).order_by('event_date')[:5]

        # Recent events attended
        recent_attended = user_attendances.select_related('event').order_by('-event__event_date')[:5]

        print(recent_attended)
        
        context.update({
            'total_attends': total_attends,
            'attendance_rate': round(attendance_rate, 1),
            'upcoming_events': upcoming_events,
            'recent_attended': recent_attended,
            'organization': getattr(user.organization, 'org_name', 'No Organization'),
            'user_events': user_attendances, 
        })
        return context


class AttendView(View):
    def get(self, request, pk):
        event_instance = get_object_or_404(Events, pk=pk)
        attendance, created = EventAttendance.objects.get_or_create(
            event=event_instance,
            attendee=request.user
        )

        if created:
            messages.success(request, f"You are now attending {event_instance.event_name}!")
        else:
            messages.info(request, f"You already attended {event_instance.event_name}.")

        return redirect('home_view')

class RegisterView(generic.FormView):
    template_name = 'app/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login_view')
    
    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return super().form_valid(form)
    