from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode
from urllib import request

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import UserProfile
from my_shop.settings import BASE_DIR


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    # api_url = f'https://api.vk.com/method/users.get/fields=bdate,sex,about&access_token={response.access_token}'

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_max')),
                                                access_token=response['access_token'],
                                                v='5.92')),
                          None
                          ))

    resp = requests.get(api_url)

    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    if data['sex']:
        user.userprofile.gender = UserProfile.MALE if data['sex'] == 2 else UserProfile.FEMALE

    if data['about']:
        user.userprofile.about_me = data['about']

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
        age = timezone.now().year - bdate.year

        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        user.age = age

    if data['photo_max']:
        if user.avatar:
            request.urlretrieve(data['photo_max'], BASE_DIR + f'/media/users_avatars/{user.pk}.jpg')
            user.avatar = f'/users_avatars/{user.pk}.jpg'

    user.save()
