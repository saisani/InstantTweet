import re
import sys

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue

import threading
import time

import smtplib

# AUDIO RECORDING FORMAT
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

# EMAIL CONFIGURATION
GMAIL_USER = 'fall8731@gmail.com'
GMAIL_PASSWORD = '<add gmail password here>'

sent_from = GMAIL_USER
to = ['fall8731.3las2i@zapiermail.com']
subject = '#IFTTT'

# list to store phrases, will be a little redundant
completed_phrases = []

# limit for IFTTT connections
IFTTT_LIMIT = 750
EMAIL_DELAY = 10
EMAIL_COUNTER = 0

# text file to write out phrases being sent
TEXT_FILE_PATH = "spoken_phrases.txt"


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)

def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        # overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if result.is_final:
        	completed_phrases.append(transcript)

    	# program will exit if speaker says exit or quit
    	# if re.search(r'\b(exit|quit)\b', transcript, re.I):
        #     print('Exiting..')
        #     break

def generate_email_text(phrase):			
	email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, phrase)

	return email_text

EMAIL_COUNTER = 0
def send_to_email(EMAIL_COUNTER, EMAIL_DELAY, IFTTT_LIMIT):
	while(True):

		if(len(completed_phrases) == 0):
			continue

		# if too long to tweet, skip
		spoken_phrase = completed_phrases[0]
		if(len(spoken_phrase) >= 280):
			completed_phrases.pop(0)
			continue

		try:
			server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
			server.ehlo()
			server.login(GMAIL_USER, GMAIL_PASSWORD)

			email_text = generate_email_text(completed_phrases[0])

			server.sendmail(sent_from, to, email_text)
			server.close()

			# writes to text file with timestamp and message
			ts = time.localtime()
			line_to_write = "" + time.strftime("%x %X ", ts) + completed_phrases[0] + "\n"
			with open(TEXT_FILE_PATH, "a") as text_file:
				text_file.write(line_to_write)

			print("EMAIL HAS SENT!" + " Message: " + completed_phrases[0])

			# removing first element to avoid huge accumulation
			if(len(completed_phrases) > 0):
				completed_phrases.pop(0)
		except:
			print("EMAIL SENDING HAS FAILED")

		time.sleep(EMAIL_DELAY)

def main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'en-US'  # a BCP-47 language tag

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    print("STARTING AUDIO TRANSCRIPTION. Feel free to talk into the mic")

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        #print("Processing New Stream")
        try:
            responses = client.streaming_recognize(streaming_config, requests)
            listen_print_loop(responses)
        except Exception as exception:
            print("Stream was open too long. RESTARTING STREAM NOW")
            


if __name__ == '__main__':

	# starting email sending thread
    emailThread = threading.Thread(target=send_to_email, args=(EMAIL_COUNTER, EMAIL_DELAY, IFTTT_LIMIT, ))
    emailThread.daemon = True
    emailThread.start()
    
    # kicking off main thread
    while True:
        main()

    # stop thread
    emailThread.join()
