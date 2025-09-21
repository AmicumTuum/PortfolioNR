import tkinter as tk
my_w = tk.Tk()
my_w.geometry("500x250")

def my_upd(v):
    color_c='#%02x%02x%02x' % (color1.get(), color2.get(), color3.get())
    b1.config(bg=color_c)
    b1.config(text=color_c)

font1=('Time',18,'normal')

color1 = tk.Scale(my_w, from_=0, to=255,bg='red', orient='horizontal',
    length=250,command=my_upd)
color1.grid(row=0,column=0,padx=5,pady=10)

color2 = tk.Scale(my_w, from_=0, to=255,bg='green', orient='horizontal',
    length=250,command=my_upd)
color2.grid(row=1,column=0,pady=10)

color3 = tk.Scale(my_w, from_=0, to=255,bg='blue', orient='horizontal',
    length=250,command=my_upd)
color3.grid(row=2,column=0,pady=10)

b1=tk.Button(my_w,text='Смешанный цвет',font=font1,width=15)
b1.grid(row=1,column=1,padx=10)
my_w.mainloop()