from django.views.generic import ListView
from django.shortcuts import redirect
from .forms import ModalActionForm
from my_publications.models import Post
from django.contrib.auth.models import User
from django.contrib import messages

class HomePageView(ListView):
    model = Post
    template_name = "home.html"
    context_object_name = "all_posts"

    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = kwargs.get('form') or ModalActionForm()
        context['form'] = form

        user = self.request.user
        context['show_modal'] = not (user.first_name and user.last_name and user.username)
        return context

    
    def post(self, request, *args, **kwargs):
        form = ModalActionForm(request.POST)
        if form.is_valid():
            user = request.user
            new_username = form.cleaned_data['login']

            #
            if User.objects.exclude(pk=user.pk).filter(username=new_username).exists():
                form.add_error('login', 'Цей логін вже зайнятий. Виберіть інший.')
                return self.get(request, *args, form=form)

            user.first_name = form.cleaned_data['name']
            user.last_name = form.cleaned_data['surname']
            user.username = new_username
            user.save()
            return redirect('home')

        return self.get(request, *args, form=form)

