from tkinter import *# for developing the UI's of the page
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from PIL import Image, ImageTk
from datetime import date, datetime
import cv2
import os
import numpy as np
#import tkinter as tk

class TrainData:
    def __init__(self, root):
        self.root = root 
        self.root.geometry("1920x1080+0+0")
        self.root.title("Student Details")
        
        # Background Image
        self.b_g_img = Image.open(r"Face_Images\face.jpg")
        self.b_g_img = self.b_g_img.resize((1500, 700), Image.Resampling.LANCZOS)
        # creating the background image as a instance variable to prevent the garbage collection. 
        self.photoimage = ImageTk.PhotoImage(self.b_g_img)
        # Label for the background image
        self.bg_label = Label(self.root,image=self.photoimage)
        self.bg_label.place(x=0, y=5, relwidth=1, relheight=1)
        # for displaying on the webpage 
        self.title = Label(self.root,text="Train Dataset", font=("Vandalia",35,"bold"),bg="white", fg="black")
        self.title.place(relx=0.5, y=0, width=1920, height=55, anchor="n") 
        
        # Performing the button action
        self.b1 = Button(self.bg_label,cursor="hand2")
        self.b1.place(x=200, y=100, width=0, height=0)
        
        # Creating the button for "Student_Details" label
        self.b1_label = Button(self.bg_label, cursor="hand2", text="Train Image Data",command=self.Train_Data_Set, font=("times new roman", 25, "bold"), bg="white", fg="black")
        self.b1_label.place(x=100, y=400, width=300, height=60) 
        
    def Train_Data_Set(self):
        self.data_directory = ("image_data")
        self.path = [os.path.join(self.data_directory,file) for file in os.listdir(self.data_directory)] 
        
        self.faces = []
        self.ids = []     
        for image in self.path:
            self.img = Image.open(image).convert("L") # for convert to the grayscale image
            self.imageNP = np.array(self.img,"uint8")  # 'uint8' isthe datatype for converting the image to grayscale using numpy.
            self.id = int(os.path.split(image)[1].split('.')[1])
            
            self.faces.append(self.imageNP)
            self.ids.append(self.id) 
            cv2.imshow("Training :", self.imageNP)
            cv2.waitKey(1) == 13
        self.ids = np.array(self.ids)
        
    #=========================== using the LBPH Algorithm for recognizing th faces  =================
    
        self.clf = cv2.face.LBPHFaceRecognizer_create()
        self.clf.train(self.faces,self.ids)
        self.clf.write("classifier.xml")
        cv2.destroyAllWindows()
        messagebox.showinfo("Result","Dataset Training completed successfully!") 
        
        
        
        
        
        
        
if __name__ == '__main__':
    root = Tk()
    obj = TrainData(root)
    root.mainloop()
