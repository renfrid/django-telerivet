from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from datetime import datetime 


# Create your views here.
@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    template_name = 'dashboard.html'

    def get(self, request):
        if request.GET.get("year") is not None:
            year = request.GET.get("year")
        else:
            year = "Overall"
            
        #context
        context = {"cur_year": year}

        date_str = '08/11/1987'

        date_object = datetime.strptime(date_str, '%d/%m/%Y').date()
        print(type(date_object))
        print(date_object)  # printed in default formatting

        """ render view """
        return render(request, self.template_name, context)