from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from datetime import datetime,date
from PIL import ImageTk, Image
import os
import csv
from tkinter import filedialog

class Attendance:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1920x1080+0+0")
        self.root.title("Attendance Sheet")
        
        # creates the variables for database
        self.var_sr_no = StringVar()
        self.var_student_id = StringVar()
        self.var_student_name = StringVar()
        self.var_roll_no = StringVar()
        self.var_division = StringVar()
        self.var_department =StringVar()
        self.var_entry_time = StringVar()
        self.var_date = StringVar()
        self.var_time = StringVar()
        self.var_attendance = StringVar()
        self.var_exit_time = StringVar()
        self.var_working_hrs = StringVar()
        self.var_attendance_id =StringVar()
    
        # define a custom style with frame border
        style = ttk.Style()
        style.configure("Custom.TFrame", background="White", bordercolor="blue", borderwidth=5, relief="solid")

        #outer frame using the ttk for custom styled border
        self.outer_frame = ttk.Frame(self.root, style="Custom.TFrame")
        self.outer_frame.place(x=10,y=50,width = 1850,height = 900)
        
        # Creating the Title label on the webpage
        self.title = Label(self.root, text= "Attendance Sheet", font=("Vnadalia", 35, "bold"), bg="white",fg="black")
        self.title.place(x=640,y=0, width=1260, height=55, anchor="n" )
        
        # main content frame inside the outer frame without any border
        self.main_frame = Frame(self.outer_frame, bg="white")
        self.main_frame.place(x=10,y=10, width=1830, height=880)
        
        # two horizontal frames 
        
        # left frame
        self.left_frame = LabelFrame(self.main_frame, text="Student Details", font=("times new roman", 20, "bold"))
        self.left_frame.place(x=5,y=10, width= 600, height=550)
        
        # creating the label of Attendance ID
        self.att_label = Label(self.left_frame, text="Attendance ID : ", font=("times new roman", 15), fg="black")
        self.att_label.grid(row=0,column=0, padx=5,pady=5)
        # creating the entry field for the Attendance id
        self.att_id_entry = ttk.Entry(self.left_frame,textvariable=self.var_attendance_id,width=25,font=("times new roman", 15, "bold"))
        self.att_id_entry.grid(row=0,column=1,padx=10,pady=10,sticky=W) 
        
        # creating the label for the Student Frame
        self.std_nm_label = Label(self.left_frame, text= "Student Name :", font= ("times new roman",15), fg="black")
        self.std_nm_label.grid(row=1, column=0, padx=10, pady=10)
        # creating the entry fields for the stduents name'
        self.std_nm_entry = ttk.Entry(self.left_frame,textvariable=self.var_student_name, width=25,font=("times new roman", 15) )
        self.std_nm_entry.grid(row=1, column = 1, padx=10, pady=10,sticky=W)
        
        # creating the label for the Roll Number 
        self.roll_label = Label(self.left_frame, text="Roll No :", font=("times new roman", 15,))
        self.roll_label.grid(row=2, column=0,padx=10,pady=10)
        #creating the entry field for the roll_no 
        self.roll_entry = ttk.Entry(self.left_frame,textvariable=self.var_roll_no, width=25,font=("times new roman", 15))
        self.roll_entry.grid(row = 2, column=1, padx= 10, pady=10,sticky=W)
        
        #creating the label for the Division 
        self.div_label = Label(self.left_frame, text= "Division : ", font=("times new roman",15))
        self.div_label.grid(row=3,column=0, padx=10, pady=10)
        #creating the entry for the division
        self.div_entry = ttk.Entry(self.left_frame,textvariable=self.var_division, width=25, font=("times new roman", 15))
        self.div_entry.grid(row=3,column=1, padx=10, pady=10,stick=W)
        
        # ctreating the label for the department
        self.dep_label = Label(self.left_frame, text= "Department : ", font=("times new roman", 15))
        self.dep_label.grid(row=4, column=0, padx= 10, pady=10)
        #creating the entry for the department
        self.dep_entry = ttk.Entry(self.left_frame, textvariable=self.var_department, width=25,font=("times new roman", 15))
        self.dep_entry.grid(row=4, column=1, padx= 10, pady=10, sticky=W)
        
        #creating the label for the Time
        self.time_label = Label(self.left_frame, text="Time : ", font=("times new roman",15))
        self.time_label.grid(row=5, column=0, padx=10, pady=10)
        # creating the Entry for the Time
        self.time_entry = ttk.Entry(self.left_frame,textvariable=self.var_time, width=25, font=("times new roman", 15))
        self.time_entry.grid(row=5, column=1, padx=10, pady=10, sticky=W)
        
        #creating the label for the Date
        self.date_label = Label(self.left_frame, text="Date : ", font=("times new roman",15))
        self.date_label.grid(row=6, column=0, padx=10, pady=10)
        # creating the Entry for the Date
        self.date_entry = ttk.Entry(self.left_frame, textvariable=self.var_date, width=25, font=("times new roman", 15))
        self.date_entry.grid(row=6, column=1, padx=10, pady=10, sticky=W)
        
        #creating the label for the Attendance Status
        self.att_sts_label = Label(self.left_frame, text="Attendance Status : ", font=("times new roman",15))
        self.att_sts_label.grid(row=7, column=0, padx=10, pady=10)
        # create and place combobox
        self.att_stscombo = ttk.Combobox(self.left_frame,width=29, textvariable=self.var_attendance,font = ("times new roman", 12, "bold"), state="readonly")
        self.att_stscombo["values"]=("Select Status","Present","Absent")
        self.att_stscombo.current(0)
        self.att_stscombo.grid(row=7,column=1,padx=2,pady=10)
        
        # ======================   Buttons Frame   ======================================================
        self.btn_frm = Frame(self.left_frame, bd=2, relief=RIDGE, bg="white")
        self.btn_frm.place(x=2, y=400, width=590, height=110)
        
        # import button
        self.import_btn = Button(self.btn_frm, text="IMPORT", font=("times new roman",13,"bold"), bg="green",fg="white")
        self.import_btn.place(x=20, y=25, width=100, height=40)
        
        # Export button
        self.export_btn = Button(self.btn_frm, text="EXPORT", font=("times new roman",13,"bold"), bg="green",fg="white")
        self.export_btn.place(x=160, y=25, width=100, height=40)
        
        # Update Button
        self.update_btn = Button(self.btn_frm, text="UPDATE", font=("times new roman",13,"bold"), bg="green",fg="white")
        self.update_btn.place(x=300, y=25, width=100, height=40)
        
        # Reset Button
        self.reset_btn = Button(self.btn_frm, text="RESET", font=("times new roman",13,"bold"), bg="green",fg="white")
        self.reset_btn.place(x=440, y=25, width=100, height=40)
        
