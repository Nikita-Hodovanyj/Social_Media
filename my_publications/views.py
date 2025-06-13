from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post, Image
from .forms import PublicationForm
from settings_page.models import UserProfile

class PublicationsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "publications.html"
    context_object_name = "all_posts"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PublicationForm()
        user = self.request.user
        context['show_modal'] = not (user.first_name and user.last_name and user.username)

        try:
            context['avatar'] = user.profile.avatar if user.profile.avatar else None
        except UserProfile.DoesNotExist:
            context['avatar'] = None
        return context

class CreatePublicationView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PublicationForm
    success_url = reverse_lazy('publications')

    def form_valid(self, form):
        form.instance.author = self.request.user
        responce = super().form_valid(form)
        images = self.request.FILES.getlist('images')

        for image in images:
            Image.objects.create(post = form.instance, image = image)

        return responce



class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('publications')

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PublicationForm
    success_url = reverse_lazy('publications')

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)