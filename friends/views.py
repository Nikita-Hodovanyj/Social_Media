from django.views.generic import ListView,DetailView
from django.contrib.auth.models import User
from settings_page.models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from my_publications.models import Post, Image
from my_publications.forms import PublicationForm

class FriendsView(ListView):
    template_name = "friends.html"
    model = User
    context_object_name = "persons"
    
    def get_queryset(self):
        return User.objects.exclude(pk=self.request.user.pk)
    
class UserProfileView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "user_prof.html"
    context_object_name = "all_posts"

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return Post.objects.filter(author_id=user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['pk']
        context['person'] = User.objects.get(pk=user_id)
        context['form'] = PublicationForm()
        user = self.request.user
        context['show_modal'] = not (user.first_name and user.last_name and user.username)

        try:
            context['avatar'] = user.profile.avatar if user.profile.avatar else None
        except UserProfile.DoesNotExist:
            context['avatar'] = None
        return context