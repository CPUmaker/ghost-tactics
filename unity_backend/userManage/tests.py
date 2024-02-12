from django.test import TestCase

from .models.player import Player
from .models.card import Card
from .api.cardManager import getCards
from .api.playerManager import login, register
from .api.utils import parse_data, wrapped_api
from key_gen import generate_new_key

from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory

import json


# Create your tests here.
class PlayerModelTests(TestCase):

    def test_has_nine_card_per_player(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        user = Player(username='abc', email='188@qq.com', password='123456')
        self.assertIs(user.email=='188@qq.com', True)


class TestPlayerManager(APITestCase):
    def setUp(self):
        # 设置初始化的值
        self.factory = APIRequestFactory()
        generate_new_key()

    def test_list1(self):
        params = {
            'username': 'admin',
            'email': '123@abc.com',
            'password': 'test1234'
        }
        request = self.factory.post('/user_manage/user/register', params)
        response = register(request)
        self.assertEqual(
            response.status_code, 
            200,
            '预期200状态的响应，但响应码为{}.'.format(response.status_code)
        )
        response_data = json.loads(response.content)
        self.assertIsNotNone(
            response_data['user_id'], 
            '预期user_id存在，但出现错误'
        )
    
    def test_list2(self):
        params = {
            'username': 'admin',
            'email': '123@abc.com',
            'password': 'test1234'
        }
        request = self.factory.post('/user_manage/user/register', params)
        response = register(request)

        params = {
            'username': 'admin',
            'password': 'test1234'
        }
        request = self.factory.post('/user_manage/user/login', params)
        response = login(request)
        self.assertEqual(
            response.status_code, 
            200,
            '预期200状态的响应，但响应码为{}.'.format(response.status_code)
        )
        response_data = json.loads(response.content)
        self.assertEqual(
            response_data['user_name'], 
            'admin',
            '预期user_name==admin，但出现错误.'.format(response.status_code)
        )
    
    def test_list3(self):
        params = {
            'username': ' ',
            'email': '123@abc.com',
            'password': 'test1234'
        }
        request = self.factory.post('/user_manage/user/register', params)
        response = register(request)
        self.assertEqual(
            response.status_code, 
            401,
            '预期401状态的响应，但响应码为{}.'.format(response.status_code)
        )
        print(response.content)
    
    def test_list4(self):
        params = {
            'username': 'abc' * 50,
            'email': '123@abc.com',
            'password': 'test1234'
        }
        request = self.factory.post('/user_manage/user/register', params)
        response = register(request)
        self.assertEqual(
            response.status_code, 
            401,
            '预期401状态的响应，但响应码为{}.'.format(response.status_code)
        )
        print(response.content)
    
    def test_list5(self):
        params = {
            'username': 'abc',
            'email': '123@abc.com',
            'password': 'test1234'
        }
        request = self.factory.post('/user_manage/user/register', params)
        response = register(request)

        params = {
            'username': 'abc',
            'email': '123@abc.com',
            'password': 'test1234'
        }
        request = self.factory.post('/user_manage/user/register', params)
        response = register(request)
        self.assertEqual(
            response.status_code, 
            401,
            '预期401状态的响应，但响应码为{}.'.format(response.status_code)
        )
        print(response.content)

        request = self.factory.post('/user_manage/user/register', params)
        response = register(request)
        params = {
            'username': 'abcd',
            'email': '123@abc.com',
            'password': 'test1234'
        }
        request = self.factory.post('/user_manage/user/register', params)
        response = register(request)
        self.assertEqual(
            response.status_code, 
            401,
            '预期401状态的响应，但响应码为{}.'.format(response.status_code)
        )
        print(response.content)

    def test_list6(self):
        params = {
            'username': 'abc',
        }
        request = self.factory.post('/user_manage/user/register', params)
        response = register(request)
        self.assertEqual(
            response.status_code, 
            401,
            '预期401状态的响应，但响应码为{}.'.format(response.status_code)
        )

        params = {
            'username': 'abc',
        }
        request = self.factory.post('/user_manage/user/login', params)
        response = login(request)
        self.assertEqual(
            response.status_code, 
            401,
            '预期401状态的响应，但响应码为{}.'.format(response.status_code)
        )
        print(response.content)
    
    def test_list7(self):
        params = {
            'username': 'abc',
            'password': 'abc'
        }
        request = self.factory.post('/user_manage/user/login', params)
        response = login(request)
        self.assertEqual(
            response.status_code, 
            401,
            '预期401状态的响应，但响应码为{}.'.format(response.status_code)
        )
        print(response.content)
    
    def test_list8(self):
        # REGISTER
        params = {
            'username': 'abcd',
            'email': '123@abcd.com',
            'password': 'test1234'
        }
        request = self.factory.post('/user_manage/user/register', params)
        response = register(request)
        # LOGIN
        params = {
            'username': 'abcd',
            'password': 'test12345'
        }
        request = self.factory.post('/user_manage/user/login', params)
        response = login(request)
        self.assertEqual(
            response.status_code, 
            401,
            '预期401状态的响应，但响应码为{}.'.format(response.status_code)
        )


class TestCardManager(APITestCase):
    def setUp(self):
        # 设置初始化的值
        self.factory = APIRequestFactory()

    def test_list1(self):
        # REGISTER
        params = {
            'username': 'abcd',
            'email': '123@abcd.com',
            'password': 'test1234'
        }
        request = self.factory.post('/user_manage/user/register', params)
        response = register(request)
        # LOGIN
        params = {
            'username': 'abcd',
            'password': 'test1234'
        }
        request = self.factory.post('/user_manage/user/login', params)
        response = login(request)
        response_data = json.loads(response.content)
        # GET_CARDS
        request = self.factory.get('/user_manage/card/get_cards/' + response_data['user_id'])
        response = getCards(request, response_data['user_id'])
        self.assertEqual(
            response.status_code, 
            200,
            '预期200状态的响应，但响应码为{}.'.format(response.status_code)
        )
        response_data = json.loads(response.content)
        self.assertEqual(
            len(response_data['card_list']), 
            12,
            '预期回复card_list长度为12，但出现错误'
        )

    def test_list2(self):
        request = self.factory.get('/user_manage/card/get_cards/' + 'Ue-pEWdVuHa3bdGrGXSm5w==')
        response = getCards(request, 'Ue-pEWdVuHa3bdGrGXSm5w==')
        self.assertEqual(
            response.status_code, 
            401,
            '预期401状态的响应，但响应码为{}.'.format(response.status_code)
        )


class TestApiUtils(APITestCase):
    def setUp(self):
        # 设置初始化的值
        self.factory = APIRequestFactory()

    def test_list1(self):
        wrapped_api({"GET": True})
    
    def test_list2(self):
        params = {
            'username': 'admin',
            'email': '123@abc.com',
            'password': 'test1234'
        }
        request = self.factory.post('/user_manage/user/register', params)
        parse_data(request)
