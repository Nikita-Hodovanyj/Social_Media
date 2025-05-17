from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import PublicationForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.http import Http404
class PublicationsView(ListView):
    model = Post
    template_name = "publications.html"
    context_object_name = "all_posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PublicationForm()
        return context

class CreatePublicationView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PublicationForm
    template_name = "publications.html"
    success_url = reverse_lazy('publications')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('publications')

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Http404:
            print(f"Post with pk={kwargs['pk']} not found for user {request.user}")
            raise