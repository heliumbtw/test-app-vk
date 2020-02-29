import random
import requests
import time

from social_django.utils import load_strategy


class VkInfoService:
    def __init__(self, request):
        self.userFields = self.getUserFields(request)
        self.userFriends = self.getUserFriends(request)

    @staticmethod
    def getUserFields(request):
        user = request.user
        social = user.social_auth.get(provider='vk-oauth2')
        r = requests.get("https://api.vk.com/method/users.get",
                         params={"user_ids": social.extra_data['id'],
                                 "fields": "photo_max",
                                 "name_case": "Nom",
                                 "access_token": getToken(request),
                                 "v": "5.103"})
        return r.json()

    @property
    def Photo(self):
        return self.userFields['response'][0]['photo_max']

    @property
    def UserId(self):
        return self.userFields['response'][0]['id']

    @property
    def FirstName(self):
        return self.userFields['response'][0]['first_name']

    @property
    def LastName(self):
        return self.userFields['response'][0]['last_name']

    @staticmethod
    def getUserFriends(request):
        user = request.user
        social = user.social_auth.get(provider='vk-oauth2')
        r = requests.get("https://api.vk.com/method/friends.get",
                         params={"user_ids": social.extra_data['id'],
                                 "order": "hints",
                                 "fields": "domain",
                                 "name_case": "Nom",
                                 "access_token": social.extra_data['access_token'],
                                 "v": "5.103"})
        return r.json()

    @property
    def FriendsCount(self):
        return self.userFriends['response']['count']

    @property
    def Friends(self):
        a = []
        for i in range(self.userFriends['response']['count']):
            a.append(f"{self.userFriends['response']['items'][i]['first_name']} "
                     f"{self.userFriends['response']['items'][i]['last_name']}")
        return a

    @property
    def FriendsLinks(self):
        a = []
        for i in range(self.userFriends['response']['count']):
            a.append(f"https://vk.com/id{self.userFriends['response']['items'][i]['id']}")
        return a

    @property
    def FiveFriends(self):
        return random.sample(self.Friends, 5)


def getToken(request):
    user = request.user
    social = user.social_auth.get(provider='vk-oauth2')
    if (social.extra_data['auth_time'] + social.extra_data['expires'] - 10) <= int(time.time()):
        strategy = load_strategy()
        social.refresh_token(strategy)
    return social.extra_data['access_token']