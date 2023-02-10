from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from datetime import datetime 
from apps.citizen.models import Citizen
from django.contrib.auth.models import User, Group


# Create your views here.
@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    template_name = 'dashboard.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DashboardView, self).dispatch( *args, **kwargs)

    def get(self, request):
        """user creation"""
        citizens = Citizen.objects.filter(status='VERIFIED',is_active=1)

        for val in citizens:
            name = val.name
            unique_id = val.unique_id 
            password = val.password

            """create user before update citizen"""
            arr_name = name.split(' ', maxsplit=2)
            first_name = arr_name[0]
            last_name = arr_name[1]
            email = f'{first_name.lower()}@jinadi.co.tz'

            """default role"""
            role = Group.objects.get(name='citizen')

            """register user"""
            user = User.objects.create_user(username=unique_id, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = False
            user.groups.add(role)
            user.save()

            """update citizen"""
            Citizen.objects.filter(id=val.id).update(user_id=user.id)


        citizen = Citizen.objects.filter(designation="MWANANCHI")

        """Filter per status"""
        total = citizen.count()
        verified = citizen.filter(status="VERIFIED").count()
        unverified = citizen.filter(status="UNVERIFIED").count()
        pending = citizen.filter(status="PENDING").count()
                
        #context
        context = {
            'total' : total,
            'verified': verified,
            'unverified': unverified,
            'pending': pending
        }

        """ render view """
        return render(request, self.template_name, context)