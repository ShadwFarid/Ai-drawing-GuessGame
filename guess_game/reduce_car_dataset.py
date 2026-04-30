import os
import shutil
import random

# الفولدر الأصلي
source_folder = "dataset/car"

# الفولدر الجديد
output_folder = "dataset_balanced/car"

# عدد الصور المطلوب
target_count = 255

# إنشاء الفولدر الجديد
os.makedirs(output_folder, exist_ok=True)

# قراءة الصور
files = os.listdir(source_folder)

# فلترة (لو في ملفات غريبة)
files = [f for f in files if f.endswith((".png", ".jpg", ".jpeg"))]

print("Total images:", len(files))

# 👇 shuffle علشان ميبقاش في تحيز
random.shuffle(files)

# 👇 اختيار عدد معين
selected_files = files[:target_count]

# نسخ + إعادة التسمية
for i, file in enumerate(selected_files):
    src_path = os.path.join(source_folder, file)
    new_name = f"car_{i}.png"
    dst_path = os.path.join(output_folder, new_name)

    shutil.copy(src_path, dst_path)

print("Done! Reduced to", target_count)