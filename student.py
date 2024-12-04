from tkinter import *# for developing the UI's of the page
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from datetime import date, datetime
from PIL import Image, ImageTk
import cv2
import os

class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1920x1080+0+0")
        self.root.title("Student Details")
        
        #  creating the variables which is used for adding the data to the database
        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_div = StringVar()
        self.var_roll_no = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_teacher = StringVar()
        self.var_photo_sample = StringVar()
        
        # Function to add placeholder text
        def add_placeholder(event):
            if self.search_entry.get() == '':
                self.search_entry.insert(0, 'Search here...')
                self.search_entry.config(foreground='grey')

        # Function to remove placeholder text when typing
        def remove_placeholder(event):
            if self.search_entry.get() == 'Search here...':
                self.search_entry.delete(0, 'end')
                self.search_entry.config(foreground='black')

        
        # Define a custom style with a border
        style = ttk.Style()
        style.configure("Custom.TFrame", background="white", bordercolor="blue", borderwidth=5, relief="solid")
        
        # Outer frame using ttk with a custom style for the border
        self.outer_frame = ttk.Frame(self.root, style="Custom.TFrame")
        self.outer_frame.place(x=10, y=50, width=1850, height=900)
        
        # Title label (centered)
        self.title = Label(self.root, text="Student Management System", font=("Vandalia", 35, "bold"))
        self.title.place(relx=0.5, y=0, width=1920, height=55, anchor="n")
        
        # Main content frame inside the outer frame (without any additional borders)
        self.main_frame = Frame(self.outer_frame, bg="white")
        self.main_frame.place(x=10, y=10, width=1830, height=880)  # Adjust padding as needed
        
        # we have to add 2 horizontal frames 
        
        # Left Frame
        self.left_frame = LabelFrame(self.main_frame, bd=2, bg="lightgray", relief=RIDGE, text = "Student Details", font=("times new roman", 12, "bold"))
        self.left_frame.place(x=5, y=10, width=600, height=550)
        
        # current course frame
        self.curr_course_fr = LabelFrame(self.left_frame, bd=2, bg="white", relief=RIDGE, text="Current Course Information", font=("times new roman", 12, "bold"))
        self.curr_course_fr.place(x=7,y=30, width=580,height=150)
        
        # creating the department label for selecting the department
        self.dep_label=Label(self.curr_course_fr, text="Department : ", font=("times new roman", 12,"bold"),bg="white")
        self.dep_label.grid(row=0,column=0,padx=5,pady=20,sticky=W)
        # create and place the combobox for department
        self.dep_combo = ttk.Combobox(self.curr_course_fr,textvariable=self.var_dep,font=("times new roman",12, "bold"), state="readonly")
        self.dep_combo["values"]=("Select Department","Computer","IT","Civil","Mechanical","E&TC","Electronics")
        self.dep_combo.current(0)
        self.dep_combo.grid(row=0, column=1,padx=2,pady=10,sticky=W)
        
        # creating the label for the Year
        self.year_label = Label(self.curr_course_fr, text="Year :", font=("times new roman", 12, "bold"),bg="white")
        self.year_label.grid(row=1,column=0,padx=5,sticky=W)
        # create and placing the combobox for year
        self.year_combo = ttk.Combobox(self.curr_course_fr,textvariable=self.var_year,font=("times new roman", 12, "bold"),state="readonly")
        self.year_combo["values"]=("Select Year", "2020-21", "2021-22","2022-23","2023-24")
        self.year_combo.current(0)
        self.year_combo.grid(row=1,column=1,padx=2,pady=10,sticky=W)
        
        # creating the label for the Course
        self.course_label = Label(self.curr_course_fr, text="Course :",font=("times new roman", 12, "bold"), bg="white")
        self.course_label.grid(row=0,column=2,padx=5,sticky=W)
        # create and place combobox for Course
        self.course_combo = ttk.Combobox(self.curr_course_fr,textvariable=self.var_course, font = ("times new roman", 12, "bold"), state="readonly")
        self.course_combo["values"]=("Select Course","First Year","Second Year","Third Year","Last Year")
        self.course_combo.current(0)
        self.course_combo.grid(row=0,column=3,padx=2,pady=10,sticky=W)
        
        # creating the label for the Semester
        self.sem_label = Label(self.curr_course_fr, text ="Semester :", font=("times new roman", 12, "bold"), bg="white")
        self.sem_label.grid(row=1,column=2,padx=5,sticky=W)
        # create and place combobox
        self.sem_combo = ttk.Combobox(self.curr_course_fr,textvariable=self.var_semester, font = ("times new roman", 12, "bold"), state="readonly")
        self.sem_combo["values"]=("Select Semester","First","Second")
        self.sem_combo.current(0)
        self.sem_combo.grid(row=1,column=3,padx=2,pady=10,sticky=W)
        
        ## creating the Student Class Information
        self.std_cls_fr = LabelFrame(self.left_frame, bd=2, bg="white", relief=RIDGE, text="Student Class Information", font=("times new roman", 12, "bold"))
        self.std_cls_fr.place(x=7,y=200, width=580,height=320)
        
        # creating the label for the Student Information
        self.std_id = Label(self.std_cls_fr, text ="Student Id :", font=("times new roman", 12, "bold"), bg="white")
        self.std_id.grid(row=0,column=0,padx=5,pady=5,sticky=W)
        # creating the Entry for the Student information
        self.std_id_entry = ttk.Entry(self.std_cls_fr,width=19,textvariable=self.var_std_id,font=("times new roman", 12, "bold"))
        self.std_id_entry.grid(row=0,column=1,padx=2,sticky=W) 
        
        # label for Student Name
        self.std_name_label = Label(self.std_cls_fr, text="Student Name :", font=("times new roman", 12, "bold"), bg="white")
        self.std_name_label.grid(row=0,column=2,padx=5,sticky=W)
        # creating the Entry for student name 
        self.std_name_entry = ttk.Entry(self.std_cls_fr,width=18,textvariable=self.var_std_name, font=("times new roman", 12, "bold"))
        self.std_name_entry.grid(row=0,column=3,padx=5,sticky=W)
     
        # label for Class Devision
        self.cls_div_label = Label(self.std_cls_fr, text="Division :", font=("times new roman", 12, "bold"), bg="white")
        self.cls_div_label.grid(row=1,column=0,padx=2,pady=5,sticky=W)
        # create  combobox for Division
        self.div_combo = ttk.Combobox(self.std_cls_fr,textvariable=self.var_div, font = ("times new roman", 10, "bold"), state="readonly",width=19)
        self.div_combo["values"]=("Select Division","A","B","C")
        self.div_combo.current(0)
        self.div_combo.grid(row=1,column=1,padx=2,pady=4,sticky=W)
        
        # label for Roll No
        self.Roll_No_label = Label(self.std_cls_fr, text="Roll No :", font=("times new roman", 12, "bold"), bg="white")
        self.Roll_No_label.grid(row=1,column=2,padx=2,pady=5,sticky=W)
        # creating the Entry for Roll No
        self.Roll_No_entry = ttk.Entry(self.std_cls_fr,width=18,textvariable=self.var_roll_no, font=("times new roman", 12, "bold"))
        self.Roll_No_entry.grid(row=1,column=3,padx=2,pady=5,sticky=W)
        
        # Label for the gender
        self.gender_label = Label(self.std_cls_fr, text="Gender :", font=("times new roman", 12, "bold"), bg="white")
        self.gender_label.grid(row=2,column=0,padx=2,pady=5,sticky=W)
        # create  combobox for gender
        self.gender_combo = ttk.Combobox(self.std_cls_fr,textvariable=self.var_gender, font = ("times new roman", 10, "bold"), state="readonly",width=19)
        self.gender_combo["values"]=("Select Gender","Male","Female","Other")
        self.gender_combo.current(0)
        self.gender_combo.grid(row=2,column=1,padx=2,pady=4,sticky=W)
        
        #label For the Email   
        self.email_label = Label(self.std_cls_fr, text="Email :", font=("times new roman", 12, "bold"), bg="white")
        self.email_label.grid(row=2,column=2,padx=2,pady=5,sticky=W)
        # create the entry for the Email
        self.email_entry = ttk.Entry(self.std_cls_fr,width=18,textvariable=self.var_email, font=("times new roman", 12, "bold"))
        self.email_entry.grid(row=2,column=3,padx=2,pady=5,sticky=W)
        
        #Label for Date Of Birth
        self.dob_label = Label(self.std_cls_fr, text="DOB :", font=("times new roman", 12, "bold"), bg="white")
        self.dob_label.grid(row=3,column=0,padx=2,pady=5,sticky=W)
        # create the entry for the DOB
        self.dob_entry = ttk.Entry(self.std_cls_fr,width=19,textvariable=self.var_dob, font=("times new roman", 12, "bold"))
        self.dob_entry.grid(row=3,column=1,padx=2,pady=5,sticky=W)
        
        # label for Phone No
        self.ph_no_label = Label(self.std_cls_fr, text="Phone No :", font=("times new roman", 12, "bold"), bg="white")
        self.ph_no_label.grid(row=3,column=2,padx=2,pady=5,sticky=W)
        # create the entry for Phone Number
        self.ph_no_entry = ttk.Entry(self.std_cls_fr,width=18,textvariable=self.var_phone, font=("times new roman", 12, "bold"))
        self.ph_no_entry.grid(row=3,column=3,padx=2,pady=5,sticky=W)
        
        #Label for Address
        self.address_label = Label(self.std_cls_fr, text="Address :", font=("times new roman", 12, "bold"), bg="white")
        self.address_label.grid(row=4,column=0,padx=2,pady=5,sticky=W)
        # create the entry for the address
        self.address_entry = ttk.Entry(self.std_cls_fr,width=19,textvariable=self.var_address, font=("times new roman", 12, "bold"))
        self.address_entry.grid(row=4,column=1,padx=2,pady=5,sticky=W)
        
        # Label for teacher name
        self.teacher_label = Label(self.std_cls_fr, text="Teacher Name :", font=("times new roman", 12, "bold"), bg="white")
        self.teacher_label.grid(row=4,column=2,padx=2,pady=5,sticky=W)
        # create the entry for the teacher name 
        self.teacher_entry = ttk.Entry(self.std_cls_fr,width=18,textvariable=self.var_teacher, font=("times new roman", 12, "bold"))
        self.teacher_entry.grid(row=4,column=3,padx=2,pady=5,sticky=W)
        
        # Radio buttons for taking the sample of the image or not
        # button1
        self.var_radio_btn1 = StringVar() # for adding to the database table 
        self.radio_btn1 = Radiobutton(self.std_cls_fr, text="Take Photo Sample",variable=self.var_radio_btn1,font=("times new roman",10,"bold"), value="Yes")
        self.radio_btn1.grid(row=5,column=0)
        #button 2
        self.radio_btn2 = Radiobutton(self.std_cls_fr, text="Not to take Photo Sample",variable=self.var_radio_btn1,font=("times new roman",10,"bold"), value="No")
        self.radio_btn2.grid(row=5,column=1)
        
        # Buttons Frame 
        self.btn_frame = Frame(self.std_cls_fr, bd=2 , relief=RIDGE, bg="white",)
        self.btn_frame.place(x=0,y=200, width=575, height = 90)
        
        # Save Button
        self.save_btn = Button(self.btn_frame, text="Save", width =24,command=self.add_data, font=("times new roman", 10, "bold"),bg="green", fg="white")
        self.save_btn.grid(row=0,column=0,padx=5,pady=5)
        
        # Update Button
        self.update_btn = Button(self.btn_frame, text="Update", width = 24, command = self.update_data, font=("times new roman", 10, "bold"),bg="green", fg="white")
        self.update_btn.grid(row=0,column=1,padx=5,pady=5)
        
        # Delete Button
        self.delete_btn = Button(self.btn_frame, text="Delete", width = 24, command = self.delete_data, font=("times new roman", 10, "bold"),bg="green", fg="white")
        self.delete_btn.grid(row=0,column=2,padx=5,pady=5)
        
        #Reset Button
        self.reset_btn = Button(self.btn_frame, text="Reset", width = 24, command= self.reset_data, font=("times new roman", 10, "bold"),bg="green", fg="white")
        self.reset_btn.grid(row=1,column=0,padx=5,pady=5)
        
        #Take Photo Sample button
        self.take_phto_btn = Button(self.btn_frame, text="Take Photo", width = 24,command = self.generate_dataset, font=("times new roman", 10, "bold"),bg="green", fg="white")
        self.take_phto_btn.grid(row=1,column=1,padx=5,pady=5)
        
        #Update photo sample button
        self.updt_phto_btn = Button(self.btn_frame, text="Update Photo" ,width = 24, font=("times new roman", 10, "bold"),bg="green", fg="white")
        self.updt_phto_btn.grid(row=1,column=2,padx=5,pady=5)
    # ==========================================================================================================    
        # Right Frame
        self.right_frame = LabelFrame(self.main_frame, bd=2, bg="lightgray", relief=RIDGE, text="Student Details",font=("times new roman", 12, "bold"))
        self.right_frame.place(x=640,y=10, width=600, height=550)
        
        # frame fo rthe search database
        self.search_fr = LabelFrame(self.right_frame, bd=2, bg="white", relief=RIDGE, text="Search Database", font=("times new roman", 12, "bold"))
        self.search_fr.place(x=5,y=20, width=580,height=70)
        
        # frame for Search by
        self.seach_label = Label(self.search_fr, text="Search By :", font=("times new roman", 12, "bold"), bg="blue",fg="white",)
        self.seach_label.grid(row=0,column=0,padx=5,pady=5,sticky=W)
        
        # create combo for Seach by with options "Roll No" and "Name"
        self.search_combo = ttk.Combobox(self.search_fr,width=10, font = ("times new roman", 12, "bold"), state="readonly")
        self.search_combo["values"]=("Select","Roll No","Name")
        self.search_combo.current(0)
        self.search_combo.grid(row=0,column=1,padx=5,pady=10,sticky=W)
        
        # Create Entry for the Search bar 
        self.search_entry = ttk.Entry(self.search_fr,width=20, font=("times new roman", 12, "bold"))
        self.search_entry.grid(row=0,column=2,padx=5,pady=5,sticky=W)
        
        # Add placeholder text initially
        self.search_entry.insert(0, 'Search here...')
        self.search_entry.config(foreground='grey')

        # Bind events to handle placeholder functionality
        self.search_entry.bind("<FocusIn>", remove_placeholder)
        self.search_entry.bind("<FocusOut>", add_placeholder)
        
        #Button for Search 
        self.search_btn = Button(self.search_fr, text="Search", width = 9, font=("times new roman", 12, "bold"),bg="blue", fg="white")
        self.search_btn.grid(row=0,column=3,padx=3,pady=5)
        
        #Button for  Show All
        self.shwall_btn = Button(self.search_fr, text="Show All", width = 9, font=("times new roman", 12, "bold"),bg="blue", fg="white")
        self.shwall_btn.grid(row=0,column=4,padx=3,pady=5)
        
        # ===================  Table Frame   ============================
        self.tbl_frame = Frame(self.right_frame,bd=3, bg="white", relief=RIDGE)
        self.tbl_frame.place(x=5,y=100,width=585, height=420)
        
        # create the scrollbars
        self.scroll_x = ttk.Scrollbar(self.tbl_frame,orient=HORIZONTAL)
        self.scroll_y = ttk.Scrollbar(self.tbl_frame,orient=VERTICAL)
        
        # crate the table 
        self.std_table = ttk.Treeview(self.tbl_frame,column=("student_id","student_name","department","course","year","semester","division","roll","gender","DOB","email","phone","address","teacher","photo"),xscrollcommand=self.scroll_x.set,yscrollcommand=self.scroll_y.set)
        
        #placing the scrollbars in table frame
        self.scroll_x.pack(side=BOTTOM, fill=X)
        self.scroll_y.pack(side=RIGHT, fill=Y)
        self.scroll_x.config(command=self.std_table.xview)
        self.scroll_y.config(command=self.std_table.yview)
        
        # giving the column names in table
        self.std_table.heading("student_id", text="Student Id")
        self.std_table.heading("student_name", text="Name")
        self.std_table.heading("department", text="Department")
        self.std_table.heading("course", text="Course")
        self.std_table.heading("year", text="Year")
        self.std_table.heading("semester", text="Semester")
        self.std_table.heading("division", text="Division")
        self.std_table.heading("roll", text="Roll No")
        self.std_table.heading("gender", text="Gender")
        self.std_table.heading("DOB", text="Birth Date")
        self.std_table.heading("email", text="Email Id")
        self.std_table.heading("phone", text="Phone No")
        self.std_table.heading("address", text="Address")
        self.std_table.heading("teacher", text="Class Teacher")
        self.std_table.heading("photo", text="Photo Status")
        self.std_table["show"]="headings"
        
        #set the width of the table column
        self.std_table.column("student_id", width=100)
        self.std_table.column("student_name", width=100)
        self.std_table.column("department", width=100)
        self.std_table.column("course", width=100)
        self.std_table.column("year", width=100)
        self.std_table.column("semester", width=100)
        self.std_table.column("division", width=100)
        self.std_table.column("roll", width=100)
        self.std_table.column("gender", width=100)
        self.std_table.column("DOB", width=100)
        self.std_table.column("email", width=100)
        self.std_table.column("phone", width=100)
        self.std_table.column("address", width=100)
        self.std_table.column("teacher", width=100)
        self.std_table.column("photo", width=100)

        
        self.std_table.pack(fill=BOTH, expand=1) 
        self.std_table.bind("<ButtonRelease>",self.get_cursor)
        self.fetch_data()
        
    # create the button function to perform the action on "save" button
    def add_data(self):
        if self.var_dep.get()=="Select Department" or self.var_std_name.get() == "" or self.var_std_id.get()=="":
            messagebox.showerror("Error", "All fields are Required",parent=self.root)
        else:
            try:
                self.conn = mysql.connector.connect(host="localhost",username="root",password="Admin@123",database="face_recognition_system")
                self.my_cursor=self.conn.cursor()
                self.my_cursor.execute("insert into student_details (student_id, student_name,department, course, year, semester,  division, roll_no, gender, dob, email, phone, address, teacher_name, photo_sample  ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(

                                                                                                self.var_std_id.get(),
                                                                                                self.var_std_name.get(),
                                                                                                self.var_dep.get(),
                                                                                                self.var_course.get(), 
                                                                                                self.var_year.get(),
                                                                                                self.var_semester.get(),
                                                                                                self.var_div.get(), 
                                                                                                self.var_roll_no.get(),
                                                                                                self.var_gender.get(),
                                                                                                self.var_dob.get(), 
                                                                                                self.var_email.get(),
                                                                                                self.var_phone.get(), 
                                                                                                self.var_address.get(),
                                                                                                self.var_teacher.get(), 
                                                                                                self.var_radio_btn1.get() ))
                self.conn.commit()
                self.fetch_data()
                self.reset_data()
                self.conn.close()
                messagebox.showinfo("Success","Student data has been added successfully!", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due To :{str(es)}", parent=self.root)
                
    # ========================================= Fuction for fetching data to UI's student_table  ===================================
    
    def fetch_data(self):
        self.conn = mysql.connector.connect(host="localhost", username="root", password="Admin@123", database="face_recognition_system")
        self.my_cursor = self.conn.cursor()
        self.my_cursor.execute("select * from student_details")
        self.data = self.my_cursor.fetchall()
        
                
        # if data is fetched update the table and convert the data to the json format
        if len(self.data)!=0:
            # clearing the table after the fetching the data.
            self.std_table.delete(*self.std_table.get_children())
            # insert data into the table of std_table.
            for row in self.data:
                self.std_table.insert("",END,values=row)
            
            
        # close the database connection.
        self.conn.close()
        
# ============= get cursor function for, whenever user click on table entry it is show in entry fields of students details  ===========

    def get_cursor(self,event=""):
        self.cursor_focus = self.std_table.focus()
        self.content = self.std_table.item(self.cursor_focus)
        self.data1 = self.content["values"]
        
        self.var_std_id.set(self.data1[0]),
        self.var_std_name.set(self.data1[1]),
        self.var_dep.set(self.data1[2]),
        self.var_course.set(self.data1[3]), 
        self.var_year.set(self.data1[4]),
        self.var_semester.set(self.data1[5]),
        self.var_div.set(self.data1[6]), 
        self.var_roll_no.set(self.data1[7]),
        self.var_gender.set(self.data1[8]),
        self.var_dob.set(self.data1[9]), 
        self.var_email.set(self.data1[10]),
        self.var_phone.set(self.data1[11]), 
        self.var_address.set(self.data1[12]),
        self.var_teacher.set(self.data1[13]), 
        self.var_radio_btn1.set(self.data1[14])
        
#  ============================= Update button Fuction ====================================================

    def update_data(self):
        if self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                self.Update = messagebox.askyesno("Update", "Do you want to update this student's details?", parent=self.root)
                if self.Update > 0:
                    # Step 1: Establish connection to the database
                    self.conn = mysql.connector.connect(host="localhost", username="root", password="Admin@123", database="face_recognition_system")
                    self.my_cursor = self.conn.cursor()

                    # Step 2: Fetch the original student record
                    original_student_id = self.var_std_id.get()
                    self.my_cursor.execute("SELECT * FROM student_details WHERE student_id=%s", (original_student_id,))
                    student_record = self.my_cursor.fetchone()

                    if student_record:
                        # Step 3: Check if the student_id has changed
                        new_student_id = self.var_std_id.get()

                        if original_student_id != new_student_id:
                            # Step 4: Insert a new record with the updated student_id
                            self.my_cursor.execute(
                                "INSERT INTO student_details (student_id, student_name, department, course, year, semester, division, roll_no, gender, dob, email, phone, address, teacher_name, photo_sample) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                (
                                    new_student_id,
                                    self.var_std_name.get(),
                                    self.var_dep.get(),
                                    self.var_course.get(),
                                    self.var_year.get(),
                                    self.var_semester.get(),
                                    self.var_div.get(),
                                    self.var_roll_no.get(),
                                    self.var_gender.get(),
                                    self.var_dob.get(),
                                    self.var_email.get(),
                                    self.var_phone.get(),
                                    self.var_address.get(),
                                    self.var_teacher.get(),
                                    self.var_photo_sample.get()
                                )
                            )

                            # Step 5: Delete the original record with the old student_id
                            self.my_cursor.execute("DELETE FROM student_details WHERE student_id=%s", (original_student_id,))
                        else:
                            # Step 6: Update the record if student_id has not changed
                            self.my_cursor.execute(
                                "UPDATE student_details SET student_name=%s, department=%s, course=%s, year=%s, semester=%s, division=%s, roll_no=%s, gender=%s, dob=%s, email=%s, phone=%s, address=%s, teacher_name=%s, photo_sample=%s WHERE student_id=%s",
                                (
                                    self.var_std_name.get(),
                                    self.var_dep.get(),
                                    self.var_course.get(),
                                    self.var_year.get(),
                                    self.var_semester.get(),
                                    self.var_div.get(),
                                    self.var_roll_no.get(),
                                    self.var_gender.get(),
                                    self.var_dob.get(),
                                    self.var_email.get(),
                                    self.var_phone.get(),
                                    self.var_address.get(),
                                    self.var_teacher.get(),
                                    self.var_photo_sample.get(),
                                    original_student_id
                                )
                            )

                        # Step 7: Commit the changes
                        self.conn.commit()
                        rows_affected = self.my_cursor.rowcount

                        # Step 8: Provide feedback to the user
                        if rows_affected > 0:
                            messagebox.showinfo("Success", "Student details updated successfully.", parent=self.root)
                        else:
                            messagebox.showinfo("Info", "No records were updated. Please check the student details.", parent=self.root)

                        # Step 9: Refresh data and reset the form
                        self.fetch_data()
                        self.reset_data()

            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)
            finally:
                if self.conn.is_connected():
                    self.conn.close()  # Ensure the connection is closed

            
