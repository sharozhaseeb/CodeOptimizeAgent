import gradio as gr
from test_case_agent import agent_wrapper



def generate(input):
    result = agent_wrapper(code= input)
    return result

examples = [
    ["""def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            k =9
            return False
    return True"""]
]

demo = gr.Interface(
    theme='JohnSmith9982/small_and_pretty',
    title = "<p style = font-size:40px>Code Optimization Agent</p>",
    description="<p style='text-align: center; font-size: 16px;'>Currently experimental. We use GPT-3.5-turbo, Prompt Engineering and Python wrappers to achive the following</p>",
    fn=generate,
    inputs=gr.inputs.Textbox(lines=5, label="Input Unoptimized Code"),
    outputs=gr.outputs.Textbox(label="Critical Points Object"),
    examples=examples
)

demo.launch(debug = True, share = True)
