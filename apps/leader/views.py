from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.http import JsonResponse
from apps.account.models import Profile
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from .forms import LeaderForm


class LeaderListView(generic.ListView):
    model = Profile
    context_object_name = 'leader'
    template_name = 'leaders/lists.html'
    paginate_by = 50

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LeaderListView, self).dispatch( *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(LeaderListView, self).get_context_data(**kwargs)
        context['title'] = "Leaders"

        return context

    def get_queryset(self, *args, **kwargs):
        leaders = Profile.objects.filter(Q(designation=2) | Q(designation=3) | Q(designation=4)).order_by('id')

        return leaders


class LeaderDetailView(generic.DetailView):
    """View to update a details"""

class LeaderCreateView(generic.CreateView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LeaderCreateView, self).dispatch( *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {'form': LeaderForm()}
        return render(request, 'leaders/create.html', context)

    def post(self, request, *args, **kwargs):
        form = LeaderForm(request.POST)
        print("reaches here")
        if form.is_valid():
            print("reaches here 1")
            print(form)

            # dt_menu = form.save(commit=False)
            # dt_menu.created_by = request.user
            # dt_menu.save()

            #message
            messages.success(request, 'Leader registered!')

            #redirect
            return HttpResponseRedirect(reverse_lazy('leader:lists'))
        return render(request, 'leaders/create.html', {'form': form})  


class MenuUpdateView(generic.UpdateView):
    """View to update a film"""

class MenuDeleteView(generic.DeleteView):
    """View to delete a film"""  
