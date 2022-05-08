import base64

file = open('speech.wav', 'rb')
file_content = file.read()

file_string = base64.b64encode(file_content).decode('ascii')

wav_file = open("temp.wav", "wb")
decode_string = base64.b64decode(file_string)

wav_file.write(decode_string)
