import gradio as gr
from TeacherBot import TeacherBot  
import psutil

# 初始化教学参数
INIT_CHAPTER = None
LANGUAGE_TYPE = "Python"

# 创建教学实例
teacher = TeacherBot(chosen_chapter=INIT_CHAPTER, language_type=LANGUAGE_TYPE)
test_content = ""

def format_code_output(response):
    """格式化代码输出为Markdown"""
    return f"```{LANGUAGE_TYPE.lower()}\n{response}\n```"

def handle_continue_click():
    global test_content
    # 继续教学流程
    response, test_mode = teacher.continue_chapter()
    full_response = ""
    if test_mode:
        test_content = response
        yield response
    else:
        for chunk in response:
            full_response += chunk
            print(chunk, end="")
            yield full_response
        
def handle_code_submit(code_input, answer_input):
    global test_content
    response_stream = teacher.test_correction(test_content, answer_input, code_input)
    full_response = ""
    for chunk in response_stream:
        full_response += chunk
        yield full_response
    

def handle_question(question, context):
    # 获取回答
    response_stream = teacher.answer_question(question, context)
    full_response = ""
    for chunk in response_stream:
        full_response += chunk
        # print(chunk, end="")
        yield full_response

with gr.Blocks(title="编程教学助手") as demo:
    gr.Markdown("# 智能编程教学系统")
    
    with gr.Row():
        with gr.Column(scale=3):
            code_input = gr.Code(
                    label="代码输入",
                    language=LANGUAGE_TYPE.lower(),
                    interactive=True,
                    lines=35         
            )
        with gr.Column(scale=3):
            chatbot = gr.Textbox(
                label="教学对话",
                lines=30
            )
            continue_btn = gr.Button("继续", variant="primary")

    with gr.Row():
        question_input = gr.Textbox(
            label="提问输入",
            placeholder="输入你的问题..."
        )
        code_submit = gr.Button("提交代码")
            
    # 组件交互
    continue_btn.click(
        handle_continue_click,
        inputs=[],
        outputs=[chatbot]
    )
    
    code_submit.click(
        handle_code_submit,
        inputs=[code_input, question_input],
        outputs=[chatbot]
    )
    
    question_input.submit(
        handle_question,
        inputs=[question_input, chatbot],
        outputs=[chatbot]
    )

if __name__ == "__main__":
    port = 50500
    demo.launch(server_name="127.0.0.1", server_port=port, share=True)