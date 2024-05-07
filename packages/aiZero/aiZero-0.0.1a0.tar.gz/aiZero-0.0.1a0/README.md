aiZero是一个简单易用的可以连接常用人工智能接口，快速搭建可视化本地web应用的Python第三方库，适配幻码人工智能初阶课程。

### 快速开始

```python
from aiZero import AIWebApp

# 设定web应用的功能
def my_ai_function():
    pass

app = AIWebApp(title='人工智能助手')    # 初始化web应用
app.set_apikey('YOUR_API_KEY')    # 设定AI接口的api key
app.add_input_text()    # 在页面中添加一个输入文本框
app.add_submit(my_ai_function)    # 添加一个提交按钮，点击后执行函数
app.run(port=6060)    # 启动应用，设定端口，默认为5000
```

启动后，你将可以在浏览器中访问http://127.0.0.1:6060/查看搭建好的web应用。

如果需要实现AI功能的可视化呈现，你只需要将`'YOUR_API_KEY'`替换为真实的api key，并完善`my_ai_function`函数即可。

### AI功能实现例子

#### 大模型文字交互

##### 单轮对话

```python
from aiZero import AIWebApp, text_generation

def my_ai_function():
    text = app.input_text    # 获取输入文本框的文字内容
    reply = text_generation([text])    # 调用AI接口，获取回复反馈
    app.results.append({'text': reply})    # 以文字形式将结果推送至前端

app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_input_text()
app.add_submit(my_ai_function)
app.run(port=6060)
```

##### 多轮对话

```python
from aiZero import AIWebApp, text_generation

def my_ai_function():
    text = app.input_text
    chat_history.append(text)    # 将输入内容添加到对话历史
    reply = text_generation(chat_history)
    chat_history.append(reply)    # 将回复结果添加到对话历史
    app.results.append({'text': reply})

chat_history = []    # 储存对话历史
app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_input_text()
app.add_submit(my_ai_function)
app.run(port=6060)
```

##### 设置系统指令

```python
from aiZero import AIWebApp, text_generation

def my_ai_function():
    text = app.input_text
    chat_history.append(text)
    # prompt参数可以设定系统指令，设定模型的行为要求
    reply = text_generation(chat_history, prompt='你是一个10岁的小学生，名叫小幻')
    chat_history.append(reply)
    app.results.append({'text': reply})

chat_history = []
app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_input_text()
app.add_submit(my_ai_function)
app.run(port=6060)
```

#### 图像理解

##### 上传图片文件

```python
from aiZero import AIWebApp, image_understanding

def my_ai_function():
    text = app.input_text
    img = app.input_pic    # 获取上传的图片
    reply = image_understanding(img, [text])
    app.results.append({'text': reply})

chat_history = []
app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_input_text()
app.add_pic_file()    # 添加一个图片文件上传按钮
app.add_submit(my_ai_function)
app.run(port=6060)
```

##### 摄像头捕获图像

```python
from aiZero import AIWebApp, image_understanding

def my_ai_function():
    text = app.input_text
    img = app.input_pic    # 获取捕获的图片
    reply = image_understanding(img, [text])
    app.results.append({'text': reply})

chat_history = []
app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_input_text()
app.add_camera()    # 添加摄像头捕获窗口和按钮
app.add_submit(my_ai_function)
app.run(port=6060)
```

#### 声音理解

##### 上传音频文件

```python
from aiZero import AIWebApp, audio_understanding

def my_ai_function():
    text = app.input_text
    audio = app.input_audio    # 获取上传的音频
    reply = audio_understanding(audio, [text])
    app.results.append({'text': reply})

chat_history = []
app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_input_text()
app.add_audio_file()    # 添加一个音频文件上传按钮
app.add_submit(my_ai_function)
app.run(port=6060)
```

##### 实时录音

```python
from aiZero import AIWebApp, audio_understanding

def my_ai_function():
    text = app.input_text
    audio = app.input_audio    # 获取录制的音频
    reply = audio_understanding(audio, [text])
    app.results.append({'text': reply})

chat_history = []
app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_input_text()
app.add_record()    # 添加音频录制功能区
app.add_submit(my_ai_function)
app.run(port=6060)
```