# ================================================================================================================================        
        #Right Frame
        self.right_frame = LabelFrame(self.main_frame, text="Catalogue", font=("times new roman", 20, "bold"))
        self.right_frame.place(x=630,y=10, width= 600, height=550)
        
        # inside frame
        self.table_frame = LabelFrame(self.right_frame, bd=2, relief=RIDGE, bg="white")
        self.table_frame.place(x=10, y=2, width=570, height=510)
        
        # scroll bar of the table
        self.scroll_x = ttk.Scrollbar(self.table_frame,orient="horizontal")
        self.scroll_y = ttk.Scrollbar(self.table_frame, orient="vertical" )
        
        self.AttendanceReport = ttk.Treeview(self.table_frame,column=("sr.no","id","name","roll no","division","department","entry","date","attendance","exit","working hrs"),xscrollcommand=self.scroll_x.set,yscrollcommand=self.scroll_y.set)
        
        # using the pack palce the scrollbars
        self.scroll_x.pack(side=BOTTOM,fill=X)
        self.scroll_y.pack(side=RIGHT,fill=Y)
        
        self.scroll_x.config(command=self.AttendanceReport.xview)
        self.scroll_y.config(command=self.AttendanceReport.yview)
        
        # giving the column name into the table frame
        self.AttendanceReport.heading("sr.no",text="Sr.No")
        self.AttendanceReport.heading("id",text="Attendance_Id")
        self.AttendanceReport.heading("name",text="Student Name")
        self.AttendanceReport.heading("roll no", text="Roll No")
        self.AttendanceReport.heading("division", text="Division")
        self.AttendanceReport.heading("department",text="Department")
        self.AttendanceReport.heading("entry",text="Entry Time")
        self.AttendanceReport.heading("date", text="Date")
        self.AttendanceReport.heading("attendance", text="Attendance Status")
        self.AttendanceReport.heading("exit", text="Exit Time")
        self.AttendanceReport.heading("working hrs", text="Active Hours")
        
        # set the column width 
        self.AttendanceReport.column("sr.no",width=50)
        self.AttendanceReport.column("id",width=100)
        self.AttendanceReport.column("name",width=100)
        self.AttendanceReport.column("roll no",width=100)
        self.AttendanceReport.column("division",width=100)
        self.AttendanceReport.column("department",width=100)
        self.AttendanceReport.column("entry",width=100)
        self.AttendanceReport.column("date",width=100)
        self.AttendanceReport.column("attendance",width=130)
        self.AttendanceReport.column("exit",width=100)
        self.AttendanceReport.column("working hrs",width=130)
        
        self.AttendanceReport['show']='headings'
        self.AttendanceReport.pack(fill=BOTH, expand=1)
        
        
