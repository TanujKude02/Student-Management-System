import socket
import requests
import bs4
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import datetime
root = Tk()
root.title("S.M.S")
root.geometry("700x500+400+200")
root.configure(background = "RosyBrown1")
class MyException(Exception):
	def __init__(self , msg):
		self.msg = msg

def loc():
	try:
		socket.create_connection( ("www.google.com", 80))
		res = requests.get("https://ipinfo.io/")
		data = res.json()                 
		loc = data['city']
		return loc 
	except Exception as e:
		showerror("Failure",str(e))
def temp():
	try:
		a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
		a2 = "&q= MUMBAI"
		a3 = "&appid=c6e315d09197cec231495138183954bd"
		api_address = a1 + a2 + a3
		res = requests.get(api_address)
		data = res.json()
		m = data['main']
		temper = m['temp']
		return temper
	except Exception as e:
		showerror("Failure",str(e))
def QOTD():
	try:
		res = requests.get("https://www.brainyquote.com/quote_of_the_day")
		soup = bs4.BeautifulSoup(res.text , "lxml")
		data = soup.find("img" , {"class": "p-qotd"}) 
		qotd = data['alt']
		motd = qotd.split(" ")
		if len(motd) > 8:
			motd.insert(9,'\n')
		qotd = " ".join(motd)
		return qotd
	except Exception as e:
		showerror("Failure",str(e))

#design of root window
def f1():
	adst.deiconify()
	root.withdraw()
def f3():
	stdata.delete(1.0, END)
	visit.deiconify()
	root.withdraw()
	con = None
	try:
		con = connect("sms.db")
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		info =""
		for d in data:
			data.sort()
		for d in data:
			info = info + "rno: " +str(d[0]) +" name: " + str(d[1]) +" marks: " +  str(d[2]) +"\n"
		stdata.insert(INSERT , info)
	except Exception as e:
			showerror("Failure" , "select issue")
	finally:
		if con is not None:
			con.close()
def f5():
	upst.deiconify()
	root.withdraw()
def f7():
	dlst.deiconify()
	root.withdraw()
def chart():
	name , marks = [] , []
	con = None
	try:
		con = connect("sms.db")
		cursor = con.cursor()
		sql = "select * from student order by marks DESC"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			name.append(d[1])
			marks.append(d[2])
		plt.bar(name[:5] , marks[:5] , color =['red','green','blue','orange','green'])
		plt.title("Batch Information")
		plt.xlabel("Name")
		plt.ylabel("Marks") 
		plt.grid()
		plt.show()
	except Exception as e:
		showerror("Failure", "selection issue")
		con.rollback()
	finally:
		if con is not None:
			con.close()
btnAdd = Button(root , text = "Add" , width=10,font=("arial",18,"bold"), command = f1)
btnView = Button(root , text = "View",width=10, font=("arial",18,"bold"), command = f3)
btnUpdate = Button(root , text = "Update" ,width=10, font=("arial",18,"bold"), command = f5)
btnDelete = Button(root , text = "Delete" ,width=10,font=("arial",18,"bold") , command=f7)
btnCharts = Button(root , text = "Charts" ,width=10, font=("arial",18,"bold"), command = chart) 
lblLoc = Label(root , text="Location: ",background="RosyBrown1",font = ("calibri", 18,"bold"))
lblTemp = Label(root , text="Temp: " ,background="RosyBrown1",font=("calibri",18,"bold"))
lblQo = Label(root , text = "QOTD:",background="RosyBrown1",font=("calibri",18,"bold"))
lblL = Label(root , text=loc() ,background="RosyBrown1",font=("calibri",18,"bold"))
lblT = Label(root , text=temp() ,background="RosyBrown1",font=("calibri",18,"bold"))
lblQ = Label(root, text=QOTD(),background="RosyBrown1", font=("calibri",18,"bold"))
btnAdd.pack(pady=5)
btnView.pack(pady=5)
btnUpdate.pack(pady=5)
btnDelete.pack(pady=5)
btnCharts.pack(pady=5)
lblLoc.place(x=20,y=350)
lblL.place(x=130,y=351)
lblTemp.place(x=300,y=350)
lblT.place(x=400,y=350)
lblQo.place(x=20,y=400)
lblQ.place(x=100,y=400)

# design of Add stu.
def f2():
	root.deiconify()
	adst.withdraw()
def save1():
	con = None
	try:
		con = connect("sms.db")
		r = int(entrno.get())
		if r < 0:
			raise MyException("Roll no. should be positive")
		n = entname.get()
		if len(n) < 2 or n.isdigit():
			raise MyException("Name should have atleast two characters")
		m = int(entmarks.get())
		if (m>100 or m<0):
			raise MyException("Marks should be positive and less than 101")
		args = (r , n, m)
		cursor = con.cursor()
		sql = "insert into student values('%d' , '%s' , '%d')"
		cursor.execute(sql % args)
		con.commit()
		showinfo("Success" , "Record Added")
		entrno.delete(0,END)
		entname.delete(0,END)
		entmarks.delete(0,END)
	except ValueError:
		showerror("Failure" , "insert positive integers only")
		#con.rollback()
	except Exception as e:
		showerror("Failure" , "insert issue " + str(e))
		con.rollback()
	finally:
		if con is not None:
			con.close()
