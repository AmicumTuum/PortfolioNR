import os
import shutil
from sklearn.model_selection import train_test_split

# Пути к исходным папкам
images_dir = 'plastic bottles'
annotations_dir = 'plastic bottles YOLO'

# Папки для выходных данных
output_dirs = {
    'images/train': 'images/train',
    'images/val': 'images/val',
    'images/test': 'images/test',
    'annotations/train': 'annotations/train',
    'annotations/val': 'annotations/val',
    'annotations/test': 'annotations/test',
    'unlabeled': 'unlabeled',  # Папка для изображений без аннотаций
}

# Создаем выходные папки
for dir_path in output_dirs.values():
    os.makedirs(dir_path, exist_ok=True)

# Утилита для перемещения файлов
def move_files_to_folder(list_of_files, destination_folder):
    for f in list_of_files:
        try:
            shutil.move(f, destination_folder)
        except Exception as e:
            print(f"Ошибка при перемещении файла {f}: {e}")

# Считываем изображения и аннотации
images = [os.path.join(images_dir, x) for x in os.listdir(images_dir) if x.endswith('.jpg')] 
images_with_annotations = []
annotations = []

# Проверяем наличие аннотаций
for image in images:
    annotation_file = os.path.join(annotations_dir, os.path.splitext(os.path.basename(image))[0] + '.txt')
    if os.path.exists(annotation_file):
        images_with_annotations.append(image)
        annotations.append(annotation_file)
    else:
        # Перемещаем изображения без аннотаций
        shutil.move(image, os.path.join(output_dirs['unlabeled'], os.path.basename(image)))

# Сортируем
images_with_annotations.sort()
annotations.sort()

# Проверяем соответствие размеров
assert len(images_with_annotations) == len(annotations), "Количество изображений и аннотаций не совпадает!"

# Разделяем на train, val, test
train_images, val_images, train_annotations, val_annotations = train_test_split(
    images_with_annotations, annotations, test_size=0.2, random_state=1
)

val_images, test_images, val_annotations, test_annotations = train_test_split(
    val_images, val_annotations, test_size=0.5, random_state=1
)

# Перемещаем данные в папки
move_files_to_folder(train_images, output_dirs['images/train'])
move_files_to_folder(val_images, output_dirs['images/val'])
move_files_to_folder(test_images, output_dirs['images/test'])
move_files_to_folder(train_annotations, output_dirs['annotations/train'])
move_files_to_folder(val_annotations, output_dirs['annotations/val'])
move_files_to_folder(test_annotations, output_dirs['annotations/test'])

# Итоговая информация
print(f"Train: {len(train_images)} images, {len(train_annotations)} annotations")
print(f"Validation: {len(val_images)} images, {len(val_annotations)} annotations")
print(f"Test: {len(test_images)} images, {len(test_annotations)} annotations")
print(f"Unlabeled: {len(os.listdir(output_dirs['unlabeled']))} images moved to '{output_dirs['unlabeled']}'")
