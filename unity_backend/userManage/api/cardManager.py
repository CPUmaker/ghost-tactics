'''
card management API
'''
from django.views.decorators.http import require_GET, require_POST
from django.http.request import HttpRequest

from Crypto.Cipher import AES
import base64

from userManage.models.player import Player
from userManage.models.card import Card

from .utils import response_wrapper, success_api_response, failed_api_response, ErrorCode


salt = '!%F=-?Pst970'
key32 = "{: <32}".format(salt).encode("utf-8")
model = AES.MODE_ECB

@response_wrapper
@require_GET
def getCards(request: HttpRequest, user_id: str):
    """Handle requests which are to obtain jwt token

    [route]: /user_manage/card/get_cards/<str:user_id>

    [method]: GET
    """
    aes = AES.new(key32, model)
    user_id = str(aes.decrypt(base64.urlsafe_b64decode(user_id)), encoding='utf-8')
    user_id = int(user_id)
    try:
        user = Player.objects.get(pk=user_id)
    except:
        return failed_api_response(ErrorCode.UNAUTHORIZED,
                                    "Your username or email address is invalid.")

    cards = Card.objects.all().filter(player__pk=user_id)

    return success_api_response({
        "card_list": [card.type for card in cards],
    })
