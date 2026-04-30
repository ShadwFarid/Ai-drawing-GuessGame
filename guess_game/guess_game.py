import cv2
import numpy as np
import os
from tensorflow.keras.models import load_model


model = load_model("cnn_model.h5")

def preprocess(img):
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (28, 28))
    
    # نعكس الألوان (علشان الخلفية تبقى سودا)
    inverted = 255 - resized
    
    # normalize
    normalized = inverted / 255.0
    
    return normalized


# predict function

labels = ["car", "sun", "house", "triangle", "square"]

def predict(image_array):
    img = image_array.reshape(1, 28, 28, 1)
    prediction = model.predict(img, verbose=0)

    index = np.argmax(prediction)
    confidence = prediction[0][index]

    return labels[index], confidence
# --------------------
# dataset setup
# --------------------

# 👇 1. إنشاء الفولدرات الأول
for label in labels:
    os.makedirs(f"dataset/{label}", exist_ok=True)

# 👇 2. بعد كده نحسب الصور
counters = {}

for label in labels:
    path = f"dataset/{label}"
    existing_files = os.listdir(path)
    counters[label] = len(existing_files)

# --------------------
# الرسم
# --------------------

canvas = np.ones((400, 400, 3), dtype="uint8") * 255

drawing = False
last_x, last_y = None, None

color = (0, 0, 0)  # أسود
thickness = 8 

def draw(event, x, y, flags, param):
    global drawing, last_x, last_y, canvas, color, thickness

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        last_x, last_y = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        # if drawing:
        #     # 👇 نرسم خط بدل نقطة
        #     cv2.line(canvas, (last_x, last_y), (x, y), color, thickness)
        #     last_x, last_y = x, y
        if drawing:
                    dx = x - last_x
                    dy = y - last_y
                    distance = max(abs(dx), abs(dy))

                    for i in range(distance):
                        xi = int(last_x + dx * i / distance)
                        yi = int(last_y + dy * i / distance)
                        cv2.circle(canvas, (xi, yi), thickness//2, color, -1)

                    last_x, last_y = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        last_x, last_y = None, None

cv2.namedWindow("Draw")
cv2.setMouseCallback("Draw", draw)

while True:
    # cv2.namedWindow("Draw", cv2.WINDOW_NORMAL)
    cv2.imshow("Draw", canvas)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        break

    elif key == ord('c'):
        canvas[:] = 255

    elif key == ord('s'):
        
        cv2.imwrite("drawing.png", canvas)
        print("Saved!")
    elif key == ord('g'):
        img = canvas.copy()
        processed = preprocess(img)

        label, conf = predict(processed)
        print(f"AI Guess: {label} ({conf:.2f})")


        # to prevent overlaping for text 
        canvas[0:60, 0:200] = 255

        # write answer in drawing 
        cv2.putText(canvas, label, (10, 40),cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 2)

    elif key == ord('e'):
        color = (255, 255, 255)
        thickness = 20
        print("Eraser ON")

    elif key == ord('b'):
        color = (0, 0, 0)
        thickness = 8
        print("Pen ON")


    elif key == ord('1'):
        filename = f"dataset/car/car_{counters['car']}.png"
        cv2.imwrite(filename, canvas)
        counters['car'] += 1
        print("Saved CAR")

    elif key == ord('2'):
        filename = f"dataset/sun/sun_{counters['sun']}.png"
        cv2.imwrite(filename, canvas)
        counters['sun'] += 1
        print("Saved SUN")

    elif key == ord('3'):
        filename = f"dataset/house/house_{counters['house']}.png"
        cv2.imwrite(filename, canvas)
        counters['house'] += 1
        print("Saved HOUSE")
    elif key == ord('4'):
        filename = f"dataset/triangle/triangle_{counters['triangle']}.png"
        cv2.imwrite(filename, canvas)
        counters['triangle'] += 1
        print("Saved TRIANGLE")

    elif key == ord('5'):
        filename = f"dataset/square/square_{counters['square']}.png"
        cv2.imwrite(filename, canvas)
        counters['square'] += 1
        print("Saved SQUARE")
cv2.destroyAllWindows()
