from os import system
audioDir = '/Users/keyan/code/packages/keyutils/audio/lib/'
rightplace = '"Caroline Rose - year of the slug - 01 everything in its right place.wav"'
success = 'success.mp3'

def play(file: str):
    system(f"afplay {audioDir}{file}")
def success(): system(f"afplay {audioDir}success.mp3")