#### 图像生成

```python
from aiZero import AIWebApp, image_generation

def my_ai_function():
    text = app.input_text
    reply = image_generation(text)
    app.results.append({'image': reply})    # 将生成的图像推送到前端

app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_input_text()
app.add_submit(my_ai_function)
app.run(port=6060)
```

#### 人物图像风格重绘

```python
from aiZero import AIWebApp, human_repaint

def my_ai_function():
    img = app.input_pic
    reply = human_repaint(img)
    app.results.append({'image': reply})

app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_camera()
app.add_submit(my_ai_function)
app.run(port=6060)
```

以上例程为使用摄像头采集图像，也可以改为上传图片文件。

`human_repaint`函数可以接受`style`参数设定风格类型，可选值为0～9的数字（默认值为7）。

#### 涂鸦作画

```python
from aiZero import AIWebApp, sketch_to_image

def my_ai_function():
    text = app.input_text    # 涂鸦作画的提示文字
    img = app.input_pic    # 涂鸦草图图像
    reply = sketch_to_image(img, text)
    app.results.append({'image': reply})

app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_input_text()
app.add_pic_file()
app.add_submit(my_ai_function)
app.run(port=6060)
```

以上例程为上传图片文件，也可以改为用摄像头捕获图像。

`sktech_to_image`函数可以接受`style`参数设定风格类型，包括：

- `"<3d cartoon>"`：3D 卡通
- `"<anime>"`：二次元（默认值）
- `"<oil painting>"`：油画
- `"<watercolor>"` ：水彩
- `"<flat illustration>"`：扁平插画

#### 语音识别

```python
from aiZero import AIWebApp, speech_recognition

def my_ai_function():
    audio = app.input_audio
    reply = speech_recognition(audio)
    app.results.append({'text': reply})

app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_record()
app.add_submit(my_ai_function)
app.run(port=6060)
```

所用接口支持中英文双语的语音识别。以上例程为实时录音，也可以改为上传录音音频文件。

#### 语音合成

```python
from aiZero import AIWebApp, speech_synthesis

def my_ai_function():
    text = app.input_text
    reply = speech_synthesis(text)
    app.results.append({'audio': reply})    # 将音频结果推送到前端

app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_input_text()
app.add_submit(my_ai_function)
app.run(port=6060)
```

`speech_synthesis`函数可以接受以下参数：

- `model`：设定使用的语音模型，详细列表参见[链接](https://help.aliyun.com/zh/dashscope/model-list)。
- `rate`：设定语速快慢，取值范围0.5~2，默认值为1。
- `pitch`：设定语调高低，取值范围0.5~2，默认值为1。

### 进阶使用

#### 多种AI功能的混合

aiZero支持方便地将不同的AI功能进行链式整合，例如，将文字交互、语音识别、语音合成结合起来，可以实现语音交互。

```python
from aiZero import AIWebApp, text_generation, speech_recognition, speech_synthesis

def my_ai_function():
    audio = app.input_audio
    text = speech_recognition(audio)
    chat_history.append(text)
    reply = text_generation([text])
    chat_history.append(reply)
    reply_audio = speech_synthesis(reply)
    app.results.append({'audio': reply_audio})

chat_history = []
app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_record()
app.add_submit(my_ai_function)
app.run(port=6060)
```

#### 同时输出多种不同类型的信息

aiZero支持输出文字、音频和图像等多种不同类型的信息，但每种类型的信息只能为一个（即不支持一次性输出2张图像、2段音频），且必须同时推送到前端。例如，我们可以输入文字，同时以文本和音频形式输出AI的响应。

```python
from aiZero import AIWebApp, text_generation, speech_synthesis

def my_ai_function():
    text = app.input_text
    chat_history.append(text)
    reply = text_generation([text])
    chat_history.append(reply)
    reply_audio = speech_synthesis(reply)
    app.results.append({'text': reply, 'audio': reply_audio})

chat_history = []
app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_input_text()
app.add_submit(my_ai_function)
app.run(port=6060)
```

