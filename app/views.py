from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from vk_login.vkInfoService import VkInfoService


def login(request):
    return render(request, 'index.html')


@login_required
def home(request):
    if request.method == 'GET':
        vk_user = VkInfoService(request)
        return render(request, 'home.html',
                      {
                        'photo': vk_user.Photo,
                        'first_five': vk_user.FiveFriends,
                        'friends_list': zip(vk_user.Friends, vk_user.FriendsLinks),
                        'friends_count': vk_user.FriendsCount
                      })
