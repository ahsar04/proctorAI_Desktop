from tkinter import *
from tkinter import messagebox
#from time import strftime
import tkinter as tk
from tkinter_webcam import webcam
from Detector import main_app
import requests
import json

url = "https://proctorai.webozan.com/api/"
# request start
params=""
response = requests.get(url+"exams",params)

desktop = Tk()
desktop.title("Login")
desktop.geometry('925x500+175+100')
desktop.configure(bg="#fff")
desktop.resizable(False,False)

def signin() :
    userId = user.get()
    exam = clicked.get()
    if exam == "Pilih Mata Kuliah":
        messagebox.showerror("Warning!", "Pilih ujian terlebih dahulu!")
    exampIdIndex= exam.index('-')
    examId = exam[0:exampIdIndex]
    params={"exam_id":examId, "participant_id":userId}
    response = requests.post(url+"login",data=params)

    if response.status_code==200:
        responseData=json.loads(response.text)
        code = responseData['code']
        message = responseData['message']
        print(message)
        data = responseData['data']
        # print(data)
        desktop.destroy()
        main_app(data)
    else:
        messagebox.showerror("Access denied!", "User ID tidak ditemukan!")
        print(f"Error: {response.status_code}")
    
    # if username=='admin' :
    #     desktop.destroy()
    #     main_app()
        
    # elif username!='admin' :
    #     messagebox.showerror("Invalid", "Invalid username and password")
        
    # elif username!="admin" :
    #     messagebox.showerror("Invalid", "Invalid username")
        

img = PhotoImage(file='logo1.png')
Label(desktop,image=img,width=350,height=350,bg='white').place(x=50,y=50)

frame = Frame(desktop,width=350,height=350,bg="white")
frame.place(x=480,y=70)

heading = Label(frame,text='Sign In',fg='#feca05',bg='white',font=('Microsoft YaHei UI Light',23,'bold'))
heading.place(x=120,y=10)

########----------------------------------
def on_enter(e) :
    user.delete(0,'end')
    
def on_leave(e):
    name = user.get()
    if name=='':
        user.insert(0,'Username')
        

user = Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
user.place(x=30,y=125)
user.insert(0,'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame,width=290,height=2,bg='black').place(x=25,y=150)

########----------------------------------
#def on_enter(e) :
    #code.delete(0,'end')
    
#def on_leave(e):
    #name = code.get()
    #if name=='':
        #code.insert(0,'Password')
options = []
if response.status_code==200:
    responseData=json.loads(response.text)
    code = responseData['code']
    message = responseData['message']
    data = responseData['data']
    # print(data)
    for i in data:
        # print(i['exam_code'])
        options.append(str(i['id'])+"-"+i['exam_name'])
        # print(i['exam_name'])
        # print(i['exam_date'])
else:
    print(f"Error: {response.status_code}")        


clicked = StringVar()
clicked.set("Pilih Mata Kuliah")

drop = OptionMenu(desktop, clicked, *options)
drop.pack()
drop.place(x=505,y=150)

########----------------------------------
Button(frame,width=39,pady=7,text='Sign In',bg='#feca05',fg='white',border=0,command=signin).place(x=35,y=204)
    

desktop.mainloop()