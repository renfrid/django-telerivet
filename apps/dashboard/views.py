from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from datetime import datetime 
from apps.citizen.models import Citizen


# Create your views here.
@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    template_name = 'dashboard.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DashboardView, self).dispatch( *args, **kwargs)

    def get(self, request):
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