# ============================== Delete function for button(delete) ================================================
    def delete_data(self):
        if self.var_std_id.get() == "":
            messagebox.showerror("Error","Student Id is Required.",parent=self.root)
            
        else:
            try:
                self.delete=messagebox.askyesno("Confirmation Message"," Do you want delete student info.",parent=self.root)
                if self.delete > 0:
                    self.conn = mysql.connector.connect(host="localhost", username = "root", password="Admin@123", database = "face_recognition_system")
                    self.my_cursor = self.conn.cursor()
                    self.sql = "delete from student_details where student_id = %s"
                    self.val = (self.var_std_id.get(),)
                    self.my_cursor.execute(self.sql,self.val)
                    
                else:
                    if not self.delete:
                        return
                self.conn.commit()
                self.fetch_data()
                self.reset_data()
                self.conn.close()
                messagebox.showinfo("Delete","Data successfully deleted.", parent=self.root)
                
            except Exception as es:
                messagebox.showerror("Error",f"Due To : {str(es)}", parent=self.root)
                
# ================================   function for restet button    =================================================

    def reset_data(self):
        self.var_std_id.set(""),
        self.var_std_name.set(""),
        self.var_dep.set("Select Department"),
        self.var_course.set("Select Course"), 
        self.var_year.set("Select Year"),
        self.var_semester.set("Select Semester"),
        self.var_div.set("Select Division"), 
        self.var_roll_no.set(""),
        self.var_gender.set("Select Gender"),
        self.var_dob.set(""), 
        self.var_email.set(""),
        self.var_phone.set(""), 
        self.var_address.set(""),
        self.var_teacher.set(""), 
        self.var_radio_btn1.set("")
        
