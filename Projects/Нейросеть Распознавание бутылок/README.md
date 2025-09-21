# 🍼 Plastic Bottle Detection using YOLOv5

## 📌 Описание
Проект посвящён обучению модели **YOLOv5** для распознавания пластиковых бутылок на изображениях.  
Включает подготовку датасета, конвертацию аннотаций, разделение на train/val/test и обучение модели.  

---

## 📂 Содержание репозитория
- 📝 [Доклад](https://github.com/AmicumTuum/PortfolioNR/blob/main/Python/%D0%9D%D0%B5%D0%B9%D1%80%D0%BE%D1%81%D0%B5%D1%82%D1%8C%20%D0%A0%D0%B0%D1%81%D0%BF%D0%BE%D0%B7%D0%BD%D0%B0%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%B1%D1%83%D1%82%D1%8B%D0%BB%D0%BE%D0%BA/%D0%A0%D0%B0%D1%81%D0%BF%D0%BE%D0%B7%D0%BD%D0%B0%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%BF%D0%BB%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%BE%D0%B2%D1%8B%D1%85%20%D0%B1%D1%83%D1%82%D1%8B%D0%BB%D0%BE%D0%BA.pdf) - полный текст работы
- ⚙️ [Конфиг](https://github.com/AmicumTuum/PortfolioNR/blob/main/Python/%D0%9D%D0%B5%D0%B9%D1%80%D0%BE%D1%81%D0%B5%D1%82%D1%8C%20%D0%A0%D0%B0%D1%81%D0%BF%D0%BE%D0%B7%D0%BD%D0%B0%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%B1%D1%83%D1%82%D1%8B%D0%BB%D0%BE%D0%BA/intelec/dataset.py) — работа с датасетом  
- 🔗 [Работа с файлами](https://github.com/AmicumTuum/PortfolioNR/blob/main/Python/%D0%9D%D0%B5%D0%B9%D1%80%D0%BE%D1%81%D0%B5%D1%82%D1%8C%20%D0%A0%D0%B0%D1%81%D0%BF%D0%BE%D0%B7%D0%BD%D0%B0%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%B1%D1%83%D1%82%D1%8B%D0%BB%D0%BE%D0%BA/intelec/sharing.py) — проверка соответствия изображений и аннотаций
- ✂️ [Разделения датасета](https://github.com/AmicumTuum/PortfolioNR/blob/main/Python/%D0%9D%D0%B5%D0%B9%D1%80%D0%BE%D1%81%D0%B5%D1%82%D1%8C%20%D0%A0%D0%B0%D1%81%D0%BF%D0%BE%D0%B7%D0%BD%D0%B0%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%B1%D1%83%D1%82%D1%8B%D0%BB%D0%BE%D0%BA/intelec/split.py) — разделение датасета на train/val/test  
- 🤖[Запуск модели](https://github.com/AmicumTuum/PortfolioNR/blob/main/Python/%D0%9D%D0%B5%D0%B9%D1%80%D0%BE%D1%81%D0%B5%D1%82%D1%8C%20%D0%A0%D0%B0%D1%81%D0%BF%D0%BE%D0%B7%D0%BD%D0%B0%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%B1%D1%83%D1%82%D1%8B%D0%BB%D0%BE%D0%BA/intelec/training.py) — запуск обучения YOLOv5  
- 🔄 [Преобразование](https://github.com/AmicumTuum/PortfolioNR/blob/main/Python/%D0%9D%D0%B5%D0%B9%D1%80%D0%BE%D1%81%D0%B5%D1%82%D1%8C%20%D0%A0%D0%B0%D1%81%D0%BF%D0%BE%D0%B7%D0%BD%D0%B0%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%B1%D1%83%D1%82%D1%8B%D0%BB%D0%BE%D0%BA/intelec/xmltotxt.py) — конвертация аннотаций из XML (Pascal VOC) в YOLO format  

Папки:
- 📂 [Изображения](https://github.com/AmicumTuum/PortfolioNR/tree/main/Python/%D0%9D%D0%B5%D0%B9%D1%80%D0%BE%D1%81%D0%B5%D1%82%D1%8C%20%D0%A0%D0%B0%D1%81%D0%BF%D0%BE%D0%B7%D0%BD%D0%B0%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%B1%D1%83%D1%82%D1%8B%D0%BB%D0%BE%D0%BA/intelec/images) — изображения (train/val/test)  
- 🏷️ [Метки](https://github.com/AmicumTuum/PortfolioNR/tree/main/Python/%D0%9D%D0%B5%D0%B9%D1%80%D0%BE%D1%81%D0%B5%D1%82%D1%8C%20%D0%A0%D0%B0%D1%81%D0%BF%D0%BE%D0%B7%D0%BD%D0%B0%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%B1%D1%83%D1%82%D1%8B%D0%BB%D0%BE%D0%BA/intelec/labels) — метки в YOLO формате (train/val/test)  

---

## 🔗 Google Colab
Обучение модели выполнялось в Google Colab:  
👉 [Colab notebook](https://colab.research.google.com/drive/1VkBarp7KPXAgJtIbPtH7lf4VGlEbJ0Up?usp=sharing)

---

## 🖼️ Результаты
Тестирование выполнено на наборе из 15 изображений.  
Основные метрики:  
- **Precision**: 0.872  
- **Recall**: 0.955  
- **mAP@0.5**: 0.959  
- **mAP@0.5:0.95**: 0.844  
- Пример работы модели:  

![Результат](https://i.imgur.com/bucuYVn.jpeg)
![Графики](https://i.imgur.com/gSKF4Re.png)

---

## 🛠 Технологии
- Python 3.x  
- PyTorch  
- YOLOv5 (Ultralytics)  
- NumPy, Pandas, Matplotlib  
