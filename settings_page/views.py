
from django.views.generic import TemplateView

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from .models import Album, Photo
from django.views import View
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

import json

class PersonalInfoPage(TemplateView):
    template_name = 'personal_info.html'




@method_decorator(csrf_exempt, name='dispatch')
class AlbumsPage(TemplateView):
    template_name = 'albums.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from datetime import datetime
        current_year = datetime.now().year
        context['years'] = range(current_year, 1900, -1) 
        context['albums'] = Album.objects.all().order_by('-year')
        return context

    def post(self, request, *args, **kwargs):
        if 'delete_album' in request.POST:
            album_id = request.POST.get('delete_album')
            Album.objects.filter(id=album_id).delete()

        elif 'toggle_visibility' in request.POST:
            album_id = request.POST.get('toggle_visibility')
            album = get_object_or_404(Album, id=album_id)
            album.is_hidden = not album.is_hidden
            album.save()

        elif 'photo' in request.FILES:
            photo_file = request.FILES['photo']
            album_id = request.POST.get('album_id')
            if album_id and photo_file:
                album = get_object_or_404(Album, id=album_id)
                Photo.objects.create(album=album, image=photo_file)

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
                    
                    Album.objects.create(name=name, theme=theme, year=int(year))

        return redirect('albums')


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class UpdateUserInfoView(View):
    def post(self, request):
        data = json.loads(request.body)
        user = request.user
        changed = False

        first_name = data.get('first_name')
        if first_name is not None:
            user.first_name = first_name
            changed = True

        last_name = data.get('last_name')
        if last_name is not None:
            user.last_name = last_name
            changed = True

        email = data.get('email')
        if email is not None:
            user.email = email
            changed = True

        if changed:
            user.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'no_changes'})
