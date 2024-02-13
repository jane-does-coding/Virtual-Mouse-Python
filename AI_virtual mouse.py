import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
MpDraw = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_x, index_y = screen_width // 2, screen_height // 2  # Start cursor at the center of the screen

# Smoothing factor
SMOOTHING_FACTOR = 0

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)

    frame_height, frame_width, _ = frame.shape
    rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgbFrame)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            MpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)
            landmarks = handLms.landmark
            for id, landmarks in enumerate(landmarks):
                x = int(landmarks.x * frame_width)
                y = int(landmarks.y * frame_height)

                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=20, color=(0, 255, 0))
                    # Smoothly update cursor position
                    index_x = int(index_x * (1 - SMOOTHING_FACTOR) + screen_width * x / frame_width * SMOOTHING_FACTOR)
                    index_y = int(index_y * (1 - SMOOTHING_FACTOR) + screen_height * y / frame_height * SMOOTHING_FACTOR)
                    pyautogui.moveTo(index_x, index_y)

                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=20, color=(0, 255, 0))
                    thumb_x = screen_width * x / frame_width
                    thumb_y = screen_height * y / frame_height

                    # Use a threshold combined with the smoothed cursor position
                    if abs(index_x - thumb_x) < 20 and abs(index_y - thumb_y) < 20:
                        pyautogui.click()
                        pyautogui.sleep(1)
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
