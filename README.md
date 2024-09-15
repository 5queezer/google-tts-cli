# Google Cloud Text-to-Speech Converter

This project provides a command-line tool to convert text to speech using **Google Cloud Text-to-Speech API**. You can specify the language, voice type, gender, and adjust parameters like pitch and speaking rate. Additionally, you can specify a general language prefix (e.g., `es` for Spanish), and the tool will show available voices across different accents/locales (e.g., `es-ES`, `es-MX`).

## Features
- Convert text to speech using Google Cloud Text-to-Speech.
- Choose different languages and voices (male, female, or neutral).
- Support for **WaveNet** and **Standard** voices.
- Specify general language prefixes to see available accents and locales.
- Adjust pitch and speaking rate for more natural or child-like voices.
- Generate filenames dynamically based on text content.
- Input text via file or command line.

## Requirements

- Python 3.x
- Google Cloud Text-to-Speech API credentials
- NLTK for stopwords processing

## Setup

### 1. Google Cloud Setup

#### Step 1: Create a Google Cloud Project
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or use an existing one.

#### Step 2: Enable the Google Cloud Text-to-Speech API
1. In your Google Cloud Console, go to **APIs & Services**.
2. Click **Enable APIs and Services**.
3. Search for **Text-to-Speech API** and enable it for your project.

#### Step 3: Create and Download Credentials
1. Go to the **Credentials** section in Google Cloud Console.
2. Click on **Create Credentials** and choose **Service Account**.
3. Download the JSON file for the service account.
4. Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the path of the downloaded JSON file:

   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-credentials.json"
   ```

### 2. Local Environment Setup

#### Step 1: Clone the repository
```bash
git clone https://github.com/5queezer/google-tts-cli.git
cd google-tts-cli
```

#### Step 2: Create a virtual environment and install dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Download NLTK Data (for stopwords)
The script uses NLTK for stopwords filtering based on the language. You'll need to download the required NLTK data.

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## Usage

### Convert text to speech (from command line)
You can provide the text directly in the command line with the `--text` option:

```bash
python tts.py --text "Hola, este es un ejemplo." --lang es --output example.mp3
```

### Convert text from a file
Alternatively, you can provide a text file using the `--file` option:

```bash
python tts.py --file input.txt --lang en --output output.mp3
```

### Specify Language Prefix
To specify a language prefix, such as `es` for Spanish, you can let the script show all available accents (e.g., `es-ES`, `es-MX`). The script will prompt you to select a voice if multiple accents/locales are available:

```bash
python tts.py --text "Hola, este es un ejemplo." --lang es --output example.mp3
```

### Choose different voice genders
You can specify the voice gender using the `--gender` option (male, female, or neutral):

```bash
python tts.py --text "Hello, this is an example." --lang en --gender female --output example_female.mp3
```

### Use WaveNet voices
To use WaveNet voices for higher quality audio, use the `--voice-type wavenet` option:

```bash
python tts.py --text "Hola, este es un ejemplo." --lang es --voice-type wavenet --output example_wavenet.mp3
```

### Adjust Pitch and Speaking Rate
You can adjust the **pitch** and **speaking rate** to create more dynamic or child-like voices:

```bash
python tts.py --text "Hola, este es un ejemplo." --lang es --pitch 7 --rate 1.2 --output child_like_voice.mp3
```

- **Pitch**: Default is `1.0`. Increase this value for a higher pitch.
- **Rate**: Default is `1.0`. Increase this value for faster speech.

### Available Options
- `--text`: Text to convert to speech (overrides file input).
- `--file`: File containing text to convert to speech.
- `--output`: Output MP3 file path (generated from text if not provided).
- `--lang`: Language prefix (e.g., `es` for Spanish, `en` for English).
- `--gender`: Voice gender (`male`, `female`, `neutral`), default: `neutral`.
- `--voice-type`: Voice type (`standard`, `wavenet`), default: `wavenet`.
- `--pitch`: Pitch of the voice, default is `1.0` (set to `7` for child-like voice).
- `--rate`: Speaking rate, default is `1.0` (set to `1.2` for child-like voice).

## Example Commands

### Example 1: Basic Conversion
```bash
python tts.py --text "Hola, este es un ejemplo." --output example.mp3
```

### Example 2: Text from a file with female WaveNet voice
```bash
python tts.py --file input.txt --lang en --gender female --voice-type wavenet --output example_female_wavenet.mp3
```

### Example 3: Child-like voice with adjusted pitch and rate
```bash
python tts.py --text "Hola, este es un ejemplo." --lang es --pitch 7 --rate 1.2 --output child_like_voice.mp3
```

## License
This project is licensed under the MIT License.

---

This updated README includes detailed instructions on how to use the language prefix feature, how to choose voices, adjust pitch and rate, and other options in your command-line tool. Let me know if you need more adjustments!