#  =======================          backend     =======================================================================

# function for the import button
    def import_button(self):
        try:
            self.conn = mysql.connector.connect(host="localhost", username="root", password="Admin@123", database="face_recognition_system")
            self.my_cursor = self.conn.cursor()
            self.my_cursor.execute("select * from attendance")
            self.rows=self.my_cursor.fetchall()
            
            for i in self.AttendanceReport.get_children():# for clearing the table 
                self.AttendanceReport.delete(i)
                
            for row in self.rows:
                self.AttendanceReport.insert(" ", END, values=row)
                
            messagebox.showinfo("Success", "Data imported successfully")
            
        except Exception as es:
            messagebox.showerror("Error", f"Due To : {str(es)}")
            
        finally:
            if self.conn.is_connected():
                self.my_cursor.close()
                self.conn.close()
            
    # functionality for the export button
    def export_button(self):
        try:
            # provide the choice to user where to and in which file data is store
            self.filepath = filedialog.asksaveasfilename(initialdir="/", title="SaveCSV", filetypes=(("CSV FILES", "*.csv"),("All files", "*.csv")), defaultextension = ".csv")
            
            # after the choose the file path
            if self.filepath:
                #open the file in write mode
                with open(self.file_path, mode="w", newline="\n") as file:
                    writer = csv.writer(file, delimiter=",")
                    
                # exporting the column names / headings of the table
                columns = [col for col in self.AttendanceReport["columns"]]
                writer.writerow(columns)
                
                # fetch attendance data from the treeview
                for  row_id in self.AttendanceReport.get_children():
                    row =self.AttendanceReport.item(row_id)['values']
                    writer.writerow(row)
                    
            messagebox.showinfo("Success"," Data exported successfully.")
            
        except Exception as es:
            messagebox.showerror("Error","Due To :{str(es)}")
                
        
                
    # functionality for the update attendance button
    def update_attendance(self):
        try:
            # fetching the data from the entry fields
            attendance_id = self.var_attendance_id.get()
            student_name = self.var_student_name.get()
            roll_no = self.var_roll_no.get()
            division = self.var_division.get()
            department = self.var_department.get()
            entry_time = self.var_entry_time.get()
            date = self.var_date.get()
            attendance_status = self.var_attendance.get()
            exit_time = self.var_exit_time.get()
            working_hrs = self.var_working_hrs.get() 
            
            # check for attendance id
            if attendance_id == "":
                messagebox.showerror("Error", "Attendance Id is mandatory.")
                return
            
            # database connection for updfating data into the database
            self.conn = mysql.connector.connect(host="localhost", username="root", password="Admin@123", database="face_recognition_attendance_system")
            self.my_cursor = self.conn.cursor()
            self.my_cursor.execute(("update attendance set student_name = %s, roll_no = %s, division = %s, department = %s, entry = %s, date = %s, attendance = %s , exit = %s, working_hrs = %s where attendance_id = %s"), (student_name, roll_no, division, department, entry_time, date,  attendance_status, exit_time, working_hrs, attendance_id))
            self.conn.commit()
            
            # update the records in treeview
            selected = self.AttendanceReport.focus()
            if not selected:
                messagebox.showerror("Error", "Please select an entry to update.")
                return
            
            self.AttendanceReport.item(selected, values=
                                       (
                                           student_id, student_name, roll_no, division, department, entry_time, attendance_status, exit_time, working_hrs, attendance_id
                                       )
                                       ) 
            messagebox.showinfo("Success", "Data Updated successfully.")   
            
        except Exception as es:
            messagebox.showerror("Error", f"Due To : {str(es)}")
            
        finally:
            if self.conn.is_connected():
                self.my_cursor.close()
                self.conn.close()  
                
# functionality for the Reset button
    def rest_button(self):
        self.var_attendance_id.set("")
        self.var_student_name.set("")
        self.var_roll_no.set("")
        self.var_division.set("")
        self.var_department.set("")
        self.var 
        
        
        
        






#==============================================================================================================        
if __name__=="__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()