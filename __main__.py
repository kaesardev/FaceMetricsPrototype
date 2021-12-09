from deepface import DeepFace
from datetime import datetime
import cv2
from face import multi_face_detect
from input import Screencast, Webcam
from plot import Analytics
from argparse import ArgumentParser


def main(input):
    input.Start()

    while True:
        frame = input.CaptureFrame()
        # Capture timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Detect theq faces
        faces = multi_face_detect(frame)
        # Draw the rectangle around each face
        for (face, x0, y0, x1, y1) in faces:
            try:
                analyze = DeepFace.analyze(img_path = face, actions=['emotion'])
                dominant_emotion = analyze['dominant_emotion']
                Analytics.append(timestamp, analyze)
                # Draw detection emotion
                frame = cv2.rectangle(frame, (x0,y0), (x1, y1), (255,0,0), 2)
                frame = cv2.putText(frame, dominant_emotion, (x0, y1+16), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,0), 1, 0)
            except Exception as ex:
                pass
        # Display the resulting frame
        input.ShowFPS()
        cv2.imshow('Edu Metrics', input.GetFrame())
        cv2.imshow('Analytics: Predominant Emotions', Analytics.report1())
        # Stop recording
        if cv2.waitKey(1) == ord('q'):
            break
    # When everything done, release the capture
    input.Stop()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = ArgumentParser(description="Edu Metrics")
    parser.add_argument('--source', '-s', type=str, choices=['webcam', 'screen'], default='webcam', help='Source of capture.')
    parser.add_argument('--fps', '-f', type=bool, choices=[True, False], default=False, help='Display fps counter.')

    args = parser.parse_args()

    if (args.source == 'screen'):
        input = Screencast(show_fps=args.fps)
    else:
        input = Webcam(show_fps=args.fps)

    main(input)