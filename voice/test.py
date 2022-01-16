from gtts import gTTS 

text = '안녕하세요, 파이썬 입문 스터디입니다. 한번 열심히 해서 파이썬 사용법을 마스터해봐요!'
tts = gTTS( text=text, lang='ko', slow=False ) 
tts.save('Insa.mp3') 

text = '헌법, 제2장 국민의 권리와 의무. \
    제10조 모든 국민은 인간으로서의 존엄과 가치를 가지며, 행복을 추구할 권리를 가진다. \
        국가는 개인이 가지는 불가침의 기본적 인권을 확인하고 이를 보장할 의무를 진다.'

tts = gTTS( text=text, lang='ko', slow=False)
tts.save('Bubjo.mp3')


rap = 'Look, If you had One shot, Or one opportunity, \
    To seize everything you ever wanted In one moment. \
        Would you capture it, Or just let it slip?'

tts = gTTS( text=rap, lang='ko', slow=False )
tts.save('Hanguksik.mp3')

tts = gTTS( text=rap, lang='en', slow=False )
tts.save('LoseYourself.mp3')

tts = gTTS( text=rap, lang='en', tld='co.uk', slow=False )
tts.save('LoseYourself_UK.mp3')


text = '你好，我是第一次学习中文。'
tts = gTTS( text=text, lang='zh-CN', slow=False )
tts.save('Mandarin.mp3')

print(type(tts))
print(tts)