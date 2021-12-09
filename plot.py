import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2

class Analytics:
    Columns = ['timestamp','angry','disgust','fear','happy','sad','surprise','neutral','dominant_emotion']
    Colors = ['#c0392b', '#8e44ad', '#16a085', '#f39c12', '#2980b9', '#d35400', '#34495e']
    Emotions = ['angry','disgust','fear','happy','sad','surprise','neutral']
    Data = []

    def append(timestamp, analyze):
        Analytics.Data.append({
            'timestamp': timestamp,
            'angry': analyze['emotion']['angry'],
            'disgust': analyze['emotion']['disgust'],
            'fear': analyze['emotion']['fear'],
            'happy': analyze['emotion']['happy'],
            'sad': analyze['emotion']['sad'],
            'surprise': analyze['emotion']['surprise'],
            'neutral': analyze['emotion']['neutral'],
            'dominant_emotion': analyze['dominant_emotion'],
        })

    def fig_to_frame(fig):
        # redraw the canvas
        fig.canvas.draw()
        
        # convert canvas to image
        frame = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        frame  = frame.reshape(fig.canvas.get_width_height()[::-1] + (3,))

        # img is rgb, convert to opencv's default bgr
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        return frame

    def report1():
        dataset = pd.DataFrame(Analytics.Data, columns=Analytics.Columns)
        
        labels = Analytics.Emotions
        colors = Analytics.Colors
        slices = [dataset[dataset.dominant_emotion == emotion].shape[0] for emotion in Analytics.Emotions]
        explode = (0, 0, 0, 0.1, 0, 0, 0)

        fig, ax = plt.subplots()
        ax.pie(slices, colors=colors, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)

        return Analytics.fig_to_frame(fig)
