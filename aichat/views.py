from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,StreamingHttpResponse
from rest_framework.views import APIView
from django.views import View
from rest_framework.response import Response
from .serializers import *
import json
from userdatabase import *
# Create your views here.

# 大模型API
API_KEY = "some_api_key"


#界面需求
def index(request):
    return render(request, 'index.html')

class TutorRespondView(View):
    def post(self, request):
        # 检查特殊token
        token = request.GET.get("token")
        if (token_check(token) == False):
            return JsonResponse({"error": "Access denied"}, status=400)
        
        # 解析请求体
        try:
            data = json.loads(request.body.decode("utf-8"))
            code = data.get("code")
            prompt = data.get("prompt")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        
        stream_response = code+'.'+prompt
        
        response = StreamingHttpResponse(stream_response, content_type="text/plain",content_length=2048)
        return response

class SessionView(View):
    #用户登录信息验证
    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            user_id = data.get("id")
            password = data.get("password")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        if (search(user_id,password) == False):
            return JsonResponse({"error": "Invalid user or password"}, status=401)
        else:
            token = 'some_token'+user_id
            user_login(user_id,password,token)
            return HttpResponse(token, content_type="text/plain")

    def delete(self, request):
        data = json.loads(request.body.decode("utf-8"))
        token = data.get("token")
        if(user_logout(token)):
            return JsonResponse({"success": "Logout successfully"}, status=200)
        else:
            return JsonResponse({"error": "Invalid token"}, status=400)


class UserView(View):
    def User_register(id,email,username,password):
        result = search(id,email,username,password)
        if(result):
            return JsonResponse({"error": "User already exists"}, status=400)
        else:
            create_user(id,email,username,password)
            return JsonResponse({"success": "User registered successfully"}, status=200)
        
    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            user_id = data.get("id")
            email = data.get("email")
            username = data.get("userName")
            password = data.get("password")
            status = data.get("status")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        if (search(username,password)):
            return JsonResponse({"error": "User already exists"}, status=400)
        else:
            create_user(user_id,email,username,password,status)
            return JsonResponse({"success": "User registered successfully"}, status=200)


