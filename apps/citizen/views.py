from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from apps.api.registration import RegistrationWrapper
from apps.location.models import *
from .models import Citizen
from .forms import CitizenForm


class CitizenListView(generic.ListView):
    model = Citizen
    context_object_name = 'citizens'
    template_name = 'citizens/lists.html'
    paginate_by = 50

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CitizenListView, self).dispatch( *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(CitizenListView, self).get_context_data(**kwargs)
        context['title'] = "Citizen"

        context['wards'] = Ward.objects.all()

        return context

    def get_queryset(self, *args, **kwargs):
        citizens = Citizen.objects.filter(designation="MWANANCHI")

        """get variables"""
        ward_id = self.request.GET.get('ward_id')
        village_id = self.request.GET.get('village_id')
        status = self.request.GET.get('status')
        unique_id = self.request.GET.get('unique_id')

        if ward_id:
            citizens = citizens.filter(ward_id=ward_id)

        if village_id:
            citizens = citizens.filter(village_id=village_id) 

        if status:
            citizens = citizens.filter(status__exact=status) 

        if unique_id:
            citizens = citizens.filter(unique_id__exact=unique_id) 

        citizens = citizens.order_by('id')

        return citizens


class CitizenDetailView(generic.DetailView):
    """View to update a details"""
    model = Citizen
    context_object_name = 'citizen'
    template_name = 'citizens/show.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CitizenDetailView, self).dispatch( *args, **kwargs) 

    def get_context_data(self, *args, **kwargs):
        context = super(CitizenDetailView, self).get_context_data(**kwargs)
        context['title'] = "Citizen"

        citizen = Citizen.objects.get(id=self.kwargs['pk'])
        context['citizen'] = citizen

        return context

    def post(self, request, *args, **kwargs):  
        qry_citizen = Citizen.objects.get(id=kwargs['pk'] )
        qry_citizen.status = request.POST.get('status') 
        qry_citizen.is_active = request.POST.get('is_active') 
        qry_citizen.be_jembe = request.POST.get('be_jembe') 
        qry_citizen.save()

        messages.success(request, 'Citizen status updated!')
        return HttpResponseRedirect(reverse_lazy('citizens:show', kwargs={'pk': kwargs['pk'] }))


class CitizenCreateView(generic.CreateView):
    """Register new citizen"""
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CitizenCreateView, self).dispatch( *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {'form': CitizenForm}
        return render(request, 'citizens/create.html', context)

    def post(self, request, *args, **kwargs):
        form = CitizenForm(request.POST)

        """registration wrapper"""
        formating = RegistrationWrapper()

        if form.is_valid():
            name = request.POST.get('name')
            pin  = formating.generate_pin(pin_size=4)
            phone = formating.format_phone(phone=request.POST.get('phone'))

            """generate unique number"""
            unique_id = formating.generate_unique_id(designation="MWANANCHI")

            """create user before update citizen"""
            arr_name = name.split(' ', maxsplit=2)
            first_name = arr_name[0]
            email = f'{first_name}@jinadi.co.tz'

            """default role"""
            role = Group.objects.get(name='citizen')

            """register user"""
            user = User.objects.create_user(username=unique_id, email=email, password=pin)
            user.first_name = first_name
            user.is_active = True
            user.groups.add(role)
            user.save()

            dt_citizen = form.save(commit=False)
            dt_citizen.user_id      = user.id
            dt_citizen.created_by   = request.user
            dt_citizen.designation  = "MWANANCHI"
            dt_citizen.is_active    = 1
            dt_citizen.status       = 'VERIFIED'
            dt_citizen.password     = pin
            dt_citizen.unique_id    = unique_id
            dt_citizen.phone        = phone
            dt_citizen.save()

            messages.success(request, 'Citizen registered!')
            return HttpResponseRedirect(reverse_lazy('citizens:lists'))
        return render(request, 'citizens/create.html', {'form': form})  

class CitizenUpdateView(generic.UpdateView):
    """Update citizen details"""
    model = Citizen
    context_object_name = 'citizen'
    form_class = CitizenForm
    template_name = 'citizens/edit.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CitizenUpdateView, self).dispatch( *args, **kwargs)

    def form_valid(self, form):
        dt_citizen = form.save(commit=False)
        dt_citizen.updated_by = self.request.user
        dt_citizen.save()

        messages.success(self.request, 'Citizen information updated!')
        return HttpResponseRedirect(reverse_lazy('citizens:lists')) 

class CitizenDeleteView(generic.DeleteView):
    """View to delete a Citizen""" 
    model = Citizen
    template_name = "citizens/confirm_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Citizen deleted successfully")
        return reverse_lazy('citizens:lists')