adst = Toplevel(root)
adst.title("Add St.")
adst.geometry("500x500+400+200")
adst.configure(background= "cyan")
adst.withdraw()

lblrno = Label(adst , text="enter rno:",background="cyan" ,font=("arial",20,"bold"))
entrno = Entry(adst , bd=5,font=("arial",20,"bold"))
lblname = Label(adst ,text = "enter name:",background="cyan" ,font=("arial",20,"bold"))
entname = Entry(adst , bd=5,font=("arial",20,"bold"))
lblmarks = Label(adst,text = "enter marks:",background="cyan" ,font=("arial",20,"bold"))
entmarks = Entry(adst , bd=5,font=("arial",20,"bold"))
btnSave = Button(adst , text="Save",width=10,font=("arial",20,"bold"), command=save1)
btnBack = Button(adst , text="Back",width=10,font=("arial",20,"bold"), command=f2)
lblrno.pack(pady=5)
entrno.pack(pady=5)
lblname.pack(pady=5)
entname.pack(pady=5)
lblmarks.pack(pady=5)
entmarks.pack(pady=5)
btnSave.pack(pady=5)
btnBack.pack(pady=5)

# design of View St.
def f4():
	root.deiconify()
	visit.withdraw()

visit = Toplevel(root)
visit.title("View St.")
visit.geometry("500x500+400+200")
visit.configure(background = "pale goldenrod")
visit.withdraw()

stdata = ScrolledText(visit , width = 40 , height = 10)
btnBack = Button(visit , text= "Back", width=10, font=("calibri",20,"bold"), command = f4)
stdata.pack(pady=10)
btnBack.pack(pady=10)

# design of Update St.
def f6():
	root.deiconify()
	upst.withdraw()
def save2():
	con = None
	try:
		con = connect("sms.db")
		rol = int(entrol.get())
		if rol < 0:
			raise MyException("Roll no. should be positive")
		na = entna.get()
		if len(na) < 2 or na.isdigit():
			raise MyException("Name should have atleast two characters")
		mark = int(entmark.get())
		if (mark>100 or mark<0):
			raise MyException("Marks should be positive and less than 101")
		args = (na , mark , rol)
		cursor = con.cursor()
		sql = "update student set name = '%s',marks = '%d' where rno = '%d'"
		cursor.execute(sql % args)
		if cursor.rowcount >= 1:
			con.commit()
			showinfo("Success" , "Record updated")
		else:
			showerror("Failure" ,"Roll no. does not exist")
		entrol.delete(0,END)
		entna.delete(0,END)
		entmark.delete(0,END)
	except ValueError:
		showerror("Failure" , "insert positive integers only")
	except Exception as e:
		showerror("Faliure", "Update issue " + str(e))
		con.rollback()
	finally:
		if con is not None:
			con.close()

upst= Toplevel(root)
upst.title("Update St.")
upst.geometry("500x500+400+200")
upst.configure(background = "RosyBrown1")
upst.withdraw()

lblrol = Label(upst , text="enter rno:",background="RosyBrown1" ,font=("arial",20,"bold"))
entrol = Entry(upst , bd=5,font=("arial",20,"bold"))
lblna = Label(upst ,text = "enter name:",background="RosyBrown1" ,font=("arial",20,"bold"))
entna = Entry(upst , bd=5,font=("arial",20,"bold"))
lblmark = Label(upst,text = "enter marks:",background="RosyBrown1" ,font=("arial",20,"bold"))
entmark = Entry(upst , bd=5,font=("arial",20,"bold"))
btnSave = Button(upst , text="Save",width=10,font=("arial",20,"bold"), command = save2)
btnBack = Button(upst , text="Back",width=10,font=("arial",20,"bold"), command = f6)
lblrol.pack(pady=5)
entrol.pack(pady=5)
lblna.pack(pady=5)
entna.pack(pady=5)
lblmark.pack(pady=5)
entmark.pack(pady=5)
btnSave.pack(pady=5)
btnBack.pack(pady=5)

#design of Delete St.
def f8():
	root.deiconify()
	dlst.withdraw()
def delete():
	con = None
	try:
		con = connect("sms.db")
		ro = int(entro.get())
		args = (ro)
		cursor = con.cursor()
		sql = "delete from student where rno = '%d'"
		cursor.execute(sql % args)
		if cursor.rowcount >= 1:
			con.commit()
			showinfo("Success" , "Record Deleted")
			entro.delete(0,END)
		else:
			showerror("Failure" ,"roll no. does not exist")
	except Exception as e:
		showerror("Failure" , "positive integers only")
		con.rollback()
	finally:
		if con is not None:
			con.close()

dlst =Toplevel(root)
dlst.title("Delete St.")
dlst.geometry("500x400+400+200")
dlst.configure(background="sky blue")
dlst.withdraw()

lblro = Label(dlst , text="enter rno:",background="sky blue" ,font=("arial",20,"bold"))
entro = Entry(dlst , bd=5,font=("arial",20,"bold"))
btnSave = Button(dlst , text="Delete",width=10,font=("arial",20,"bold"), command = delete)
btnBack = Button(dlst , text="Back",width=10,font=("arial",20,"bold"), command =f8)
lblro.pack(pady=5)
entro.pack(pady=5)
btnSave.pack(pady=5)
btnBack.pack(pady=5)

root.mainloop()