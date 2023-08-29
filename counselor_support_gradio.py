import os

import openai
import datetime
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
import gradio as gr

import re
openai_api_key = "YOUR_OPENAI_API"
openai.api_key = openai_api_key

def filter_private_info(text):
    text = re.sub(r'(?<=名字叫)[\u4e00-\u9fa5]{2,4}', '<NAME>', text)
    text = re.sub(r'(?<=住在).*?，', '<ADDRESS>，', text)
    text = re.sub(r'(\d{4})年(\d{1,2})月(\d{1,2})日', '<YEAR>年<MONTH>月<DAY>日', text)
    text = re.sub(r'\d{10}', '<TELEPHONE>', text)
    return text

def detoxify(response):
    embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)
    persist_directory = "YOUR_VECTORE_DATABASE"
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    match = re.search(r"推荐的回复话术：(.*?)(?=推荐的心理疗法|$)", response, re.DOTALL)
    if match:
        recommended_response = match.group(1).strip()
        query = recommended_response
    else:
        print('解析失败')
        query = response
    docs = vectordb.similarity_search_with_score(query)
    db_query_score = docs[0][1]
    return db_query_score

def counselor_support_model(prompt):
    print('心理咨询师支持系统分析中...')
    role_define = '你是一名心理咨询专家，你的任务是辅助我（非专业心理干预人士）进行心理辅导。' \
                  '请务必记住你自己的身份，不要反转。请务必避免输出不正确，不积极的价值观！' \
                  '对于提问，请结合我所提供的背景信息，以专业的口吻进行下述回复，以尝试教导我正确思考，完成心理辅导。' \
                  '对我可能犯错误的地方请着重标注进行提示。对于问题中的不正确说法或者非专业表述，请指出错误并对我进行纠正。' \
                  '请在下方附上参考资料和相关案例以便我日后进行学习。' \
                  '对于患者问题中可能存在的认知歪曲请进行识别和分类。' \
                  '下述分别以patient和counselor分别代表着患者和咨询师的问题和想做出的回复。\n' \
                  '请以下述格式进行回复：' \
                  '* 患者心理问题的分析：\n' \
                  '* 患者认知歪曲特征识别：\n' \
                  '* 咨询师回复的评价：\n' \
                  '* 专业知识的纠正：\n' \
                  '* 推荐的回复话术：\n' \
                  '* 推荐的心理疗法：\n' \
                  '* 参考资料：\n'
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        temperature=0.8,
        max_tokens=1000,
        messages=[
            {"role": "system", "content": role_define},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']


def my_main(patient_question, counselor_answer):
    prompt = f'Patient: {patient_question}\n' \
             f'Counselor: {counselor_answer}'
    prompt = filter_private_info(prompt)
    print(f'提问：')
    print(f'{prompt}')
    counselor_support_response = counselor_support_model(prompt)
    ''' detoxify
    while True:
        counselor_support_response = counselor_support_model(prompt)
        print(counselor_support_response)
        detoxify_score = detoxify(counselor_support_response)
        if detoxify_score >= 0.2:
            break
    '''
    print(f'心理专家支持系统：\n{counselor_support_response}')
    save_base_path = 'counselor_support_report'
    os.makedirs(save_base_path, exist_ok=True)
    current_time = datetime.datetime.now()
    file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S.md")
    result = '* 生成时间：'+current_time.strftime("%Y-%m-%d %H-%M-%S")+'\n'+'## 心理专家支持系统：\n'+counselor_support_response
    with open(f'{save_base_path}/{file_name}', "w") as f:
        f.write(f'## 问题：\n{prompt}\n')
        f.write(f'* 生成时间：{current_time.strftime("%Y-%m-%d %H-%M-%S")}\n')
        f.write(f'## 心理专家支持系统：\n{counselor_support_response}')
    return result

demo = gr.Interface(fn=my_main,
                    inputs=[gr.Textbox(lines=2, placeholder="Patient:", label='客户的发言：'),
                            gr.Textbox(lines=2, placeholder="Counselor:", label='你的回复')],
                    outputs="text",
                    title='心理咨询师支持系统')

demo.queue().launch(share=False, inbrowser=True)
