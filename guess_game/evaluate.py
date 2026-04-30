import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt

# -----------------------
# Load model
# -----------------------
model = load_model("cnn_model.h5")

# -----------------------
# Labels
# -----------------------
labels = ["car", "sun", "house", "triangle", "square"]

# -----------------------
# Preprocess (نفس اللي عندك)
# -----------------------
def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (28, 28))
    inverted = 255 - resized
    normalized = inverted / 255.0
    return normalized

# -----------------------
# Load dataset
# -----------------------
X = []
y = []

for label_index, label in enumerate(labels):
    folder = f"dataset/{label}"

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        img = cv2.imread(path)
        if img is None:
            continue

        processed = preprocess(img)
        X.append(processed)
        y.append(label_index)

X = np.array(X).reshape(-1, 28, 28, 1)
y = np.array(y)

print("Total samples:", len(X))

# -----------------------
# Prediction
# -----------------------
y_pred_probs = model.predict(X)
y_pred = np.argmax(y_pred_probs, axis=1)

# -----------------------
# Accuracy
# -----------------------
accuracy = np.mean(y_pred == y)
print("Accuracy:", accuracy)

# -----------------------
# Confusion Matrix
# -----------------------
cm = confusion_matrix(y, y_pred)

print("\nConfusion Matrix:\n", cm)

# -----------------------
# Plot Confusion Matrix
# -----------------------
plt.imshow(cm)
plt.title("Confusion Matrix")
plt.colorbar()

plt.xticks(range(len(labels)), labels, rotation=45)
plt.yticks(range(len(labels)), labels)

plt.xlabel("Predicted")
plt.ylabel("Actual")

# كتابة الأرقام جوه المربعات
for i in range(len(labels)):
    for j in range(len(labels)):
        plt.text(j, i, cm[i, j], ha='center', va='center')

plt.tight_layout()
plt.show()

# -----------------------
# Classification Report
# -----------------------
print("\nClassification Report:\n")
print(classification_report(y, y_pred, target_names=labels))