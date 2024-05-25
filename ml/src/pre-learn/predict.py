import cv2
from PIL import Image
from ultralytics import YOLO

model = YOLO("weights/medium_50epoch.pt")

im1 = Image.open("data/yolo/all_images/study_0509_slice28.png")
results = model.predict(source=im1, save=True)