import os
from flask import Flask, render_template, jsonify, request, url_for, send_from_directory
import base64
import threading
from pathlib import Path
import uuid
import logging
from http import HTTPStatus
import dashscope
import requests
import time
import json


RESOURCE_PATH = Path(__file__).parent.resolve()


def resolve_resource_path(path):
    return Path(RESOURCE_PATH / path).resolve()


# 1. 大模型文字交互
def text_generation(chat_history, prompt='你是一个人工智能助手，你的名字叫小H', stream=False):
    def generator():
        for r in response:
            if r.status_code == HTTPStatus.OK:
                yield r.output.choices[0]['message']['content']
            else:
                return "错误: " + r.message
    try:
        result = words_check(chat_history[-1])
        if result['status'] == 'error':
            return result['message']
        result = words_check(prompt)
        if result['status'] == 'error':
            return result['message']
        messages = [{'role': 'system', 'content': prompt}]
        for index, content in enumerate(chat_history):
            if len(content) != 0:
                if index % 2 == 0:
                    messages.append({'role': 'user', 'content': content})
                else:
                    messages.append({'role': 'assistant', 'content': content})
            else:
                return '输入参数错误'
        response = dashscope.Generation.call(model="qwen-plus",
                                             messages=messages,
                                             result_format='message',
                                             stream=stream)
        if stream:
            return generator()
        else:
            if response.status_code == HTTPStatus.OK:
                return response.output.choices[0]['message']['content']
            else:
                return "错误: " + response.message
    except Exception as e:
        return "错误: " + str(e)


# 2. 大模型图像理解
def image_understanding(img, chat_history, prompt='你是一名人工智能助手', stream=False):
    try:
        result = words_check(chat_history[-1])
        if result['status'] == 'error':
            return result['message']
        result = words_check(prompt)
        if result['status'] == 'error':
            return result['message']
        img_url = upload_file(img)
        messages = [{'role': 'system', 'content': [{'text': prompt}]},
                    {'role': 'user', 'content': [{'image': img_url}, {'text': chat_history[0]}]}]

        for index, content in enumerate(chat_history[1:]):
            if index % 2 == 0:
                messages.append({'role': 'assistant', 'content': [{'text': content}]})
            else:
                messages.append({'role': 'user', 'content': [{'text': content}]})
        response = dashscope.MultiModalConversation.call(model='qwen-vl-plus',
                                                         messages=messages,
                                                         stream=stream)
        if stream:
            for r in response:
                if r.status_code == HTTPStatus.OK:
                    yield r.output.choices[0].message.content[0]['text']
                else:
                    return "错误: " + r.message
        else:
            if response.status_code == HTTPStatus.OK:
                return response.output.choices[0].message.content[0]['text']
            else:
                return "错误: " + response.message
    except Exception as e:
        return "错误: " + str(e)


# 3. 大模型声音理解
def audio_understanding(audio, chat_history, prompt='你是一名人工智能助手', stream=False):
    try:
        result = words_check(chat_history[-1])
        if result['status'] == 'error':
            return result['message']
        result = words_check(prompt)
        if result['status'] == 'error':
            return result['message']
        audio_url = upload_file(audio)
        messages = [{'role': 'system', 'content': [{'text': prompt}]},
                    {'role': 'user', 'content': [{'audio': audio_url}, {'text': chat_history[0]}]}]
        for index, content in enumerate(chat_history[1:]):
            if index % 2 == 0:
                messages.append({'role': 'assistant', 'content': [{'text': content}]})
            else:
                messages.append({'role': 'user', 'content': [{'text': content}]})
        response = dashscope.MultiModalConversation.call(model='qwen-audio-turbo',
                                                         messages=messages,
                                                         stream=stream)
        if stream:
            for r in response:
                if r.status_code == HTTPStatus.OK:
                    yield r.output.choices[0].message.content[0]['text']
                else:
                    return "错误: " + r.message
        else:
            if response.status_code == HTTPStatus.OK:
                return response.output.choices[0].message.content[0]['text']
            else:
                return "错误: " + response.message
    except Exception as e:
        return "错误: " + str(e)


# 4. 大模型图像生成
def image_generation(prompt):
    try:
        result = words_check(prompt)
        if result['status'] == 'error':
            return result['message']
        response = dashscope.ImageSynthesis.async_call(model='wanx-v1',
                                                       prompt=prompt,
                                                       n=1,
                                                       size='1024*1024')
        if response.status_code == HTTPStatus.OK:
            rsp = dashscope.ImageSynthesis.wait(response)
            if rsp.status_code == HTTPStatus.OK:
                return rsp.output.results[0].url
            else:
                return "错误: " + response.message
        else:
            return "错误: " + response.message
    except Exception as e:
        return "错误: " + str(e)


