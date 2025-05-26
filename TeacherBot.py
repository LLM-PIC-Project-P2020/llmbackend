from openai import OpenAI
from templates import *
from test_case import Knowledges, Test

# DEEPSEEK_API_KEY = "sk-e818c70c505248ba8d1266283907f905"
# DEEPSEEK_BASE_URL = "https://api.deepseek.com"
API_KEY =  "sk-rfWtF0v1aOGFJNbBMREnlbTb1jmmRMe9za2bjHUMrTNJzFdE"
BASE_URL = "https://api.moonshot.cn/v1"
MODEL = "moonshot-v1-8k"



class TeacherBot:
    def __init__(self, chosen_chapter: str, language_type: str = "Python") -> None:
        self.client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
        self.language_type = language_type
        self.prepare_lessons(chosen_chapter)
        self.previous_content = None

    def prepare_lessons(self, chosen_chapter: str = None) -> None:
        #TODO: request lesson content from the back-end
        self.lessons = Knowledges
        # self.lessons = []
        self.test = Test

    def recommand_lessons(self, test_result: str):
        #TODO: match the most relevant chapter according to student's previous test result
        pass
    
    def continue_chapter(self):
        if len(self.lessons) > 0:
            return self.teach(), False
        elif len(self.test) > 0:
            return self.test.pop(0), True
        else:
            return
    
    def get_stream_completion(self, prompt):
        messages = [
            {"role": "user", "content": prompt},
        ]
        response = self.client.chat.completions.create(
            model = MODEL,
            messages = messages,
            stream = True
        )

        full_content = ""
        for chunk in response:
            content =  chunk.choices[0].delta.content
            if content == None:
                continue
            full_content += content
            yield content
        
        # TODO: refine the logic here
        self.previous_content = full_content

    def teach(self):
        lesson = self.lessons.pop(0)
        lesson_content = f"# {lesson['标题']}\n\n{lesson['内容']}"
        prompt = tutor_prompt(self.language_type, lesson_content, self.previous_content)
        
        return self.get_stream_completion(prompt)
    
    def answer_question(self, question, context, code=None):
        if code is None:
            prompt = qa_prompt_without_code(question, context)
        else:
            prompt = qa_prompt_with_code(question, context, code)
        return self.get_stream_completion(prompt)

    def test_correction(self, test_content, language_response="", code_response=""):
        student_response = language_response if code_response == "" else code_response
        prompt = test_correction_prompt(test_content, student_response, self.language_type)
        return self.get_stream_completion(prompt)
    
if __name__ == "__main__":
    teacher = TeacherBot(chosen_chapter="Python")
    for response in teacher.teach():
        print(response, end="")
    for response in teacher.answer_question("请问Python可以用来做什么？", "Python 是一门流行的编程语言。它由 Guido van Rossum 创建，于 1991 年发布。它用于：Web 开发（服务器端）、软件开发、数学、系统脚本。"):
        print(response, end="")
    for response in teacher.test_correction("请编写代码，输出'Hello, World!'", "print('Hello, World!')"):
        print(response, end="")
    teacher.continue_chapter()
        
