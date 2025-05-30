from django.views.generic import ListView
from my_publications.models import Post

class HomePageView(ListView):
    model = Post
    template_name = "home.html"
    context_object_name = "all_posts"

    def get_queryset(self):
        return Post.objects.all()