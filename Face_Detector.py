from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from PIL import Image, ImageTk
import cv2
import os
from datetime import date, datetime
from time import strftime

class FaceDetect:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1920x1080+0+0")
        self.root.title("Face Detector")
        
        # background image
        self.bg_img = Image.open(r"Face_Images\face_detect1.JPG")
        self.bg_img = self.bg_img.resize((1920, 1080),Image.Resampling.LANCZOS)
        
        # storing the background image as instance variable for prevents the garbage collection
        self.photoimage = ImageTk.PhotoImage(self.bg_img)
        
        # Displaying the image on the webpage 
        self.bg_label = Label(self.root, image=self.photoimage)
        self.bg_label.place(relwidth=1, relheight=1, x= 0, y=0)
        
        # Bind the function to handle the image size
        self.root.bind("<Configure>", self.resize_image)
        
        
        # writing the title on the background image
        self.bg_title = Label(self.bg_label, text="Face Detection System", font=("Vandalia", 35, "bold"), bg="white", fg="black",)
        self.bg_title.place(relx=0.5, y=0, width=1920, height=55, anchor="n")
        
        # img on bg image 
        self.left_image = Image.open(r"Face_Images\Face Recognition.png")
        self.left_image = self.left_image.resize((1920,1080), Image.Resampling.LANCZOS)
        
        # converting the image to the instance variable for preventing the garbage collection
        self.left_photoimage = ImageTk.PhotoImage(self.left_image)
        
        # displaying the image on the webpage
        self.left_img_lbl = Label(self.bg_label, image = self.left_photoimage, cursor="hand2")
        self.left_img_lbl.place(x=600, y=56, width=950, height=600) 
        
        # provide the options to the admin for select the camera
        self.camera_opt=ttk.Combobox(self.left_img_lbl,font=("times new roman", 15, "bold"))
        self.camera_opt['values']=("Select Camera","Entry Camera","Exit Camera")
        self.camera_opt.current(0)
        self.camera_opt.place(x=200, y=200, width=200, height=40)       
        
        # =========================== Face Detect Button   ==============================================
        self.face_detect_b1 = Button(self.left_img_lbl, text = "Face Detecting",command= self.Face_recognition, font=("times new roman", 20, "bold"), bg="green",fg="white" )
        self.face_detect_b1.place(x=200, y=300, width= 300, height=60)
        
        # binding the camera selction method for calling or performing the event
        self.camera_opt.bind("Comboboxsekected",self.select_camera)
        
    # function for the select camera option
    def select_camera(self,event):
        selected_camera = self.camera_opt.get()
        if selected_camera == "Entry Camera":
            self.camera_index = 0 # by default webcamera
        elif selected_camera == "Exit Camera":
            self.camera_index = 1
        else:
            messagebox.showerror("Error", "Camera index out off range.")
            
        if self.camera_index is not None:
            self.video_cap = cv2.VideoCapture(self.camera_index)# update the selcted camera index
            
        
        
    #  ==========================================   Store the attendance in file   ==========================
        
    def genrate_attendance(self,i,r,n,div,dep):
        with open("Attendance.csv","r+",newline="\n") as f:
            mydatalist = f.readlines()
            name_list = [line.split(",")[0] for line in mydatalist]
            
            if i not in name_list:
                now = datetime.now()
                date= now.strftime("%d/%m/%Y")
                time = now.strftime("%H:%M:%S")
                    
                    
                with open("Attendance.csv","a",newline="\n") as f:
                    f.write(f"\n{i},{r},{n},{div},{dep},{date},{time},Present")
                    
                print(f"Attendance stored for {n} (ID: {i}) at {time} on {date}")

            else:
                # Debugging: Inform if attendance already exists
                print(f"Attendance already marked for {n} (ID: {i})")
   
            
                
        
        
        # ============= function for the button ===================
        
    def Face_recognition(self):
        def draw_boundry(img,classifier,scaleFactor,minNighbors,color,text,clf):
            self.gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            self.features = classifier.detectMultiScale(self.gray_img,scaleFactor,minNighbors)
            
            self.co_ordinates = []
            
            for (x,y,w,h) in self.features:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
                id,predict = clf.predict(self.gray_img[x:x+w,y:y+h])
                confidence = int((100*(1-predict/300)))
                
                # the image data is saved in database for accesing the database' data connect it.
                self.conn = mysql.connector.connect(host="localhost", username="root", password="Admin@123", database="face_recognition_system")
                self.my_cursor = self.conn.cursor()# store the database cursor in the variable
                
                # check for the match id of the database with image
                self.my_cursor.execute("select student_id from student_details where student_id="+str(id))
                i=self.my_cursor.fetchone()
                i="+".join(i)
                # check for match the name of the database with the image
                self.my_cursor.execute("select student_name from student_details where student_id="+str(id))# join id with string
                n=self.my_cursor.fetchone()
                n="+".join(n)
                # check for the roll number 
                self.my_cursor.execute("select roll_no from student_details where student_id="+str(id))
                r=self.my_cursor.fetchone()
                r="+".join(r)
                # check for the division
                self.my_cursor.execute("select division from student_details where student_id="+str(id))
                div=self.my_cursor.fetchone()
                div="+".join(div)
                # check for the department
                self.my_cursor.execute("select department from student_details where student_id="+str(id))
                dep=self.my_cursor.fetchone()
                dep="+".join(dep)
                
                if confidence >68:# if matching percentage is greater than 50 , then 
                    # showing the roll_no,name, division of the studnent on the top of the rectangle
                    cv2.putText(img,"id : {i}",(x,y-80),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Roll No : {r}",(x,y-55), cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Name : {n}",(x,y-30), cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Division : {div}",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Department : {dep}",(x,y+20),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)

                    # stores the attendance for recognized person
                    self.genrate_attendance(i,r,n,div,dep)
                
                else:# if person is unknown 
                    # creating the rectangle of red colour
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                    cv2.putText(img,"Alert : Anoymous Person",(x,y-20),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,0,255),3)#shows text stranger in red colour.
                    #messagebox.showwarning("Alert", "Anonymous Person")
                    
                self.co_ordinates=[x,y,w,h]#previously we create the empty co-ordinates list in that list we are passes the values x,y,w,h
            return self.co_ordinates
        
        # creating the function for the recognizing the image 
        def Recognize(img,clf,faceCascade):
            self.co_ordinates=draw_boundry(img,faceCascade,1.1,10,(255,255,255),"Face",clf)
            return img
        
        #storing the files
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")# passing the algorithm file for recognize the face
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")# in this file we stores the previously captured images data in binary format
        
        # capturing the video
        video_cap = cv2.VideoCapture(0)# for secondary camera , index is 1
        
        # creating the loop for video capture
        while True:
            ret,img = video_cap.read()
            img = Recognize(img,clf,faceCascade)
            cv2.imshow("Welcome to the Face Recognition",img)
            
            if cv2.waitKey(1) == 13:
                break
            
        video_cap.release()
        cv2.destroyAllWindows()
        
    # Function for resizing the image based on the window size
    def resize_image(self, event):
        new_width = event.width
        new_height = event.height
        
        img_resized = self.bg_img.resize((new_width, new_height), Image.Resampling.LANCZOS)  # Use self.img
        self.photoimage = ImageTk.PhotoImage(img_resized)  # Create new PhotoImage
        self.bg_label.config(image=self.photoimage)  # Update bg_label with the resized image
        self.bg_label.image = self.photoimage  # Keep a reference to avoid garbage collection
    
        
        
if __name__ == '__main__':
    root = Tk()
    obj = FaceDetect(root)
    root.mainloop()
