from django.test import TestCase, Client
from django.http import JsonResponse, StreamingHttpResponse
from unittest.mock import patch, MagicMock
from .views import TutorRespondView

# class TutorRespondViewTestCase(TestCase):
#     def setUp(self):
#         # 初始化测试客户端
#         self.client = Client()

#     def test_post_with_invalid_token(self):
#         # 发送POST请求到视图，使用无效的token
#         response = self.client.post('/tutorResponse/', content_type='application/json', data='{"code": "test_code", "prompt": "test_prompt"}')
        
#         # 检查响应的状态码是否为400（Bad Request）
#         self.assertEqual(response.status_code, 400)
        
#         # 检查响应的内容
#         response_data = response.json()
#         self.assertEqual(response_data['error'], 'Access denied')

#     def test_post_with_missing_token(self):
#         # 发送POST请求到视图，不使用token
#         response = self.client.post('/tutorResponse/',content_type='application/json', data='{"code": "test_code", "prompt": "test_prompt"}')
        
#         # 检查响应的状态码是否为400（Bad Request）
#         self.assertEqual(response.status_code, 400)
        
#         # 检查响应的内容
#         response_data = response.json()
#         self.assertEqual(response_data['error'], 'Access denied')

#     def test_post_with_valid_token_and_invalid_json(self):
#         # 发送POST请求到视图，使用有效的token但无效的JSON数据
#         response = self.client.post('/tutorResponse/?token=valid_token', content_type='application/json', data='{invalid_json}')
        
#         # 检查响应的状态码是否为400（Bad Request）
#         self.assertEqual(response.status_code, 400)
        
#         # 检查响应的内容
#         response_data = response.json()
#         self.assertEqual(response_data['error'], 'Invalid JSON data')

#     @patch('aichat.views.token_check')
#     @patch('aichat.views.get_stream_completion')
#     def test_post_with_valid_token_and_valid_json(self, mock_get_stream_completion, mock_token_check):
#         # 模拟token_check返回True
#         mock_token_check.return_value = True
        
#         # 模拟get_stream_completion返回一个生成器
#         mock_stream = MagicMock()
#         mock_stream.return_value = iter(["Code: test_code\n", "Prompt: test_prompt\n", "Completion: Example completion\n"])
#         mock_get_stream_completion.return_value = mock_stream()
        
#         # 发送POST请求到视图，使用有效的token和有效的JSON数据
#         response = self.client.post('/tutorResponse/?token=valid_token', content_type='application/json', data='{"code": "test_code", "prompt": "test_prompt"}')
        
#         # 检查响应的状态码是否为200（OK）
#         self.assertEqual(response.status_code, 200)
        
#         # 检查响应的内容类型是否为text/plain
#         self.assertEqual(response['Content-Type'], 'text/plain')
        
#         # 检查响应的内容
#         response_content = ''.join([chunk.decode('utf-8') for chunk in response.streaming_content])
#         expected_content = "Code: test_code\nPrompt: test_prompt\nCompletion: Example completion\n"
#         self.assertEqual(response_content, expected_content)

class SessionViewTestCase(TestCase):
    def setUp(self):
        
