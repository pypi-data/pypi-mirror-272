# Open-Lyrics

[![PyPI](https://img.shields.io/pypi/v/openlrc)](https://pypi.org/project/openlrc/)
[![PyPI - License](https://img.shields.io/pypi/l/openlrc)](https://pypi.org/project/openlrc/)
[![Downloads](https://static.pepy.tech/badge/openlrc)](https://pepy.tech/project/openlrc)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/zh-plus/Open-Lyrics/ci.yml)

Open-Lyrics is a Python library that transcribes voice files using
[faster-whisper](https://github.com/guillaumekln/faster-whisper), and translates/polishes the resulting text
into `.lrc` files in the desired language using LLM,
e.g. [OpenAI-GPT](https://github.com/openai/openai-python), [Anthropic-Claude](https://github.com/anthropics/anthropic-sdk-python).

#### Key Features:

- Well preprocessed audio to reduce hallucination (Loudness Norm & optional Noise Suppression).
- Context-aware translation to improve translation quality.
  Check [prompt](https://github.com/zh-plus/openlrc/blob/master/openlrc/prompter.py) for details.

## New 🚨

- 2024.3.29: Claude models are now available for translation. According to the testing, Claude 3 Sonnet performs way
  better than GPT-3.5 Turbo. We recommend using Claude 3 Sonnet for non-english audio (source language) translation (For
  now, the default model
  are still GPT-3.5 Turbo):
    ```python
    lrcer = LRCer(chatbot_model='claude-3-sonnet-20240229')
    ```
- 2024.4.4: Add basic streamlit GUI support. Try `openlrc gui` to start the GUI.
- 2024.5.7:
    - Add custom endpoint (base_url) support for OpenAI & Anthropic:
        ```python
        lrcer = LRCer(base_url_config={'openai': 'https://api.chatanywhere.tech',
                                       'anthropic': 'https://api.g4f.icu'})
        ```
    - Generating bilingual subtitles
        ```python
        lrcer.run('./data/test.mp3', target_lang='zh-cn', bilingual_sub=True)
        ``` 

## Installation ⚙️

1. Please install CUDA 11.x and [cuDNN 8 for CUDA 11](https://developer.nvidia.com/cudnn) first according
   to https://opennmt.net/CTranslate2/installation.html to enable `faster-whisper`.

   `faster-whisper` also needs [cuBLAS for CUDA 11](https://developer.nvidia.com/cublas) installed.
   <details>
   <summary>For Windows Users (click to expand)</summary> 

   (For Windows Users only) Windows user can Download the libraries from Purfview's repository:

   Purfview's [whisper-standalone-win](https://github.com/Purfview/whisper-standalone-win) provides the required NVIDIA
   libraries for Windows in a [single archive](https://github.com/Purfview/whisper-standalone-win/releases/tag/libs).
   Decompress the archive and place the libraries in a directory included in the `PATH`.

   </details>


2. Add LLM API keys, you can either:
    - Add your [OpenAI API key](https://platform.openai.com/account/api-keys) to environment variable `OPENAI_API_KEY`.
    - Add your [Anthropic API key](https://console.anthropic.com/settings/keys) to environment
      variable `ANTHROPIC_API_KEY`.

3. Install [PyTorch](https://pytorch.org/get-started/locally/):
   ```shell
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

4. Install latest [fast-whisper](https://github.com/guillaumekln/faster-whisper)
   ```shell
   pip install git+https://github.com/guillaumekln/faster-whisper
   ```

5. Install [ffmpeg](https://ffmpeg.org/download.html) and add `bin` directory
   to your `PATH`.

6. This project can be installed from PyPI:

    ```shell
    pip install openlrc
    ```

   or install directly from GitHub:

    ```shell
    pip install git+https://github.com/zh-plus/openlrc
    ```

## Usage 🐍

### GUI

> [!NOTE]
> We are migrating the GUI from streamlit to Gradio. The GUI is still under development.

```shell
openlrc gui
```

![](https://github.com/zh-plus/openlrc/blob/master/resources/streamlit_app.jpg?raw=true)

### Python code

```python
from openlrc import LRCer

if __name__ == '__main__':
    lrcer = LRCer()

    # Single file
    lrcer.run('./data/test.mp3',
              target_lang='zh-cn')  # Generate translated ./data/test.lrc with default translate prompt.

    # Multiple files
    lrcer.run(['./data/test1.mp3', './data/test2.mp3'], target_lang='zh-cn')
    # Note we run the transcription sequentially, but run the translation concurrently for each file.

    # Path can contain video
    lrcer.run(['./data/test_audio.mp3', './data/test_video.mp4'], target_lang='zh-cn')
    # Generate translated ./data/test_audio.lrc and ./data/test_video.srt

    # Use context.yaml to improve translation
    lrcer.run('./data/test.mp3', target_lang='zh-cn', context_path='./data/context.yaml')

    # To skip translation process
    lrcer.run('./data/test.mp3', target_lang='en', skip_trans=True)

    # Change asr_options or vad_options, check openlrc.defaults for details
    vad_options = {"threshold": 0.1}
    lrcer = LRCer(vad_options=vad_options)
    lrcer.run('./data/test.mp3', target_lang='zh-cn')

    # Enhance the audio using noise suppression (consume more time).
    lrcer.run('./data/test.mp3', target_lang='zh-cn', noise_suppress=True)

    # Change the LLM model for translation
    lrcer = LRCer(chatbot_model='claude-3-sonnet-20240229')
    lrcer.run('./data/test.mp3', target_lang='zh-cn')

    # Clear temp folder after processing done
    lrcer.run('./data/test.mp3', target_lang='zh-cn', clear_temp_folder=True)

    # Change base_url
    lrcer = LRCer(base_url_config={'openai': 'https://api.chatanywhere.tech',
                                   'anthropic': 'https://api.g4f.icu'})

    # Bilingual subtitle
    lrcer.run('./data/test.mp3', target_lang='zh-cn', bilingual_sub=True)
```

Check more details in [Documentation](https://zh-plus.github.io/openlrc/#/).

### Context

Utilize the available context to enhance the quality of your translation.
Save them as `context.yaml` in the same directory as your audio file.

> [!NOTE]
> The improvement of translation quality from Context is **NOT** guaranteed.

```yaml
background: "This is a multi-line background.
This is a basic example."
audio_type: Movie
description_map: {
  movie_name1 (without extension): "This
  is a multi-line description for movie1.",
  movie_name2 (without extension): "This
  is a multi-line description for movie2.",
  movie_name3 (without extension): "This is a single-line description for movie 3.",
}
```

## Pricing 💰

*pricing data from [OpenAI](https://openai.com/pricing)
and [Anthropic](https://docs.anthropic.com/claude/docs/models-overview#model-comparison)*

| Model Name                 | Pricing for 1M Tokens <br/>(Input/Output) (USD) | Cost for 1 Hour Audio <br/>(USD) |
|----------------------------|-------------------------------------------------|----------------------------------|
| `gpt-3.5-turbo-0125`       | 0.5, 1.5                                        | 0.01                             |
| `gpt-3.5-turbo`            | 0.5, 1.5                                        | 0.01                             |
| `gpt-4-0125-preview`       | 10, 30                                          | 0.5                              |
| `gpt-4-turbo-preview`      | 10, 30                                          | 0.5                              |
| `claude-3-haiku-20240307`  | 0.25, 1.25                                      | 0.015                            |
| `claude-3-sonnet-20240229` | 3, 15                                           | 0.2                              |
| `claude-3-opus-20240229`   | 15, 75                                          | 1                                |

**Note the cost is estimated based on the token count of the input and output text.
The actual cost may vary due to the language and audio speed.**

### Recommended translation model

For english audio, we recommend using `gpt-3.5-turbo`.

For non-english audio, we recommend using `claude-3-sonnet-20240229`.

## Todo

- [x] [Efficiency] Batched translate/polish for GPT request (enable contextual ability).
- [x] [Efficiency] Concurrent support for GPT request.
- [x] [Translation Quality] Make translate prompt more robust according to https://github.com/openai/openai-cookbook.
- [x] [Feature] Automatically fix json encoder error using GPT.
- [x] [Efficiency] Asynchronously perform transcription and translation for multiple audio inputs.
- [x] [Quality] Improve batched translation/polish prompt according
  to [gpt-subtrans](https://github.com/machinewrapped/gpt-subtrans).
- [x] [Feature] Input video support.
- [X] [Feature] Multiple output format support.
- [x] [Quality] Speech enhancement for input audio.
- [ ] [Feature] Preprocessor: Voice-music separation.
- [ ] [Feature] Align ground-truth transcription with audio.
- [ ] [Quality]
  Use [multilingual language model](https://www.sbert.net/docs/pretrained_models.html#multi-lingual-models) to assess
  translation quality.
- [ ] [Efficiency] Add Azure OpenAI Service support.
- [ ] [Quality] Use [claude](https://www.anthropic.com/index/introducing-claude) for translation.
- [ ] [Feature] Add local LLM support.
- [X] [Feature] Multiple translate engine (Anthropic, Microsoft, DeepL, Google, etc.) support.
- [ ] [**Feature**] Build
  a [electron + fastapi](https://ivanyu2021.hashnode.dev/electron-django-desktop-app-integrate-javascript-and-python)
  GUI for cross-platform application.
- [x] [Feature] Web-based [streamlit](https://streamlit.io/) GUI.
- [ ] Add [fine-tuned whisper-large-v2](https://huggingface.co/models?search=whisper-large-v2) models for common
  languages.
- [x] [Feature] Add custom OpenAI & Anthropic endpoint support.
- [ ] [Feature] Add local translation model support (e.g. [SakuraLLM](https://github.com/SakuraLLM/Sakura-13B-Galgame)).
- [ ] [Others] Add transcribed examples.
    - [ ] Song
    - [ ] Podcast
    - [ ] Audiobook

## Credits

- https://github.com/guillaumekln/faster-whisper
- https://github.com/m-bain/whisperX
- https://github.com/openai/openai-python
- https://github.com/openai/whisper
- https://github.com/machinewrapped/gpt-subtrans
- https://github.com/MicrosoftTranslator/Text-Translation-API-V3-Python
- https://github.com/streamlit/streamlit

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=zh-plus/Open-Lyrics&type=Date)](https://star-history.com/#zh-plus/Open-Lyrics&Date)
