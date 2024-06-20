# AudioTranscribeGPT

# Audio Transcription and Summarization with Gradio and OpenAI

# 使用 Gradio 和 OpenAI 进行音频转录和总结

## Features

## 功能

-   **Audio Upload**: Upload an audio file in MP3 format.
-   **音频上传**: 上传 MP3 格式的音频文件。

-   **Audio Transcription**: Transcribe the audio to text using OpenAI's Whisper model.
-   **音频转录**: 使用 OpenAI 的 Whisper 模型将音频转录为文本。

-   **Text Summarization**: Summarize the transcribed text using OpenAI's GPT-3.5-turbo model.
-   **文本总结**: 使用 OpenAI 的 GPT-3.5-turbo 模型总结转录的文本。

-   **Text-to-Speech**: Convert the summarized text to speech using OpenAI's TTS model.
-   **文本转语音**: 使用 OpenAI 的 TTS 模型将总结的文本转换为语音。

## Requirements

## 依赖

-   Python 3.10
-   Gradio
-   OpenAI
-   pydub
-   pathlib

## Installation

## 安装

1. Clone this repository:
1. 克隆此仓库:

    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

1. Install the required packages:
1. 安装所需的依赖包:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

## 使用方法

1. Set up your OpenAI API key:
1. 设置你的 OpenAI API 密钥:

    Replace `'sk-xxxx'` with your actual OpenAI API key in the script.
    在脚本中将 `'sk-xxxx'` 替换为你的实际 OpenAI API 密钥。

1. Run the application:
1. 运行应用程序:

    ```bash
    python your_script_name.py
    ```

1. Open your web browser and go to `http://127.0.0.1:8008` to access the Gradio interface.
1. 打开你的浏览器，访问 `http://127.0.0.1:8008` 进入 Gradio 界面。

## License

## 许可证

This project is licensed under the MIT License.
此项目基于 MIT 许可证。
