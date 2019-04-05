from Config import Config
import os
import re
from gtts import gTTS


def say_something(txt, language):
	#use alsamixer to check which is which (is 0 recording? or is 1?)
	#os.system("espeak -ven+f3 -k5 -s150 '" + txt + "'")
	print("speaking " + language)
	sentences = ""
	paragraph = re.sub('[!,;:?.]','.',txt)
	for eachSentence in paragraph.split('.'):
		print(eachSentence)
		words = eachSentence.split()
		numWords = len(words)
		curSentence = 0
		curCharacters = 0
		curWord = 0
		for word in words:
			if curCharacters + len(word) + 1 < 100:
				sentences = sentences + ' ' + word
			else:
				curSentence = curSentence + 1
				sentences = sentences + "111" + word
				curCharacters = 0
			curCharacters = curCharacters + len(word)+1
			curWord = curWord + 1
		sentences = sentences + "111"

	feedTxt = sentences.split("111")
	for sentence in feedTxt:
		if len(sentence) > 2:
			# sentence = sentence.replace("'", "%27")
			print(sentence)
			# os.system("mpg123 -a hw:1 -q 'http://translate.google.com/translate_tts?tl=" + language + "&q=" + sentence + "'")
			spokenText = gTTS(text=sentence, lang=language, slow=False)

			# Saving the converted audio in a mp3 file named
			# welcome
			spokenText.save("spoken_text.mp3")

			# Playing the converted file
			os.system("mpg321 spoken_text.mp3")

			os.rmdir("spoken_text.mp3")

