from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from payments.models import Payment


class HomeView(TemplateView):
    template_name = 'core/index.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get recent payments for the user
        context['recent_payments'] = Payment.objects.filter(user=self.request.user)[:5]
        return context