# 📰 News Classifier

## 📌 Описание
Проект посвящён созданию простого классификатора новостей на основе **методов машинного обучения**.  
Классификатор анализирует текст заголовка новости и определяет её тематику (одна из 5 категорий).  

Работа выполнена в рамках курсовой работы.  

---

## 📂 Содержание репозитория
- 📝 [Доклад](https://github.com/AmicumTuum/PortfolioNR/blob/main/Python/%D0%9A%D0%BB%D0%B0%D1%81%D1%81%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82%D0%BE%D1%80%20%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B5%D0%B9/%D0%9A%D0%BB%D0%B0%D1%81%D1%81%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82%D0%BE%D1%80%20%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B5%D0%B9.pdf) — описание проекта и результатов  
- ⚙️ [Код программы](https://github.com/AmicumTuum/PortfolioNR/blob/main/Python/%D0%9A%D0%BB%D0%B0%D1%81%D1%81%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82%D0%BE%D1%80%20%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B5%D0%B9/news.py) — обучение модели и классификация текста
- 🖥️ [GUI](https://github.com/AmicumTuum/PortfolioNR/blob/main/Python/%D0%9A%D0%BB%D0%B0%D1%81%D1%81%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82%D0%BE%D1%80%20%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B5%D0%B9/newsform.py) — GUI-приложение на `tkinter` (использовалось для сборки `.exe`)  

---

## 📊 Датасет
Использован датасет **BBC News**:  
- источник: [bbc-news-data.csv](https://raw.githubusercontent.com/amankharwal/Website-data/master/bbc-news-data.csv)  
- размер: ~2200 новостных заголовков  
- категории: `business`, `entertainment`, `politics`, `sport`, `tech`  

---

## 🖼️ Результаты
Для обучения модели использовалась **наивная байесовская классификация (MultinomialNB)**.  
Основные результаты:  
- Модель успешно классифицирует новости по 5 категориям.  
- Средняя точность (accuracy) на тестовой выборке: **~97%**.  

Пример работы:
![Результат](https://i.imgur.com/RvfGFqa.png)


