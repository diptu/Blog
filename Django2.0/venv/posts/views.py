
import urllib.parse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import PostForm
from django.utils import timezone
from .models import Post

from .forms import PostForm
from django.views.generic.edit import FormView

from django.views.generic.edit import CreateView ,UpdateView , DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout


class PostDelete(LoginRequiredMixin ,DeleteView):
    model   =   Post
    success_url = '/posts/'

class PostUpdate(SuccessMessageMixin,LoginRequiredMixin ,UpdateView):
    model   =   Post
    success_url = '/posts/'
    success_message = "post  has been updeted successfully"
    fields  =   ['title','content','image','draft','publish']
    template_name_suffix    =   '_update_form'

    #success_url = '/posts/'
    def get_success_url(self):
        slug = self.object.slug
        #print(id)
        success_url = '/posts/'+str(slug)+'/'

        return  success_url



class PostCreate(SuccessMessageMixin,LoginRequiredMixin ,CreateView):
    model = Post
    fields = ['title','content','image','draft','publish']
    success_url = '/posts/'
    success_message = "%(title)s was created successfully"



class PostListView(ListView):
    model   =   Post
    paginate_by = 2

    # def get_queryset_filters(self):
    #     filters = {}
    #     if not self.request.user.is_superuser:
    #         print("not super user")
    #     return filters
    def get_context_data(self, *args , **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'for_superuser_posts': Post.objects.all().filter(draft=True),
            'now'      :    timezone.now(),
            'older_filter': Post.objects.all().filter(publish__year__lte="2017"),
            'year_wise_filter': Post.objects.all().filter(publish__year=timezone.now().year),
            'month_wise_filter': Post.objects.all().filter(publish__year=timezone.now().year).filter(publish__month=timezone.now().month),
        })

        return context

class PostDetailView(DetailView):
    model = Post
    def get_context_data(self, *args , **kwargs):
        #print(self.request.user)
        share_string= self.object.content
        context = super().get_context_data(**kwargs)

        context['now'] = timezone.now()
        context['share_string'] = urllib.parse.quote(share_string, safe='')
        print(context['share_string'])
        return context