# =========================== function for Take a photo sample or generate dataset =======================================
    def generate_dataset(self):
        if self.var_std_id.get() == "" or self.var_std_name.get() == "" or self.var_dep.get() == "Select Department":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return
        else:
            try:
                self.conn = mysql.connector.connect(host="localhost", username="root", password="Admin@123", database="face_recognition_system")
                self.my_cursor = self.conn.cursor()

                # Retrieve and use the student ID
                student_id = int(self.var_std_id.get())  # Convert to integer for further use

                # Update student details in the database
                self.my_cursor.execute("UPDATE student_details SET student_name=%s, department=%s, course=%s, year=%s, semester=%s, division=%s, roll_no=%s, gender=%s, dob=%s, email=%s, phone=%s, address=%s, teacher_name=%s, photo_sample=%s WHERE student_id=%s", (
                    self.var_std_name.get(),
                    self.var_dep.get(),
                    self.var_course.get(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_div.get(),
                    self.var_roll_no.get(),
                    self.var_gender.get(),
                    self.var_dob.get(),
                    self.var_email.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_teacher.get(),
                    self.var_photo_sample.get(),
                    student_id  # Use the student ID for the update
                ))
                self.conn.commit()
                self.fetch_data()
                self.reset_data()
                self.conn.close()

                # =========================== Loading the haarcascade_frontalface_default.xml file =======================================
                if not os.path.exists("image_data"):
                    os.makedirs("image_data")

                self.face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")  # Predefined algorithm to recognize frontal faces.

                def face_cropped(img):
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = self.face_classifier.detectMultiScale(gray, 1.3, 5)  # 1.3 is the scaling factor, 5 = Minimum neighbors.
                    for (x, y, w, h) in faces:
                        cropped_face = img[y:y + h, x:x + w]
                        return cropped_face
                    return None

                self.cap = cv2.VideoCapture(0)
                self.img_id = 0
                
                while True:
                    ret, my_frame = self.cap.read()
                    if ret:
                        cropped_face = face_cropped(my_frame)
                        if cropped_face is not None:
                            self.img_id += 1
                            face = cv2.resize(cropped_face, (450, 450))
                            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                            # Use the student ID from earlier
                            file_path = f"image_data/std.{student_id}.{self.img_id}.jpg"  # Ensure you use the correct student ID
                            cv2.imwrite(file_path, face)
                            cv2.putText(face, str(self.img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
                            cv2.imshow("Cropped Faces", face)

                        if cv2.waitKey(1) == 13 or self.img_id == 100:  # Exit on pressing Enter or capturing 100 images
                            break
                    else:
                        break

                self.cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Success", "Image data generated successfully!", parent=self.root)

            except Exception as es:
                messagebox.showerror("Error", f"Due To : {str(es)}", parent=self.root)

        
        
if __name__ == '__main__':
    root = Tk()
    obj = Student(root)
    root.mainloop()
