import gradio as gr
from openai import OpenAI
from pathlib import Path
from pydub import AudioSegment
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Initialize OpenAI client
# add base_url if you need to use a custom endpoint
client = OpenAI(
    api_key='sk-xxxx',
    base_url='http://xxx/v1'
)


# Define functions for splitting audio and transcribing to text
def split_audio_with_pydub(file_path, segment_length_ms=20*60*1000):
    # Read audio file
    audio = AudioSegment.from_file(file_path, format="mp3")
    
    # Calculate the number of segments
    total_length = len(audio)
    segments = [audio[i:i+segment_length_ms] for i in range(0, total_length, segment_length_ms)]
    
    # Save each segment
    segment_paths = []
    for i, segment in enumerate(segments):
        segment_path = f"./temp_segment_{i}.mp3"
        segment.export(segment_path, format="mp3")
        segment_paths.append(segment_path)
    
    return segment_paths

def transcribe_segment(segment_path, index, attempt=1):
    try:
        with open(segment_path, "rb") as audio_file:
            segment_text = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text",
                timeout=60  # Set timeout to 60 seconds
            )
            return index, segment_text
    except openai.error.Timeout:
        if attempt <= 3:
            print(f"Request timed out on attempt {attempt}. Retrying...")
            time.sleep(5)  # Wait 5 seconds before retrying
            return transcribe_segment(segment_path, index, attempt + 1)
        else:
            print(f"Failed to transcribe segment {segment_path} after 3 attempts.")
            return index, ""

def transcribe_audio_with_progress(uploaded_file, progress=gr.Progress(track_tqdm=True)):
    if uploaded_file is None:
        raise ValueError("No file uploaded")
    
    file_path = uploaded_file.name
    
    # Use pydub to read the audio file and split it into 10-minute segments
    segment_paths = split_audio_with_pydub(file_path)
    num_segments = len(segment_paths)

    transcribed_texts = [""] * num_segments
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_index = {executor.submit(transcribe_segment, path, i): i for i, path in enumerate(segment_paths)}
        for i, future in enumerate(as_completed(future_to_index)):
            index, segment_text = future.result()
            transcribed_texts[index] = segment_text
            progress((i + 1) / num_segments)  # Update progress bar
    
    transcribed_text = "\n".join(transcribed_texts)
    return transcribed_text

# Define summarize function with an added prompt parameter
def summarize_text_with_progress(input_text, prompt, progress=gr.Progress(track_tqdm=True), model="gpt-3.5-turbo"):
    max_tokens = 1000  # Maximum token limit for gpt-3.5-turbo
    input_tokens = input_text.split()
    
    # Split input text into appropriate chunks
    segments = [' '.join(input_tokens[i:i + max_tokens]) for i in range(0, len(input_tokens), max_tokens)]
    summarized_text = ""
    num_segments = len(segments)

    for i, segment in enumerate(segments):
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": segment}
            ]
        )
        summarized_text += response.choices[0].message.content + "\n"
        progress((i + 1) / num_segments)  # Update progress bar

    return summarized_text

# Define function to convert text to speech
def text_to_speech(input_text):
    speech_response = client.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=input_text
    )
    speech_file_path = Path("./speech_output.mp3")  # 定义音频文件的保存路径
    speech_response.stream_to_file(speech_file_path)  # 保存音频文件

    return speech_file_path  # 返回音频文件的路径供下载或播放

with gr.Blocks() as demo:
    # Audio upload and transcription part
    with gr.Group():
        with gr.Row():
            audio_input = gr.File(label="Upload Audio File")
        with gr.Row():
            transcribe_btn = gr.Button("Transcribe")
        with gr.Row():
            transcribed_text_output = gr.Textbox(label="Transcribed Text")

    transcribe_btn.click(
        fn=transcribe_audio_with_progress,
        inputs=audio_input,
        outputs=transcribed_text_output
    )

    # Summary and text-to-speech part
    with gr.Group():
        with gr.Row():
            custom_prompt_input = gr.Textbox(label="Custom Prompt", value="You are a meeting assistant. Based on the provided meeting content, summarize the key points of the meeting.")
        with gr.Row():
            summarize_btn = gr.Button("Summarize")
        with gr.Row():
            summarized_text_output = gr.Textbox(label="Summarized Text")
        with gr.Row():
            speech_output = gr.Audio(label="Summarized Text Speech Output", type="filepath")  # Added speech output
            tts_btn = gr.Button("Convert Text to Speech")

    # Click event for summarize button
    summarize_btn.click(
        fn=summarize_text_with_progress,
        inputs=[transcribed_text_output, custom_prompt_input],
        outputs=summarized_text_output
    )

    # Click event for text-to-speech button
    tts_btn.click(
        fn=text_to_speech,
        inputs=summarized_text_output,
        outputs=speech_output
    )

# Launch Gradio interface
demo.launch(server_name='0.0.0.0', server_port=8008)
