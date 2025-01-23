from django.db.models.base import django
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView
from .models import Property
from django.views.generic.edit import FormMixin
from .Forms import PropertyBookingForm
from .filters import PropertyFilter
from django_filters.views import FilterView
from django.contrib import messages
from django.urls import reverse

# Create your views here.
class PropertyListView(FilterView):
    model = Property 
    # pagination
    paginate_by = 1
    filterset_class = PropertyFilter
    template_name = 'Property/property_list.html'
    
class PropertyDetailView(FormMixin, DetailView):
    model = Property  
    form_class = PropertyBookingForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related"] = Property.objects.filter(Category=self.get_object().Category)[:2]
        return context  
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            myform = form.save(commit=False)
            myform.Property = self.get_object()
            myform.User = request.user
            myform.save()
            
            return redirect('/')
        else:
            print('Not valid')

class NewProperty(CreateView):
    model = Property
    fields = ['Name', 'Description', 'Price', 'Location', 'Main_Image', 'Category']

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            myform = form.save(commit=False)
            myform.owner = request.user
            myform.save()
            messages.success(request, 'Successfully Added Your Property')

            ### send gmail message
            return redirect(reverse('Property:property_list'))