from django.views import generic
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.core.urlresolvers import reverse_lazy
from .models import Album
from django.contrib.auth import authenticate,login
from forms import UserForm
from django.shortcuts import render,redirect
from django.views.generic import View

class IndexView(generic.ListView):
    context_object_name = 'all_album'
    template_name = 'music/index.html'

    def get_queryset(self):
        return Album.objects.all()

class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'

class AlbumCreate(CreateView):
    model = Album
    fields = ['artist','album_title','genre','album_logo']


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist','album_title','genre','album_logo']


class AlbumDelete(DeleteView):
    model = Album
    success_url=reverse_lazy('music:index')

class UserForm(View):
    form_class=UserForm
    template_name='music/registration_form.html'

    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            #normalized
            user=form.save(commit=False)
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user.set_password(password)
            user.save()
            #authenticate
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('music:index')
        return render(request,self.template_name,{'form':form})
