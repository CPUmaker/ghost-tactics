'''
user management API
'''
import re
import random

from django.views.decorators.http import require_GET, require_POST
from django.http.request import HttpRequest

from Crypto.Cipher import AES
import base64

from userManage.models.player import Player
from userManage.models.card import Card
from userManage.models.log import Log

from .utils import response_wrapper, success_api_response, failed_api_response, ErrorCode


salt = '!%F=-?Pst970'
key32 = "{: <32}".format(salt).encode("utf-8")
model = AES.MODE_ECB

@response_wrapper
@require_POST
def login(request: HttpRequest):
    """Handle requests which are to obtain jwt token

    [route]: /user_manage/user/token-auth

    [method]: POST
    """
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    if username and password:
        username = username.strip()
        try:
            user = Player.objects.get(username=username)
        except:
            return failed_api_response(ErrorCode.UNAUTHORIZED,
                                       "Your username or email address is invalid.")
        if user.password != password:
            return failed_api_response(ErrorCode.UNAUTHORIZED,
                                       "Your password is incorrect!")
        Log.objects.create(player=user)
        aes = AES.new(key32, model)
        user_id = base64.urlsafe_b64encode(aes.encrypt(str(user.pk).zfill(16).encode(encoding='utf-8')))
        return success_api_response({
            "user_id": user_id.decode(),
            "user_name": username
        })
    return failed_api_response(ErrorCode.UNAUTHORIZED,
                               "Your username or password is empty!")


@response_wrapper
@require_POST
def register(request):
    """Handle requests which are to register a new user

    [route]: /user_manage/user/register

    [method]: POST
    """
    print(request.POST)
    username = request.POST.get('username', None)
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    if username and email and password:
        username = username.strip()
        if Player.objects.filter(username=username).exists():
            return failed_api_response(ErrorCode.UNAUTHORIZED,
                                       "Username exists.")
        if Player.objects.filter(email=email).exists():
            return failed_api_response(ErrorCode.UNAUTHORIZED,
                                       "Email exists.")
        if len(username) == 0:
            return failed_api_response(ErrorCode.UNAUTHORIZED,
                                       "Username cannot be empty.")
        if len(username) > 50:
            return failed_api_response(ErrorCode.UNAUTHORIZED,
                                       "Username cannot larger than 50 chars.")
        # if not username_checker(username):
        #     return failed_api_response(ErrorCode.UNAUTHORIZED,
        #                                "Username must contains numbers, letters or '_'.")
        if len(password) <= 6:
            return failed_api_response(ErrorCode.UNAUTHORIZED,
                                       "The length of password must larger than 6.")
        if len(password) > 18:
            return failed_api_response(ErrorCode.UNAUTHORIZED,
                                       "The length of password cannot larger than 18 chars.")
        if re.match(r'.*[^0-9a-zA-Z@#$%]+.*', password):
            return failed_api_response(ErrorCode.UNAUTHORIZED,
                                       "Password must contains numbers, letters or '@', '#', '$' and '%'.")

        user = Player.objects.create(username=username,
                                     email=email,
                                     password=password)
        for i in range(12):
            Card.objects.create(player=user, type=i)
        return success_api_response({
            "user_id": str(user.pk),
        })
    else:
        return failed_api_response(ErrorCode.UNAUTHORIZED,
                                   "params format error.")
