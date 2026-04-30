import os
import shutil

# كل الفولدرات اللي فيها داتا
source_folders = [
    '/Users/mac/Downloads/ali' ,
    '/Users/mac/Downloads/engy',
    '/Users/mac/Downloads/norhan',
    '/Users/mac/Downloads/shadw',
   '/Users/mac/Downloads/yousef '
    
]

# الكلاسات
labels = [ "sun", "house", "triangle", "square", "car"]

# الفولدر النهائي
output_base = "dataset"

for label in labels:
    output_path = os.path.join(output_base, label)
    os.makedirs(output_path, exist_ok=True)

    counter = 0

    for folder in source_folders:
        source_path = os.path.join(folder, label)

        if not os.path.exists(source_path):
            continue

        for file in os.listdir(source_path):
            src_file = os.path.join(source_path, file)

            # اسم جديد للصورة
            new_name = f"{label}_{counter}.png"
            dst_file = os.path.join(output_path, new_name)

            shutil.copy(src_file, dst_file)

            counter += 1

print("Merge done successfully!")