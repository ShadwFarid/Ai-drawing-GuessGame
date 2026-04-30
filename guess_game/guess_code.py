# import os
# import cv2
# import numpy as np
# from tensorflow.keras import layers, models
# from tensorflow.keras.utils import to_categorical

# labels = ["cat", "sun", "house", "triangle", "square"]

# data = []
# targets = []

# # 📥 تحميل الصور
# for label_index, label in enumerate(labels):
#     path = f"dataset/{label}"
    
#     for file in os.listdir(path):
#         img_path = os.path.join(path, file)
#         img = cv2.imread(img_path)
        
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         resized = cv2.resize(gray, (28, 28))
#         inverted = 255 - resized
#         normalized = inverted / 255.0
        
#         data.append(normalized)
#         targets.append(label_index)

# # تحويل لـ numpy
# data = np.array(data).reshape(-1, 28, 28, 1)
# targets = to_categorical(targets)

# # 🧠 CNN Model
# model = models.Sequential([
#     layers.Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)),
#     layers.MaxPooling2D(2,2),

#     layers.Conv2D(64, (3,3), activation='relu'),
#     layers.MaxPooling2D(2,2),

#     layers.Flatten(),
#     layers.Dense(128, activation='relu'),
#     layers.Dense(len(labels), activation='softmax')
# ])

# model.compile(
#     optimizer='adam',
#     loss='categorical_crossentropy',
#     metrics=['accuracy']
# )

# # 🚀 تدريب
# model.fit(data, targets, epochs=10)

# # 💾 حفظ
# model.save("cnn_model.h5")

# print("Model trained and saved!")

import os
import cv2
import numpy as np
from tensorflow.keras import layers, models
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# --------------------
# الكلاسات
# --------------------
labels = ["car", "sun", "house", "triangle", "square"]

data = []
targets = []

# --------------------
# تحميل الصور
# --------------------
for label_index, label in enumerate(labels):
    path = f"dataset/{label}"

    for file in os.listdir(path):
        img_path = os.path.join(path, file)
        img = cv2.imread(img_path)

        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (28, 28))
        inverted = 255 - resized
        normalized = inverted / 255.0

        data.append(normalized)
        targets.append(label_index)

# --------------------
# تحويل البيانات
# --------------------
data = np.array(data).reshape(-1, 28, 28, 1)
targets = to_categorical(targets)

# --------------------
# تقسيم الداتا
# --------------------
X_train, X_val, y_train, y_val = train_test_split(
    data, targets,
    test_size=0.2,
    random_state=42
)

# --------------------
# الموديل
# --------------------
model = models.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Flatten(),

    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),

    layers.Dense(len(labels), activation='softmax')
])

# --------------------
# إعداد الموديل
# --------------------
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# --------------------
# التدريب
# --------------------
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=8,
    batch_size=32
)

# --------------------
# حفظ الموديل
# --------------------
model.save("cnn_model.h5")

print("✅ Model trained & saved!")