import edge_tts
import asyncio
import os
from pydub import AudioSegment
from pydub.playback import play
from pydub.exceptions import CouldntDecodeError
from langcodes import Language

async def sample_all_voices():
    # List of available voices
    voices = await edge_tts.list_voices()

    # Filter only English voices
    english_voices = [voice for voice in voices if voice['Locale'].startswith('en')]

    # Group voices by language using langcodes for full language names
    languages = {}
    for voice in english_voices:
        lang_code = voice['Locale']
        lang_name = Language.get(lang_code).display_name()  # Get the full language name
        if lang_name not in languages:
            languages[lang_name] = []
        languages[lang_name].append(voice)

    for lang_name, voices in languages.items():
        print(f"\n{'='*20} Language: {lang_name} {'='*20}\n")
        
        # Create a folder for each language
        if not os.path.exists(lang_name):
            os.makedirs(lang_name)
        
        for voice in voices:
            # Generate the spoken text including name, language, location, and gender
            spoken_text = (
                f"This is the voice of {voice['Name']}. "
                f"speaking {lang_name}. "
                f"from {voice['Locale']}."
            )
            print(spoken_text)

            output_filename = os.path.join(lang_name, f"{voice['ShortName']}.mp3")
            communicate = edge_tts.Communicate(spoken_text, voice=voice['ShortName'])
            await communicate.save(output_filename)

            print(f"Sample saved as: {output_filename}")
            print(f"Playing {voice['Name']} sample...\n")

            # Play the generated sound using pydub with error handling
            try:
                sound = AudioSegment.from_file(output_filename)
                play(sound)
            except CouldntDecodeError:
                print(f"Could not play {output_filename}. There might be an issue with FFmpeg or the file format.")

if __name__ == "__main__":
    asyncio.run(sample_all_voices())
