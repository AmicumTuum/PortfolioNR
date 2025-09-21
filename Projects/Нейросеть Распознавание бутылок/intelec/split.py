import os
import shutil
from sklearn.model_selection import train_test_split

# Пути к папкам
images_dir = 'plastic bottles'
annotations_dir = 'plastic bottles YOLO'
unlabeled_dir = 'unlabeled'

# Создаем папку для изображений без аннотаций
os.makedirs(unlabeled_dir, exist_ok=True)

# Считываем изображения
images = [os.path.join(images_dir, x) for x in os.listdir(images_dir) if x.endswith('.jpg')]  # Замените формат, если не JPG

# Список для изображений с аннотациями
images_with_annotations = []
annotations = []

# Проверяем наличие аннотации для каждого изображения
for image in images:
    annotation_file = os.path.join(annotations_dir, os.path.splitext(os.path.basename(image))[0] + '.txt')
    if os.path.exists(annotation_file):
        images_with_annotations.append(image)
        annotations.append(annotation_file)
    else:
        # Перемещаем изображения без аннотаций в папку unlabeled
        shutil.move(image, os.path.join(unlabeled_dir, os.path.basename(image)))

# Сортируем для соответствия
images_with_annotations.sort()
annotations.sort()

# Проверяем, чтобы количество изображений совпадало с количеством аннотаций
assert len(images_with_annotations) == len(annotations), "Число изображений и аннотаций не совпадает!"

# Разделяем на train, val, test
train_images, val_images, train_annotations, val_annotations = train_test_split(
    images_with_annotations, annotations, test_size=0.2, random_state=1
)

val_images, test_images, val_annotations, test_annotations = train_test_split(
    val_images, val_annotations, test_size=0.5, random_state=1
)

# Вывод для проверки
print(f"Train: {len(train_images)} images, {len(train_annotations)} annotations")
print(f"Validation: {len(val_images)} images, {len(val_annotations)} annotations")
print(f"Test: {len(test_images)} images, {len(test_annotations)} annotations")
print(f"Unlabeled: {len(os.listdir(unlabeled_dir))} images moved to '{unlabeled_dir}'")