
from django.views.generic import TemplateView



class PersonalInfoPage(TemplateView):
    template_name = 'personal_info.html'

class AlbumsPage(TemplateView):
    template_name = 'albums.html'
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

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
