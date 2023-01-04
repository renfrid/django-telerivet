from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.http import JsonResponse
from .forms import MenuForm
from .models import Keyword, Menu, SubMenu, MenuLink
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages


class MenuListView(generic.ListView):
    model = Menu
    context_object_name = 'menu'
    template_name = 'menu/lists.html'
    paginate_by = 50

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MenuListView, self).dispatch( *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MenuListView, self).get_context_data(**kwargs)
        context['title'] = "Menu"

        keyword = Keyword.objects.all()
        context['keyword'] = keyword

        return context

    def get_queryset(self, *args, **kwargs):
        """Filter data"""
        keyword_id = self.request.GET.get('keyword_id')
        menu = Menu.objects.order_by('keyword__title', 'step')
        if keyword_id:
            menu = menu.filter(keyword_id=keyword_id)

        return menu

class MenuDetailView(generic.DetailView):
    """View menu details"""
    model = Menu
    context_object_name = 'menu'
    template_name = 'menu/detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MenuDetailView, self).dispatch( *args, **kwargs) 

    def get_context_data(self, *args, **kwargs):
        context = super(MenuDetailView, self).get_context_data(**kwargs)
        context['title'] = "Menu"

        sub_menu = SubMenu.objects.filter(menu_id=self.kwargs['pk'])
        context['sub_menu'] = sub_menu
        return context

    def post(self, request, *args, **kwargs):
        menu_id   = kwargs['pk']  
        view_id   = request.POST.get('view_id')    
        sub_menu  = request.POST.get('sub_menu') 

        new_sub_menu           = SubMenu()
        new_sub_menu.menu_id   = menu_id
        new_sub_menu.title     = sub_menu
        new_sub_menu.view_id   = view_id  
        new_sub_menu.save()

        return HttpResponseRedirect(reverse_lazy('setup:detail-menu', kwargs={'pk': menu_id}))


class MenuCreateView(generic.CreateView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MenuCreateView, self).dispatch( *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {'form': MenuForm()}
        return render(request, 'menu/create.html', context)

    def post(self, request, *args, **kwargs):
        form = MenuForm(request.POST)
        if form.is_valid():
            print("reached 2")
            dt_menu = form.save(commit=False)
            dt_menu.created_by = request.user
            dt_menu.save()

            #message
            messages.success(request, 'Menu registered!')

            #redirect
            return HttpResponseRedirect(reverse_lazy('setup:menu'))
        return render(request, 'menu/create.html', {'form': form})  


class MenuUpdateView(generic.UpdateView):
    """View to update a menu"""
    model = Menu
    context_object_name = 'menu'
    form_class = MenuForm
    template_name = 'menu/edit.html'

    def form_valid(self, form):
        response = form.save(commit=False)
        response.updated_by = self.request.user
        response.save()

        #message
        messages.success(self.request, 'Menu information updated!')

        #redirect
        return HttpResponseRedirect(reverse_lazy('setup:menu')) 


class MenuDeleteView(generic.DeleteView):
    """View to delete a menu""" 
    model = Menu
    success_url = reverse_lazy('setup:menu')


class SubMenuDeleteView(generic.DeleteView):
    """View to delete a sub menu""" 
    model = SubMenu
    success_url = reverse_lazy('setup:menu')


class MenuLinkListView(generic.ListView):
    """Menu Links Crud Operation"""
    model = MenuLink
    context_object_name = 'menu_links'
    template_name = 'menu_links/lists.html'
    paginate_by = 50

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MenuLinkListView, self).dispatch( *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MenuLinkListView, self).get_context_data(**kwargs)
        context['title'] = "Menu Links"
        context['keyword'] = Keyword.objects.all()
        context['menu'] = Menu.objects.filter(keyword_id=1).order_by('step')

        return context

    def post(self, request):
        """Posting menu link data"""
        menu_id = request.POST.get('menu_id')
        menu_link_id = request.POST.get('link_id')

        sub_menu_id = None
        if request.POST.get('sub_menu_id') != '':
            sub_menu_id = request.POST.get('sub_menu_id')

        """update or create menu link"""
        menu_link, created = MenuLink.objects.update_or_create(menu_id=menu_id, sub_menu_id=sub_menu_id, link_id=menu_link_id, defaults={})
        
        #message
        messages.success(request, 'Menu link created/update!')

        #redirect
        return HttpResponseRedirect(reverse_lazy('setup:menu-links'))

def get_menu_lists(request, *args, **kwargs):
    if request.method == 'GET':
        keyword_id = kwargs['keyword_id']
        menu = Menu.objects.filter(keyword_id=keyword_id).order_by('step')

        # return response.
        return render(None, 'menu/menu_select.html', {'menu': menu})



def get_sub_menu_lists(request, *args, **kwargs):
    if request.method == 'GET':
        menu_id = kwargs['menu_id']
        sub_menu = SubMenu.objects.filter(menu_id=menu_id)

        # return response.
        return render(None, 'menu/sub_menu.html', {'sub_menu': sub_menu})












