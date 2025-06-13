from django.views.generic import ListView
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import FriendRequest, Friendship
from my_publications.models import Post
from my_publications.forms import PublicationForm
from settings_page.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.db.models import Q
from .models import FriendRequest

class FriendsView(TemplateView):
    template_name = 'friends.html'

    def get_friends_ids(self):
        user = self.request.user
        # Получаем все подтвержденные дружбы, где user — от кого или кому
        friends_qs = FriendRequest.objects.filter(
            (Q(from_user=user) | Q(to_user=user)) & Q(is_accepted=True)
        )
        friend_ids = set()
        for fr in friends_qs:
            if fr.from_user == user:
                friend_ids.add(fr.to_user.id)
            else:
                friend_ids.add(fr.from_user.id)
        return list(friend_ids)

    def get_recommendations(self):
        user = self.request.user
        friends_ids = self.get_friends_ids()
        # Рекомендации — пользователи, кроме текущего и его друзей
        return User.objects.exclude(id__in=friends_ids + [user.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Запросы в друзья, которые пришли текущему пользователю и ещё не приняты
        context['received_requests'] = FriendRequest.objects.filter(
            to_user=user,
            is_accepted=False
        )

        # Список всех друзей
        context['all_friends'] = User.objects.filter(id__in=self.get_friends_ids())

        # Рекомендации друзей
        context['persons'] = self.get_recommendations()

        # Флаг для показа модального окна, если не заполнены обязательные поля
        context['show_modal'] = not (user.first_name and user.last_name and user.username)

        return context

    
    def get_friends_ids(self):
        friends1 = Friendship.objects.filter(
            user1=self.request.user
        ).values_list('user2_id', flat=True)
        
        friends2 = Friendship.objects.filter(
            user2=self.request.user
        ).values_list('user1_id', flat=True)
        
        return list(friends1) + list(friends2)

@login_required
@require_POST
def send_friend_request(request, user_id):
    to_user = User.objects.get(pk=user_id)
    FriendRequest.objects.create(from_user=request.user, to_user=to_user)
    return JsonResponse({'status': 'success'})

@login_required
@require_POST
def accept_request(request, request_id):
    friend_request = FriendRequest.objects.get(
        pk=request_id,
        to_user=request.user,
        is_accepted=False
    )
    friend_request.is_accepted = True
    friend_request.save()
    Friendship.objects.create(
        user1=friend_request.from_user,
        user2=friend_request.to_user
    )
    return JsonResponse({'status': 'success'})

@login_required
@require_POST
def remove_friend(request, friend_id):
    Friendship.objects.filter(
        Q(user1=request.user, user2_id=friend_id) |
        Q(user2=request.user, user1_id=friend_id)
    ).delete()
    return JsonResponse({'status': 'success'})

class UserProfileView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "user_prof.html"
    context_object_name = "all_posts"

    def get_queryset(self):
        return Post.objects.filter(author_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person'] = User.objects.get(pk=self.kwargs['pk'])
        context['form'] = PublicationForm()
        context['is_friend'] = Friendship.objects.filter(
            Q(user1=self.request.user, user2_id=self.kwargs['pk']) |
            Q(user2=self.request.user, user1_id=self.kwargs['pk'])
        ).exists()
        return context