# 5. 大模型人像风格重绘
def human_repaint(img, style=7):
    try:
        img_url = upload_file(img)
        url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation'
    
        headers = {
            'Content-Type': 'application/json',
            'Authorization': dashscope.api_key,
            'X-DashScope-Async': 'enable'
        }
    
        params = {
            'model': 'wanx-style-repaint-v1',
            'input': {
                'image_url': img_url,
                'style_index': style
            }
        }
    
        response = requests.post(url, headers=headers, json=params)
        if response.status_code == 200:
            task_id = response.json()['output']['task_id']
            while True:
                time.sleep(3)
                response = requests.get('https://dashscope.aliyuncs.com/api/v1/tasks/{}'.format(task_id),
                                        headers={'Authorization': dashscope.api_key})
                if response.status_code == 200:
                    if response.json()['output']['task_status'] == 'SUCCEEDED':
                        return response.json()['output']['results'][0]['url']
                    elif response.json()['output']['task_status'] == 'FAILED':
                        return "错误: " + response.json()['output']['message']
                else:
                    return "错误: " + response.json()['message']
        else:
            return "错误: " + response.json()['message']
    except Exception as e:
        return "错误: " + str(e)


# 6. 涂鸦作画
def sketch_to_image(img, prompt, style='<anime>'):
    try:
        result = words_check(prompt)
        if result['status'] == 'error':
            return result['message']
        img_url = upload_file(img)
        url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis/'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': dashscope.api_key,
            'X-DashScope-Async': 'enable'
        }

        params = {
            'model': 'wanx-sketch-to-image-lite',
            'input': {
                'sketch_image_url': img_url,
                'prompt': prompt
            },
            'parameters': {
                'size': '768*768',
                'n': 1,
                'style': style
            }
        }

        response = requests.post(url, headers=headers, json=params)
        if response.status_code == 200:
            task_id = response.json()['output']['task_id']
            while True:
                time.sleep(3)
                response = requests.get('https://dashscope.aliyuncs.com/api/v1/tasks/{}'.format(task_id),
                                        headers={'Authorization': dashscope.api_key})
                if response.status_code == 200:
                    if response.json()['output']['task_status'] == 'SUCCEEDED':
                        return response.json()['output']['results'][0]['url']
                    elif response.json()['output']['task_status'] == 'FAILED':
                        return "错误: " + response.json()['output']['message']
                else:
                    return "错误: " + response.json()['message']
        else:
            return "错误: " + response.json()['message']
    except Exception as e:
        return "错误: " + str(e)


# 7. 语音识别
def speech_recognition(audio):
    try:
        audio_url = upload_file(audio)
        task_response = dashscope.audio.asr.Transcription.async_call(
            model='paraformer-v1',
            file_urls=[audio_url]
        )
        transcribe_response = dashscope.audio.asr.Transcription.wait(task=task_response.output.task_id)
        if transcribe_response.status_code == HTTPStatus.OK:
            result = transcribe_response.output
            if result['task_status'] == 'SUCCEEDED':
                json_url = result['results'][0]['transcription_url']
                response = requests.get(json_url)
                if response.status_code == 200:
                    data = response.json()
                    return data['transcripts'][0]['text']
                else:
                    return '错误: 结果获取出错'
            else:
                return '错误: 解码错误'
        else:
            return '错误: 解析错误'
    except Exception as e:
        return "错误: " + str(e)


# 8. 语音合成
def speech_synthesis(text, model='sambert-zhiying-v1', rate=1, pitch=1):
    try:
        result = dashscope.audio.tts.SpeechSynthesizer.call(model=model,
                                                            text=text,
                                                            rate=rate,  # 0.5-2
                                                            pitch=pitch)  # 0.5-2
        if result.get_audio_data() is not None:
            audio_data = result.get_audio_data()
            filename = f"{uuid.uuid4()}.wav"
            output_file_path = str(resolve_resource_path(f'static/audios/{filename}'))
            with open(output_file_path, 'wb') as audio_file:
                audio_file.write(audio_data)
            return f'static/audios/{filename}'
        else:
            return '错误: ' + result.get_response().message
    except Exception as e:
        return "错误: " + str(e)


def upload_file(file_path):
    file_path = str(resolve_resource_path(file_path))
    if not os.path.exists(file_path):
        return file_path
    with open(file_path, 'rb') as file:
        files = {'file': (file_path, file)}
        response = requests.post('https://fileserver.hlqeai.cn/upload', files=files)
    if response.status_code == 201:
        print("文件上传成功")
        print(response.json()['url'])
        return response.json()['url']
    else:
        print(response.status_code, response.text)
        raise Exception(
            'Error Message: {}, Status Code: {}, Response: {}'.format('文件上传失败', response.status_code, response.text))


def words_check(content):
    url = "http://wordscheck.hlqeai.cn/wordscheck"
    data = json.dumps({'content': content})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=data, headers=headers)
    if response.json()['code'] == '0':
        if response.json()['word_list']:
            return {'status': 'error', 'message': '您的输入信息可能含有违禁词，请谨慎输入'}
        else:
            return {'status': 'success', 'message': ''}
    else:
        return {'status': 'error', 'message': response.json()['msg']}


