from django.shortcuts import render
from django.http import JsonResponse
import openai
import speech_recognition as sr
import pyaudio

openai.api_key = "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"

def process_speech(request):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Speak Anything')
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            print('You said: {}'.format(text))
        except sr.UnknownValueError:
            return JsonResponse({'error': 'Could not recognize your voice'})
        except sr.RequestError as e:
            return JsonResponse({'error': f'Recognition request failed: {e}'})

    prompt0 = "다음 문장을 한국어로 해석해줘\n" + text
    completion_trans = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You have a good grasp of Korean grammar."},
            {"role": "user", "content": prompt0}
        ]
    )

    prompt1 = completion_trans.choices[0].message.content
    prompt1 = "다음 문장의 문법을 올바르게 수정해줘\n" + prompt1

    completion_gram = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You have a good grasp of Korean grammar."},
            {"role": "user", "content": prompt1}
        ]
    )

    prompt2 = completion_gram.choices[0].message.content
    prompt2 = "다음 문장을 하십시오체, 하오체, 하게체, 해라체, 해요체, 해체로 상대높임 표현으로 바꿔줘\n" + prompt2

    completion_up = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You have a good grasp of Korean grammar."},
            {"role": "user", "content": prompt2}
        ]
    )

    result = completion_up.choices[0].message.content

    return JsonResponse({'result': result})
