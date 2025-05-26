from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,StreamingHttpResponse
from rest_framework.views import APIView
from django.views import View
from rest_framework.response import Response
import json
import time
import asyncio
from database import *
import subprocess
# Create your views here.


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
            prompt = data.get("prompt")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        
        stream_response = get_stream_completion(prompt)
        
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

class CoursesView(View):
    def get(self, request):
        result, classes = get_all_course()
        if result == True:
            if classes != []:
                return JsonResponse({"success": "Classes found", "classes": classes}, status=200)
            else:
                return JsonResponse({"error": "No classes found"}, status=400)
        else:
            return JsonResponse({"error": "No classes found"}, status=404)

class ClassesView(View):
    def get(self, request):
        try:
            data = request.GET.get("id")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        if data == None:
            return JsonResponse({"error": "Invalid course id"}, status=400)
        else:
            result, course = get_all_classes(data)
            if (result ==True):
                return JsonResponse({"success": "Course found", "course": course}, status=200)
            else:
                return JsonResponse({"error": "Course not found"}, status=404)

class ClassContentView(View):
    def get(self, request):
        try:
            class_id = request.GET.get("classId")
            course_id = request.GET.get("courseId")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        if (class_id == None or course_id == None):
            return JsonResponse({"error": "Invalid class or course id"}, status=400)
        else:
            result, course_content = get_class_description(course_id, class_id)
            if result == True:
                return JsonResponse({"success": "Course content found", "course_content": course_content[1]}, status=200)
            else:
                return JsonResponse({"error": "Course content not found"}, status=404)

class CodeComplierView(View):
    def post(self, request):
        if request.method == "POST":
            # 获取用户输入的代码
            code = request.form.get("code")
            try:
                result = code_complier(code)
            except:
                return JsonResponse({"error": "Invalid code"}, status=400)
            return JsonResponse({'result':result}, status=200)

def async_generator():
    for i in range(10):
        yield str(i)+"\n"
        time.sleep(1)

def stream_response(request):
    response = StreamingHttpResponse(async_generator(), content_type="text/plain")
    return response

def code_complier(code):
    try:
        # 使用 subprocess 执行代码并捕获输出
        result = subprocess.run(
            ["python", "-c", code],  # 执行代码
            text=True,               # 以文本形式返回输出
            capture_output=True,    # 捕获标准输出和错误
            timeout=5,               # 设置超时时间（秒）
        )
        # 返回执行结果
        if result.returncode == 0:  # 执行成功
            output = result.stdout
        else:  # 执行失败
            output = result.stderr

    except subprocess.TimeoutExpired:  # 超时处理
        output = "Error: Code execution timed out."
    except Exception as e:  # 其他异常
        output = f"Error: {str(e)}"
    result = {
        'output': output
    }
    return result  # 返回 JSON 格式的结果

def token_check(token):
    # 这里可以写token验证逻辑
    return True

async def get_stream_completion(prompt):
    # 这里可以写AI模型的调用逻辑
    for i in range(10):
        yield str(i)+"\n"
        await asyncio.sleep(1)