from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .lithologypipeline import calculate_composition,calculate_overall_composition
from .models import Composition
from .discontinuity_detection import detect
import os
import shutil
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
import keras
import pickle
import numpy as np
import json
def empty_directory(directory_path):
    # Check if the directory exists
    if os.path.exists(directory_path):
        # Remove all files and subdirectories within the directory
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        print(f"The directory {directory_path} does not exist.")
def index(request):
    return render(request,'mainpage.html')

@csrf_exempt
def predictComposition(request):
    empty_directory('static/temp_images/output')
    empty_directory('temp_images\input')
    print(request.FILES)
    fileObj=request.FILES['filePath']
    name=request.POST["name"]
    location=request.POST["location"]

    fs=FileSystemStorage()
    filePathName=fs.save(fileObj.name,fileObj)
    filePathName=fs.url(filePathName)
    testimage='.'+filePathName
    composition,composition_with_path=calculate_composition(testimage)
    discontinuities_image_path=detect(testimage)
    compositions=Composition(name=name,location=location,limestone_percentage=composition["limestone_percentage"],sandstone_percentage=composition["sandstone_percentage"],shale_percentage=composition["shale_percentage"],unknown_percentage=composition["unknown_percentage"])
    compositions.save()
    # print(composition)
    print(composition_with_path)
    no_of_images=len(composition_with_path)
    # context={'filePathName':filePathName,'predictedLabel':prediction_label}
    return render(request,'mainpage.html',{"compositions":composition,"composition_with_path":composition_with_path,"discontinuities_image_path":discontinuities_image_path,"len":no_of_images,'name':name,'location':location})


def dashboard(request):
    location = request.GET.get('location', None)
    created_at__gte = None

    # Get the time period selected via radio buttons
    time_period = request.GET.get('inputs', None)
    if time_period:
        # Define the logic to set created_at__gte based on the selected time period
        # For simplicity, I'll assume the time_period is in days
        if time_period == '1 Week':
            created_at__gte = datetime.now() - timedelta(weeks=1)
        elif time_period == '1 Month':
            created_at__gte = datetime.now() - timedelta(days=30)
        elif time_period == '6 Months':
            created_at__gte = datetime.now() - timedelta(days=180)
        elif time_period == '1 Year':
            created_at__gte = datetime.now() - timedelta(days=365)

    # Filter the queryset based on the provided filters
    queryset = Composition.objects.all()
    locations = Composition.objects.values_list('location', flat=True).all().distinct()
    if location:
        queryset = queryset.filter(location=location)
    if created_at__gte:
        queryset = queryset.filter(created_at__gte=created_at__gte)

    overall_composition=calculate_overall_composition(queryset.values())
    context = {'overall_composition': list(overall_composition.values())[:3],"locations":locations}
    return render(request, 'chart.html', context)

def chat(text):
    # load trained model
    chat_model = keras.models.load_model('/content/Chatbot.h5')

    # load tokenizer object
    with open('/content/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
    with open('/content/label_encoder.pickle', 'rb') as enc:
        label_encoder = pickle.load(enc)
    with open("intents.json") as file :
        data = json.load(file)

    # parameters
    max_len = 10

    while True:

        inp = input()
        if inp.lower() == "quit":
            break

        result = chat_model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                             truncating='post', maxlen=max_len))
        tag = label_encoder.inverse_transform([np.argmax(result)])


        for i in data['intents']:
            if i['tag'] == tag:
                return np.random.choice(i['responses'])

def chatbot(request):
    global d
    print("hi")
    if request.method == 'GET':            
        inp= request.GET.get('inp')
        print(inp)
    predictions=chat(inp)
    d[inp]=predictions
    return render(request,"chatbot.html",{"d":d})



