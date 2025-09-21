import os
import shutil
from sklearn.model_selection import train_test_split

# Путь к основной папке датасета
data_dir = "C:/Users/Alex/Desktop/DataSet"

# Создаем папки train, validation и test внутри основной папки
train_dir = os.path.join(data_dir, 'train')
validation_dir = os.path.join(data_dir, 'validation')
test_dir = os.path.join(data_dir, 'test')

os.makedirs(train_dir, exist_ok=True)
os.makedirs(validation_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Получаем список классов
classes = os.listdir(data_dir)

# Разделение каждого класса на train, validation и test
for class_name in classes:
    class_dir = os.path.join(data_dir, class_name)

    # Получаем список файлов для текущего класса
    files = os.listdir(class_dir)

    # Разделяем на тренировочный, валидационный и тестовый наборы
    train_files, test_val_files = train_test_split(files, test_size=0.3, random_state=42)
    val_files, test_files = train_test_split(test_val_files, test_size=0.5, random_state=42)

    # Создаем подпапки для каждого набора данных
    train_class_dir = os.path.join(train_dir, class_name)
    validation_class_dir = os.path.join(validation_dir, class_name)
    test_class_dir = os.path.join(test_dir, class_name)

    os.makedirs(train_class_dir, exist_ok=True)
    os.makedirs(validation_class_dir, exist_ok=True)
    os.makedirs(test_class_dir, exist_ok=True)

    # Копируем файлы в соответствующие подпапки
    for file in train_files:
        shutil.copy(os.path.join(class_dir, file), os.path.join(train_class_dir, file))

    for file in val_files:
        shutil.copy(os.path.join(class_dir, file), os.path.join(validation_class_dir, file))

    for file in test_files:
        shutil.copy(os.path.join(class_dir, file), os.path.join(test_class_dir, file))
