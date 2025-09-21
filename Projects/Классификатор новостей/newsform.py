import tkinter as tk
import tkinter.font as tkFont
from tkinter.messagebox import showerror, showinfo
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


class App:
    def __init__(self, root):
        global checkData, checkTrain
        checkData = False
        checkTrain = False
        #setting title
        root.title("News category predict")
        #setting window size
        width=927
        height=415
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GButton_301=tk.Button(root)
        GButton_301["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_301["font"] = ft
        GButton_301["fg"] = "#000000"
        GButton_301["justify"] = "center"
        GButton_301["text"] = "Load Dataset"
        GButton_301.place(x=30,y=40,width=118,height=30)
        GButton_301["command"] = self.GButton_301_command

        global GLabel_435
        GLabel_435=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_435["font"] = ft
        GLabel_435["fg"] = "#333333"
        GLabel_435["justify"] = "left"
        GLabel_435.place(x=190,y=40,width=720,height=106)

        GButton_890=tk.Button(root)
        GButton_890["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_890["font"] = ft
        GButton_890["fg"] = "#000000"
        GButton_890["justify"] = "center"
        GButton_890["text"] = "Train"
        GButton_890.place(x=30,y=170,width=118,height=30)
        GButton_890["command"] = self.GButton_890_command

        global GLineEdit_154
        GLineEdit_154=tk.Entry(root)
        GLineEdit_154["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_154["font"] = ft
        GLineEdit_154["fg"] = "#333333"
        GLineEdit_154["justify"] = "center"
        GLineEdit_154["text"] = "Input text"
        GLineEdit_154.place(x=30,y=300,width=873,height=30)

        GButton_550=tk.Button(root)
        GButton_550["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_550["font"] = ft
        GButton_550["fg"] = "#000000"
        GButton_550["justify"] = "center"
        GButton_550["text"] = "Predict"
        GButton_550.place(x=30,y=360,width=118,height=30)
        GButton_550["command"] = self.GButton_550_command

        global GLabel_961
        GLabel_961=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_961["font"] = ft
        GLabel_961["fg"] = "#333333"
        GLabel_961["justify"] = "center"
        GLabel_961["text"] = ""
        GLabel_961.place(x=180,y=360,width=173,height=30)


    def GButton_301_command(self):
        global data, checkData, x, y
        checkData = True
        data = pd.read_csv("https://raw.githubusercontent.com/amankharwal/Website-data/master/bbc-news-data.csv", sep='\t')
        showinfo(title="Информация", message="База данных загружена" )
        GLabel_435["text"] = data.head()
        data = data[["title", "category"]]
        x = np.array(data["title"])
        y = np.array(data["category"])


    def GButton_890_command(self):
        global checkData, checkTrain
        if(checkData == True):
            global cv, X_train, X_test, y_train, y_test, model
            cv = CountVectorizer()
            X = cv.fit_transform(x)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
            model = MultinomialNB()
            model.fit(X_train,y_train)
            checkTrain = True
            showinfo(title="Информация", message="Сеть обучена" )
        else:
            showerror(title="Информация", message="База данных не загружена" )
        

    def GButton_550_command(self):
        global output, checkData, checkTrain
        if(checkData == True):
            if(checkTrain == True):
                user = GLineEdit_154.get()
                data = cv.transform([user]).toarray()
                output = model.predict(data)
                GLabel_961["text"] = output
            else:
                showerror(title="Информация", message="Сеть не обучена" )
        else:
            showerror(title="Информация", message="База данных не выгружена" )


if __name__ == "__main__":
    
    root = tk.Tk()
    app = App(root)
    root.mainloop()