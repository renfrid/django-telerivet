from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.http import JsonResponse
from apps.account.models import Profile
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages


class CitizenListView(generic.ListView):
    model = Profile
    context_object_name = 'citizens'
    template_name = 'citizens/lists.html'
    paginate_by = 50

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CitizenListView, self).dispatch( *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(CitizenListView, self).get_context_data(**kwargs)
        context['title'] = "Citizen"

        return context

    def get_queryset(self, *args, **kwargs):
        citizens = Profile.objects.filter(designation=1).order_by('id')

        return citizens


class CitizenDetailView(generic.DetailView):
    """View to update a details"""
