from keras.preprocessing import image
import torch
import cv2
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import pandas as pd
model = torch.hub.load('ultralytics/yolov5', 'custom', 'best_new.pt')  # custom trained model
mode_blank_space=torch.hub.load('ultralytics/yolov5', 'custom', 'best_blankspace.pt')

def draw_bounding_boxes(image_path, df):
    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Iterate through rows and draw bounding boxes with name
    for index, row in df.iterrows():
        xmin, ymin, xmax, ymax = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
        name = row['name']

        # Draw bounding box with reduced thickness
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)  # Green color for the bounding box

    # Draw text after drawing bounding boxes to avoid obscuring the text
    for index, row in df.iterrows():
        xmin, ymin, xmax, ymax = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
        name = row['name']

        # Set the font and text properties
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        font_thickness = 2 # Reduced thickness for the text
        font_color = (255,255, 0)  # Black text color

        # Calculate text size to determine position
        (text_width, text_height), baseline = cv2.getTextSize(f"{name}", font, font_scale, font_thickness)

        # Set a minimum vertical space between text and bounding box
        vertical_space = 3

        # Adjust the text position based on the bounding box
        text_position = (xmin, max(ymin - vertical_space, text_height + vertical_space))

        # Draw bounding box
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 1)  # Green color for the bounding box

        # Draw text on the image
        cv2.putText(image, f"{name}", text_position, font, font_scale, font_color, font_thickness, cv2.LINE_AA)

    # Display the image with bounding boxes and name
    return image
def detect(image_path):
  results = model("original.jpg")
  results_blank_space=mode_blank_space("original.jpg")
  results.xyxy[0]  # im predictions (tensor)
  results.pandas().xyxy[0]  # im predictions (pandas)
  df=results.pandas().xyxy[0] 
  results_blank_space.xyxy[0]  # im predictions (tensor)
  results_blank_space.pandas().xyxy[0]  # im predictions (pandas)
  df_b=results_blank_space.pandas().xyxy[0]
  result = pd.concat([df, df_b], ignore_index=True)
#   df=df[df["name"]>=0.6]
  #print(df)
  bound_image=draw_bounding_boxes("original.jpg", result)
  cv2.imwrite("static/temp_images/test.jpg",bound_image)
  return "temp_images/test.jpg"


def predict_discontinuities(request):
    #print (request)
    #print (request.POST.dict())
    fileObj=request.FILES['filePath']
    fs=FileSystemStorage()
    filePathName=fs.save(fileObj.name,fileObj)
    filePathName=fs.url(filePathName)
    testimage='.'+filePathName
    path=detect(testimage)
    return render(request,"index.html",{"image_path":path})