from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from apps.api.registration import RegistrationWrapper
from apps.api.classes import TelerivetWrapper
from .forms import LeaderForm
from apps.citizen.models import Citizen
from apps.location.models import *


class LeaderListView(generic.ListView):
    model = Citizen
    context_object_name = 'leaders'
    template_name = 'leaders/lists.html'
    paginate_by = 50

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LeaderListView, self).dispatch( *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(LeaderListView, self).get_context_data(**kwargs)
        context['title'] = "Leaders"

        context['wards'] = Ward.objects.all()

        return context

    def get_queryset(self, *args, **kwargs):
        leaders = Citizen.objects.filter(Q(designation="MTENDAJI_KATA") | 
            Q(designation="MTENDAJI") | 
            Q(designation="MWENYEKITI") | 
            Q(designation="MJUMBE"))

        """get variables"""
        ward_id = self.request.GET.get('ward_id')
        village_id = self.request.GET.get('village_id')
        designation = self.request.GET.get('designation')
        unique_id = self.request.GET.get('unique_id')

        if ward_id:
            leaders = leaders.filter(ward_id=ward_id)

        if village_id:
            leaders = leaders.filter(village_id=village_id) 

        if designation:
            leaders = leaders.filter(designation__exact=designation) 

        if unique_id:
            leaders = leaders.filter(unique_id__exact=unique_id) 

        leaders = leaders.order_by('id')

        """return leaders"""
        return leaders


class LeaderDetailView(generic.DetailView):
    """View to update a details"""
    model = Citizen
    context_object_name = 'leader'
    template_name = 'leaders/show.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LeaderDetailView, self).dispatch( *args, **kwargs) 

    def get_context_data(self, *args, **kwargs):
        context = super(LeaderDetailView, self).get_context_data(**kwargs)
        context['title'] = "Leaders"

        leader = Citizen.objects.get(id=self.kwargs['pk'])
        context['leader'] = leader

        return context

    def post(self, request, *args, **kwargs):  
        qry_leader = Citizen.objects.get(id=kwargs['pk'] )
        qry_leader.status = request.POST.get('status') 
        qry_leader.is_active = request.POST.get('is_active') 
        qry_leader.save()

        messages.success(request, 'Leader status updated!')
        return HttpResponseRedirect(reverse_lazy('leaders:show', kwargs={'pk': kwargs['pk'] }))


class LeaderCreateView(generic.CreateView):
    """Register new leader"""
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LeaderCreateView, self).dispatch( *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {'form': LeaderForm()}
        return render(request, 'leaders/create.html', context)

    def post(self, request, *args, **kwargs):
        form = LeaderForm(request.POST)

        """registration wrapper"""
        formating = RegistrationWrapper()

        """telerivet wrapper"""
        telerivet = TelerivetWrapper()

        if form.is_valid():
            designation = request.POST.get('designation')
            name = request.POST.get('name')
            pin  = formating.generate_pin(pin_size=4)
            phone = formating.format_phone(phone=request.POST.get('phone'))

            """generate unique number"""
            unique_id = formating.generate_unique_id(designation=designation)

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

            """save POST data"""
            dt_leader = form.save(commit=False)
            dt_leader.user_id   = user.id
            dt_leader.created_by = request.user
            dt_leader.is_active = 1
            dt_leader.status = 'VERIFIED'
            dt_leader.verified_at = datetime.now()
            dt_leader.password = pin
            dt_leader.unique_id = unique_id
            dt_leader.phone = phone
            dt_leader.save()

            """Message to WEO"""
            message_to_weo = "Habari " + name + ", usajili wako umekamilika. Neno siri ni " + pin + "."

            """send message to MWANANCHI"""
            telerivet.send_message(sender=phone, message=message_to_weo)

            messages.success(request, 'New Leader registered!')
            return HttpResponseRedirect(reverse_lazy('leaders:lists'))
        return render(request, 'leaders/create.html', {'form': form})  


class LeaderUpdateView(generic.UpdateView):
    """Update citizen details"""
    model = Citizen
    context_object_name = 'leader'
    form_class = LeaderForm
    template_name = 'leaders/edit.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LeaderUpdateView, self).dispatch( *args, **kwargs)

    def form_valid(self, form):
        """registration wrapper"""
        formating = RegistrationWrapper()

        dt_leader = form.save(commit=False)
        dt_leader.updated_by = self.request.user
        dt_leader.phone = formating.format_phone(phone=self.request.POST.get('phone'))
        dt_leader.save()

        messages.success(self.request, 'Leader information updated!')
        return HttpResponseRedirect(reverse_lazy('leaders:lists')) 

class LeaderDeleteView(generic.DeleteView):
    """View to delete a Citizen""" 
    model = Citizen
    template_name = "leaders/confirm_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Leader deleted successfully")
        return reverse_lazy('leaders:lists') 
