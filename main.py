from tkinter import *# uses for the GUI 
from PIL import Image, ImageTk  # For handling images
from tkinter import ttk# ttk stands for the Themed Tkinter, it provides the set of themed widgets
from tkinter import messagebox# for printing the pop up dialog box on the screen.
import os
import threading # adding the threads for improving  the performance of the project
from student import Student# mports the Student class from the student.py file
from Train_Data import TrainData
from Face_Detector import FaceDetect

class Face_Recognition_System:
    def __init__(self, root):# root is the main window of the project.
        self.root = root
        self.root.geometry("1920x1080+0+0")
        self.root.title("Face Recognition System")
        
        
        # Background Image
        self.bg_img = Image.open(r"Face_Images\face1.JPG")
        self.bg_img = self.bg_img.resize((1920, 1080), Image.Resampling.LANCZOS)  # Resampling.LANCZOS used for resizing the image
        
        # Store the image as an instance variable to prevent garbage collection
        self.photoimage = ImageTk.PhotoImage(self.bg_img)
        
        # Displaying the background image using a Label
        self.bg_label = Label(self.root, image=self.photoimage)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Bind the function to handle window size
        self.root.bind("<Configure>", self.resize_image)
        
        # Writing the title on the background image
        self.img_title = Label(self.bg_label, text="Face Recognition Attendance System", 
        font=("Vandalia", 35, "bold"), bg="#000000", fg="white")
        self.img_title.place(relx=0.5, y=0, width=1920, height=55, anchor="n")
        
        # Creating the buttons on the home page
        
        # =========================== Student Button ===================================
        self.img1 = Image.open(r"Face_Images\Student Information.png") 
        self.img1 = self.img1.resize((150, 150), Image.Resampling.LANCZOS)
        
        # Storing the image as an instance variable to prevent garbage collection
        self.photoimage1 = ImageTk.PhotoImage(self.img1)
        
        # Performing the button action
        self.b1 = Button(self.bg_label, image=self.photoimage1,command=self.student_details, cursor="hand2")
        self.b1.place(x=200, y=100, width=150, height=150)
        
        # Creating the button for "Student_Details" label
        self.b1_label = Button(self.bg_label, cursor="hand2",command=self.student_details, text="Student Details", font=("times new roman", 15, "bold"), bg="blue", fg="white")
        self.b1_label.place(x=200, y=250, width=150, height=40)
        
        # ============================== Face Detector / Opening the Camera ======================================
         
        # Access the image to the webpage
        self.img2 = Image.open(r"Face_Images\Face Recognition.png")
        self.img2 = self.img2.resize((150, 150), Image.Resampling.LANCZOS)
         
        # Storing the image as an instance variable for preventing garbage collection
        self.photoimage2 = ImageTk.PhotoImage(self.img2)
         
        # Creating the button for performing the actual action
        self.b2 = Button(self.bg_label, image=self.photoimage2,command=self.Face_Detect_Data, cursor="hand2")
        self.b2.place(x=450, y=100, width=150, height=150)
        
        # Creating the button for the "Face Detector" Label
        self.b2_label = Button(self.bg_label, text="Face Detector",command=self.Face_Detect_Data, font=("times new roman", 15, "bold"), bg="blue", fg="white")
        self.b2_label.place(x=450, y=250, width=150, height=40)
        
        # ===================================== Attendance Button ====================================================
        
        # Access the image to the web page 
        self.img3 = Image.open(r"Face_Images\Class Timetable.png")
        self.img3 = self.img3.resize((150, 150), Image.Resampling.LANCZOS)
        
        # Storing the image as an instance variable for preventing garbage collection
        self.photoimage3 = ImageTk.PhotoImage(self.img3)
        
        # Creating the button for the Attendance
        self.b3 = Button(self.bg_label, image=self.photoimage3, cursor="hand2")
        self.b3.place(x=700, y=100, width=150, height=150)
        
        # Creating the button for the Attendance label
        self.b3_label = Button(self.bg_label, text="Attendance", font=("times new roman", 15, "bold"), bg="blue", fg="white")
        self.b3_label.place(x=700, y=250, width=150, height=40)
        
        # =================================== Help Desk Button =====================================================
        
        # Accessing the image to the webpage
        self.img4 = Image.open(r"Face_Images\Help Desk (2).png")
        self.img4 = self.img4.resize((150, 150), Image.Resampling.LANCZOS)
        
        # Making image as an instance variable for preventing garbage collection
        self.photoimage4 = ImageTk.PhotoImage(self.img4)
        
        # Creating the button for the help desk
        self.b4 = Button(self.bg_label, image=self.photoimage4, cursor="hand2")
        self.b4.place(x=950, y=100, width=150, height=150)
        
        # Creating the button for the Help Desk label
        self.b4_label = Button(self.bg_label, text="Help Desk", font=("times new roman", 15, "bold"), bg="blue", fg="white")
        self.b4_label.place(x=950, y=250, width=150, height=40)
        
        # =========================================Train Data Button =====================================================
        
        # accessing the image to the webpage
        self.img5 = Image.open(r"Face_Images\train_data.png")
        self.img5 = self.img5.resize((150,150),Image.Resampling.LANCZOS)
        
        # making the img as a instance variable to prevents the garbage collection
        self.photoimg5 = ImageTk.PhotoImage(self.img5)
        
        # creating the button for the img of train data
        self.b5 = Button(self.bg_label, image = self.photoimg5,command=self.TrainDataset, cursor = "hand2")
        self.b5.place(x=200,y=350, width=150, height=150)
        
        # creating the label and button for the Train data
        self.b5_label = Button(self.bg_label, text="Train Data",command=self.TrainDataset, cursor="hand2", font=("times new roman", 15, "bold"), bg="blue", fg="white") 
        self.b5_label.place(x=200,y=500, width=150, height=40)
        
        # ====================================== Button for show photos folder ==============================================
        
        # accessing the imag to the webpage 
        self.img6 = Image.open(r"Face_Images\gallery_face.png")
        self.img6 = self.img6.resize((150,150),Image.Resampling.LANCZOS)
        
        # storing the image as a instance variable for preventing the Garbage collection
        self.photoimg6 = ImageTk.PhotoImage(self.img6)
        
        # creating the button for the image of photo
        self.b6 = Button(self.bg_label, image = self.photoimg6,command=self.open_imgs, cursor = "hand2")
        self.b6.place(x=450,y=350, width=150, height=150)
        
        # creating the button and the label for the photos 
        self.b6_label = Button(self.bg_label, text = "Photos", cursor = "hand2",command=self.open_imgs, font=("times new roman", 15, "bold"), bg="blue", fg="white",)
        self.b6_label.place(x=450, y=500, width=150, height=40)
        
        # ================================= Developer Button ===========================================================
        
        #accessing the image for the Drveloper button
        self.img7 = Image.open(r"Face_Images\developer.jpg")
        self.img7 = self.img7.resize((150,150),Image.Resampling.LANCZOS)
        
        # storing the image as a instance variable for preventing the garbage collection
        self.photoimage7 = ImageTk.PhotoImage(self.img7)
        
        # creating the button for the Developer Button
        self.b7 = Button(self.bg_label, image = self.photoimage7, cursor= "hand2")
        self.b7.place(x=700, y=350, width=150,height=150)
        
        # creating the button and label for developer button
        self.b7_label = Button(self.bg_label, text = "Developer", cursor = "hand2", font=("times new roman", 15, "bold"),bg="blue", fg="white")
        self.b7_label.place(x=700,y=500,width=150,height=40)
        
        # ====================================== Exit Button ===========================================================
        
        # accessing the image on the webpage
        self.img8 = Image.open(r"Face_Images\exit_face.jpg")
        self.img8 = self.img8.resize((150,150), Image.Resampling.LANCZOS)
        
        # storing the image as a instance variable for preventing the garbage collection
        self.photoimg8 = ImageTk.PhotoImage(self.img8)
        
        # creating the button for the image of the Exit Button
        self.b8 = Button(self.bg_label, image = self.photoimg8, cursor = "hand2")
        self.b8.place(x=950, y=350, width=150,height=150 )
        
        # creating the label and the button for the exit button
        self.b8_label = Button(self.bg_label, text = "Exit", cursor="hand2", font=("times new roman", 15, "bold"),bg="blue",fg="white",)
        self.b8_label.place(x=950,y=500, width=150,height=40)

        
    # ===================================================================================================================
    # Function for resizing the image based on the window size
    def resize_image(self, event):
        new_width = event.width
        new_height = event.height
        
        img_resized = self.bg_img.resize((new_width, new_height), Image.Resampling.LANCZOS)  # Use self.img
        self.photoimage = ImageTk.PhotoImage(img_resized)  # Create new PhotoImage
        self.bg_label.config(image=self.photoimage)  # Update bg_label with the resized image
        self.bg_label.image = self.photoimage  # Keep a reference to avoid garbage collection
    
    def open_imgs(self):
        os.startfile("image_data")
        
    # =================================== Button Functions  ===============================================
    
    # function for student button on the homepage
    def student_details(self):
        self.new_window=Toplevel(self.root)#where to open new window
        self.app = Student(self.new_window)# in new window its open the Student Class
        
    # function for the Train Dataset button on the homepage
    def TrainDataset(self):
        self.new_window=Toplevel(self.root)#where to open new window
        self.app = TrainData(self.new_window)
        
    # function for the face detector button on the homepage 
    def Face_Detect_Data(self):
        self.new_window=Toplevel(self.root)
        self.app = FaceDetect(self.new_window)
     

#===================================================================================================================================
                       
if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()
