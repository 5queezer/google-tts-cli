import click
import re
from google.cloud import texttospeech
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK resources if not available
nltk.download('punkt')
nltk.download('stopwords')


def get_available_voices(client, language_prefix, gender):
    """Fetch the available voices from Google Cloud for the given language prefix and gender."""
    voices = client.list_voices()
    matched_voices = []

    gender_map = {
        'male': texttospeech.SsmlVoiceGender.MALE,
        'female': texttospeech.SsmlVoiceGender.FEMALE,
        'neutral': texttospeech.SsmlVoiceGender.NEUTRAL
    }

    for voice in voices.voices:
        for language_code in voice.language_codes:
            if language_code.startswith(language_prefix) and voice.ssml_gender == gender_map[gender]:
                matched_voices.append(voice.name)

    if not matched_voices:
        raise click.UsageError(f"No available voices found for language '{language_prefix}' and gender '{gender}'")

    return matched_voices


def select_voice(available_voices, voice_type):
    """Prompt the user to select a voice if multiple matches are found."""
    matched_voices = [v for v in available_voices if voice_type in v.lower()]

    if len(matched_voices) == 1:
        return matched_voices[0]  # Only one voice matches, return it

    elif len(matched_voices) > 1:
        # If multiple voices match, prompt the user to choose
        click.echo(f"\nMultiple voices found for {voice_type}:")
        for idx, voice in enumerate(matched_voices):
            click.echo(f"{idx + 1}. {voice}")

        # Ask the user to select one of the available voices
        choice = click.prompt(f"\nEnter the number of the voice you want to use (1-{len(matched_voices)})", type=int)

        # Ensure the user input is valid
        if 1 <= choice <= len(matched_voices):
            return matched_voices[choice - 1]
        else:
            raise click.UsageError("Invalid choice! Please run the command again and select a valid option.")

    else:
        # No specific match for voice_type, return the first available voice
        return available_voices[0]


def generate_filename_from_text(text, lang_code):
    """
    Generate a filename based on text and language.
    Use up to 3 keywords from the text, ignoring stopwords for the specified language.
    """
    # Remove non-alphabetical characters and tokenize
    words = word_tokenize(re.sub(r'[^a-zA-Z\s]', '', text.lower()))

    # Get stopwords for the language, fallback to no stopwords if the language is unsupported
    try:
        stop_words = set(stopwords.words(lang_code.split('-')[0]))
    except OSError:
        stop_words = set()

    filtered_words = [word for word in words if word not in stop_words]

    # Take up to 3 keywords to generate a filename
    keywords = '_'.join(filtered_words[:3]) if filtered_words else 'speech'

    return f"{keywords}.mp3"


@click.command()
@click.option('--text', default=None, help='Text to convert to speech (overrides file input).')
@click.option('--file', type=click.File('r'), default=None, help='File containing text to convert to speech.')
@click.option('--output', default=None, help='Output MP3 file path (generated from text if not provided).')
@click.option('--lang', default='es', help='Language prefix (e.g., es for Spanish, en for English).')
@click.option('--gender', default='neutral', type=click.Choice(['male', 'female', 'neutral']),
              help='Voice gender (male, female, or neutral), default is neutral.')
@click.option('--voice-type', default='wavenet', type=click.Choice(['standard', 'wavenet']),
              help='Voice type (standard or wavenet), default is wavenet.')
@click.option('--pitch', default=1.0, help='Pitch of the voice, set to 7 for a child-like voice.')
@click.option('--rate', default=1.0, help='Speaking rate, set to 1.2 for a child-like voice.')
def tts(text, file, output, lang, gender, voice_type, pitch, rate):
    """
    Convert text to speech using Google Cloud Text-to-Speech in any language with child-like voice adjustments.
    """
    # Initialize client
    client = texttospeech.TextToSpeechClient()

    # Read text from command line or file
    if text is None and file is not None:
        text = file.read()
    elif text is None:
        raise click.UsageError("You must provide either --text or --file.")

    # Generate a filename from the text if no output is specified
    if output is None:
        output = generate_filename_from_text(text, lang)

    # Fetch available voices for the language prefix and gender
    available_voices = get_available_voices(client, lang, gender)

    # Prompt user to select a voice if multiple matches are found
    selected_voice = select_voice(available_voices, voice_type)

    # Handle gender options correctly
    if gender == 'male':
        ssml_gender = texttospeech.SsmlVoiceGender.MALE
    elif gender == 'female':
        ssml_gender = texttospeech.SsmlVoiceGender.FEMALE
    else:
        ssml_gender = texttospeech.SsmlVoiceGender.NEUTRAL

    # Set up the voice request based on the specified language, gender, and type
    voice = texttospeech.VoiceSelectionParams(
        language_code=lang,
        name=selected_voice,
        ssml_gender=ssml_gender  # Corrected for enum
    )

    # Set the audio file format and modify pitch and rate for child-like voice
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,  # Corrected for enum
        pitch=pitch,  # Increase pitch to make the voice sound higher
        speaking_rate=rate  # Slightly increase speaking rate for child-like speech
    )

    # Perform the text-to-speech request
    synthesis_input = texttospeech.SynthesisInput(text=text)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Save the audio to a file
    with open(output, "wb") as out:
        out.write(response.audio_content)
        click.echo(f"Audio content written to file '{output}'")


if __name__ == "__main__":
    tts()
