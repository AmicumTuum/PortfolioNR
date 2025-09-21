import xml.etree.ElementTree as ET
import os
import glob

# Путь к папке с XML файлами и изображениям
xml_folder = 'plastic bottles YOLO'
image_folder = 'plastic bottles'
output_folder = 'labels'

# Преобразование координат XML в формат YOLO
def convert_xml_to_yolo(xml_file, image_width, image_height):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    yolo_annotations = []
    
    for member in root.findall('object'):
        class_name = member.find('name').text
        class_id = 0  # Замените на соответствующий ID класса, если их несколько
        bndbox = member.find('bndbox')
        
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)
        
        # Преобразуем координаты в формат YOLO (центр, ширина, высота)
        x_center = (xmin + xmax) / 2.0 / image_width
        y_center = (ymin + ymax) / 2.0 / image_height
        width = (xmax - xmin) / float(image_width)
        height = (ymax - ymin) / float(image_height)
        
        # Формат YOLO: class_id x_center y_center width height
        yolo_annotations.append(f"{class_id} {x_center} {y_center} {width} {height}")
    
    return yolo_annotations

# Основная функция для конвертации всех XML в формат YOLO
def convert_all_xml_to_yolo():
    xml_files = glob.glob(os.path.join(xml_folder, "*.xml"))
    
    for xml_file in xml_files:
        # Извлечение имени изображения из XML файла
        image_file = os.path.splitext(os.path.basename(xml_file))[0] + '.jpg'
        image_path = os.path.join(image_folder, image_file)
        
        # Получаем размеры изображения (ширина и высота)
        from PIL import Image
        with Image.open(image_path) as img:
            image_width, image_height = img.size
        
        # Преобразуем XML аннотации в YOLO
        yolo_annotations = convert_xml_to_yolo(xml_file, image_width, image_height)
        
        # Сохраняем аннотации в текстовый файл
        yolo_file = os.path.splitext(os.path.basename(xml_file))[0] + '.txt'
        yolo_file_path = os.path.join(output_folder, yolo_file)
        
        with open(yolo_file_path, 'w') as f:
            for annotation in yolo_annotations:
                f.write(f"{annotation}\n")

# Запуск конвертации
convert_all_xml_to_yolo()
