from datetime import datetime
from django.utils import timezone
from social_core.exceptions import AuthForbidden
from django.conf import settings

import requests

from .models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = f"https://api.vk.com/method/users.get?fields=bdate,sex,about,photo_max_orig&access_token={response['access_token']}&v=5.131"
    
    vk_response = requests.get(api_url)

    if vk_response.status_code != 200:
        return

    vk_data = vk_response.json()['response'][0]

    if vk_data['sex']:
        if vk_data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE
        elif vk_data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE

    if vk_data['about']:
        user.shopuserprofile.about_me = vk_data['about']

    if vk_data['bdate']:
        b_date = datetime.strptime(vk_data['bdate'], '%d.%m.%Y').date()
        age = timezone.now().date().year - b_date.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        user.age = age

    if vk_data['photo_max_orig']:
        resp = requests.get(vk_data['photo_max_orig'])
        if resp.status_code == 200:
            file_name = f'users_avatars/{user.email}_avatar.jpg'
            full_file_name = f'media/{file_name}'
            with open(full_file_name, 'wb') as f:
                f.write(resp.content)
            user.avatar = file_name

    user.save()
