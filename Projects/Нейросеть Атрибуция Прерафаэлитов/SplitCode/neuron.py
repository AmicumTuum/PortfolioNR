import os
from keras.preprocessing.image import ImageDataGenerator

# Пути к папкам с данными
data_dir = '/путь/к/основной/папке/датасета'
train_dir = os.path.join(data_dir, 'тренировочный')
validation_dir = os.path.join(data_dir, 'валидационный')
test_dir = os.path.join(data_dir, 'тестовый')

# Размер изображений
img_size = (224, 224)

# Создание генератора изображений
datagen = ImageDataGenerator(rescale=1./255)

# Генераторы данных для тренировочного, валидационного и тестового наборов
train_generator = datagen.flow_from_directory(
    train_dir,
    target_size=img_size,
    batch_size=32,
    class_mode='binary'  # 'categorical' для нескольких классов
)

validation_generator = datagen.flow_from_directory(
    validation_dir,
    target_size=img_size,
    batch_size=32,
    class_mode='binary'
)

test_generator = datagen.flow_from_directory(
    test_dir,
    target_size=img_size,
    batch_size=32,
    class_mode='binary'
)

# Пример использования генератора данных в модели Keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(1, activation='sigmoid'))  # 'softmax' для нескольких классов

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Обучение модели
model.fit(
    train_generator,
    epochs=10,
    validation_data=validation_generator
)

# Оценка модели на тестовом наборе данных
test_loss, test_accuracy = model.evaluate(test_generator)
print(f'Test Accuracy: {test_accuracy}')