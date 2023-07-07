import cv2
import os
from main import GeneratePCD
angles = 4


def save_frame(video_path, result_path, ext=".jpg"):
    cap = cv2.VideoCapture(video_path)
    count = 1
    if not cap.isOpened():
        return
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    inc = int(frames / angles)
    print(inc)
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    while frames > angles:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frames - 1)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(result_path + str(count) + ext, frame)
            count = count + 1
            frames = frames - inc
    print("done")


def callVideoPath(subject, ang):
    global angles
    angles = ang
    save_frame('data/additional_vid/'+subject+'.mp4', 'data/auto/results/'+subject+'/'+str(angles)+'/')
    obj = GeneratePCD()
    obj.main_caller(subject, angles)


for i in range(4, 13, 2):
    callVideoPath("apple_bruise", i)
#save_frame('data/fruits_vid/lime.mp4', 'data/temp/result_single/')