class AIWebApp:
    def __init__(self, title='My AI Web App'):
        self.app = Flask(__name__)
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        self.title = title
        self.components = []
        self.input_pic = None
        self.input_audio = None
        self.input_text = ''
        self.results = []

    def set_apikey(self, key):
        dashscope.api_key = key

    def add_input_text(self):
        self.components.append({
            'type': 'input_text',
            'id': 'textComponent'
        })

    def add_camera(self):
        self.components.append({
            'type': 'camera',
            'id': 'cameraComponent'
        })

    def add_record(self):
        self.components.append({
            'type': 'record',
            'id': 'recordComponent'
        })

    def add_pic_file(self):
        self.components.append({
            'type': 'input_pic',
            'id': 'inputPicComponent'
        })

    def add_audio_file(self):
        self.components.append({
            'type': 'input_audio',
            'id': 'inputAudioComponent'
        })

    def add_submit(self, callback):
        self.ai_callback = callback
        self.components.append({
            'type': 'submit',
            'id': 'submitButton'
        })

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html', title=self.title)

        @self.app.route('/get_components')
        def get_components():
            return jsonify(self.components)

        @self.app.route('/save_image', methods=['POST'])
        def save_image():
            data = request.get_json()
            image_data = data['image']

            header, encoded = image_data.split(",", 1)
            image_bytes = base64.b64decode(encoded)

            filename = f"{uuid.uuid4()}.png"
            filepath = Path(resolve_resource_path('static/images')) / filename

            with open(filepath, 'wb') as file:
                file.write(image_bytes)

            self.input_pic = str(str(Path('static/images') / filename))
            return jsonify({'filePath': str(filepath)})

        @self.app.route('/save_audio', methods=['POST'])
        def save_audio():
            if 'audioFile' not in request.files:
                return jsonify({'error': 'No audio file part'}), 400
            audio_file = request.files['audioFile']
            if audio_file.filename == '':
                return jsonify({'error': 'No selected audio file'}), 400
            if audio_file:
                filename = f"{uuid.uuid4()}.wav"
                filepath = Path(resolve_resource_path('static/audios')) / filename
                audio_file.save(filepath)
                self.input_audio = str(Path('static/audios') / filename)
                return jsonify({'message': 'Audio file uploaded successfully', 'filePath': str(filepath)})

        @self.app.route('/upload_image', methods=['POST'])
        def upload_image():
            if 'file' not in request.files:
                return jsonify({'error': 'No file part'}), 400
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No selected file'}), 400
            if file:
                filename = file.filename
                ext = file.filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
                filename = f"{uuid.uuid4()}.{ext}"
                file_path = Path(resolve_resource_path('static/images')) / filename
                file.save(file_path)
                self.input_pic = str(Path('static/images') / filename)
                # self.input_pic = str(file_path)
                file_url = url_for('static', filename=f'images/{filename}', _external=True)
                return jsonify({'message': 'File uploaded successfully', 'fileUrl': file_url})

        @self.app.route('/upload_audio', methods=['POST'])
        def upload_audio():
            if 'file' not in request.files:
                return jsonify({'error': 'No file part'}), 400
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No selected file'}), 400
            if file:
                filename = file.filename
                ext = file.filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
                filename = f"{uuid.uuid4()}.{ext}"
                file_path = Path(resolve_resource_path('static/audios')) / filename
                file.save(file_path)
                self.input_audio = str(Path('static/audios') / filename)
                file_url = url_for('static', filename=f'audios/{filename}', _external=True)
                return jsonify({'message': 'File uploaded successfully', 'fileUrl': file_url})

        @self.app.route('/submit-text', methods=['POST'])
        def submit_text():
            data = request.get_json()
            self.input_text = data['text']
            return jsonify({'message': '文本内容已成功接收'})

        @self.app.route('/submit', methods=['POST'])
        def submit():
            threading.Thread(target=self.ai_callback).start()
            response = {"status": "success"}
            if self.input_text:
                response['text'] = self.input_text
            if self.input_pic:
                response['image'] = self.input_pic
            if self.input_audio:
                response['audio'] = self.input_audio
            return jsonify(response)

        @self.app.route('/result', methods=['GET'])
        def get_result():
            if self.results:
                new_result = self.results.pop()
                self.results.clear()
                if 'running' in new_result:
                    new_result['status'] = 'processing'
                else:
                    new_result['status'] = 'finish'
                return jsonify(new_result)
            return jsonify({"status": "processing", "content": ""})

        @self.app.route('/static/audios/<filename>')
        def audio_file(filename):
            return send_from_directory('static/audios', filename)

        @self.app.route('/static/images/<filename>')
        def image_file(filename):
            return send_from_directory('static/images', filename)

    def run(self, **kwargs):
        if not os.path.exists(resolve_resource_path('static/images')):
            os.mkdir(resolve_resource_path('static/images'))
        if not os.path.exists(resolve_resource_path('static/audios')):
            os.mkdir(resolve_resource_path('static/audios'))
        for file in os.listdir(resolve_resource_path('static/images')):
            os.remove(os.path.join(resolve_resource_path('static/images'), file))
        for file in os.listdir(resolve_resource_path('static/audios')):
            os.remove(os.path.join(resolve_resource_path('static/audios'), file))
        self.setup_routes()
        if 'port' in kwargs:
            port = kwargs['port']
        else:
            port = '5000'
        print(f'访问地址：http://127.0.0.1:{port}')
        self.app.run(**kwargs)
