
from django.views.generic import TemplateView

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from .models import Album, Photo, UserProfile, OnePhoto
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

import json


# views.py
# view

from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Album, Photo, OnePhoto

@method_decorator(csrf_exempt, name='dispatch')
class AlbumsPage(TemplateView):
    template_name = 'albums.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from datetime import datetime
        current_year = datetime.now().year
        context['years'] = range(current_year, 1900, -1) 
        context['albums'] = Album.objects.filter(user = self.request.user).order_by('-year')
        context['one_photo'] = OnePhoto.objects.filter(user = self.request.user).order_by('-id').first()
        return context

    def post(self, request, *args, **kwargs):
        if 'delete_album' in request.POST:
            album_id = request.POST.get('delete_album')
            Album.objects.filter(id=album_id).delete()
            print("deleted")

        # elif 'toggle_visibility' in request.POST:
        #     album_id = request.POST.get('toggle_visibility')
        #     album = get_object_or_404(Album, id=album_id)
        #     album.is_hidden = True
        #     album.save()
        #     print("Not hidden") 
        elif 'delete_photo' in request.POST:
            photo_id = request.POST.get('photo_id')
            photo = get_object_or_404(Photo, id=photo_id)
            photo.delete()
        
        elif 'delete_one_photo' in request.POST:
            one_photo_id = request.POST.get('one_photo_id')
            one_photo = get_object_or_404(OnePhoto, id=one_photo_id)
            one_photo.delete()
      
            
        elif 'photo' in request.FILES:
            photos = request.FILES.getlist('photo')
            album_id = request.POST.get('album_id')
           
            print(photos)

            for photo_file in photos:
                if album_id and photo_file:
                    album = get_object_or_404(Album, id=album_id)
                    Photo.objects.create(album=album, image=photo_file)
             


        elif 'one_photo' in request.FILES:
            one_photo = request.FILES.get('one_photo')
            OnePhoto.objects.create(user = self.request.user, photo=one_photo)


        else:
           
            album_id = request.POST.get('album_id') 
            name = request.POST.get('album_name')
            theme = request.POST.get('album_theme')
            year = request.POST.get('album_year')

            if name and theme and year:
                if album_id:
                   
                    album = get_object_or_404(Album, id=album_id)
                    album.name = name
                    album.theme = theme
                    album.year = int(year)
                    album.save()
                else:
                    
                    Album.objects.create(user = self.request.user, name=name, theme=theme, year=int(year))

        return redirect('albums')







class PersonalInfoPage(LoginRequiredMixin, TemplateView):
    template_name = 'personal_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['user'] = user
        try:
            profile = user.profile
            context['avatar'] = profile.avatar  # Теперь доступно как {{ avatar.url }}
        except UserProfile.DoesNotExist:
            context['avatar'] = None  # Чтобы избежать ошибки в шаблоне

        return context





@method_decorator(login_required, name='dispatch')
class UpdateUserInfoView(View):
    def post(self, request):
        user = request.user
        updated = False
        avatar_url = None

        data = request.POST

        # Обновляем поля пользователя, если они есть в POST
        for field in ['first_name', 'last_name', 'email', 'username']:
            if field in data and getattr(user, field) != data[field]:
                setattr(user, field, data[field])
                updated = True

        # Если есть аватар в файлах — обновляем
        if 'avatar' in request.FILES:
            avatar_file = request.FILES['avatar']
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.avatar = avatar_file
            try:
                profile.save()
                avatar_url = profile.avatar.url
                updated = True
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Помилка збереження аватару: {str(e)}'}, status=500)

        if updated:
            try:
                user.save()
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Помилка збереження користувача: {str(e)}'}, status=500)

            response = {
                'status': 'success',
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'email': user.email,
            }
            if avatar_url:
                response['avatar_url'] = avatar_url

            return JsonResponse(response)

        return JsonResponse({'status': 'error', 'message': 'Немає змін для оновлення'}, status=400)
