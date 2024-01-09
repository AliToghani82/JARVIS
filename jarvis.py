import openai
import speech_recognition as sr
import boto3
import vlc
# Set up OpenAI API key and engine
openai.api_key = ""
engine_id = "text-davinci-003"

polly_client = boto3.Session(
        aws_access_key_id='',
        aws_secret_access_key='',
        region_name='us-west-2').client('polly')
# Initialize speech recognition engine
r = sr.Recognizer()

# Set the timeout for the audio input to 5 seconds
timeout = 10  # seconds
# Start listening for audio input with timeout
x = 1
while(x):
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Say something...")
        audio = r.listen(source, timeout=timeout)

    # Attempt to recognize the audio input
    try:
        command = r.recognize_google(audio)
        print(command)
        if(command.startswith('Jarvis')):
            response = openai.Completion.create(
                engine=engine_id,
                prompt=command,
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.5
            )
            completion = response.choices[0].text
            print(completion)
            # Set up the voice configuration
            voice = {
                'LanguageCode': 'en-GB',
                'Name': 'Arthur'
            }
            response = polly_client.synthesize_speech(
                Text=completion,
                OutputFormat='mp3',
                VoiceId=voice['Name'],
                Engine="neural")
            # Save the audio file
            with open('output.mp3', 'wb') as file:
                file.write(response['AudioStream'].read())
            p = vlc.MediaPlayer("output.mp3")
            p.play()
            while p.get_state() != vlc.State.Ended:
                pass
        elif(command.startswith('bye Jarvis')):
            text = "Alright my sir, have a good rest of your day"
            voice = {
                'LanguageCode': 'en-GB',
                'Name': 'Arthur'
            }
            response = polly_client.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                VoiceId=voice['Name'],
                Engine="neural")
            # Save the audio file
            with open('output.mp3', 'wb') as file:
                file.write(response['AudioStream'].read())
            p = vlc.MediaPlayer("output.mp3")
            p.play()
            break
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Error: {0}".format(e))
