from tkinter import *
from tkinter import ttk
from customtkinter import * 
import json,requests,os
from csv import *
import subprocess
import shutil
from shutil import copyfile
from tkinter import filedialog,messagebox
import pyqrcode
import smtplib
from PIL import ImageTk,Image
import imghdr
from email.message import EmailMessage
import png
import subprocess
from tkterminal import Terminal

window=CTk()
window.title("Skroman Production")
#window.set_appearance_mode("dark")
window.resizable(0, 0)

#ctk.deactivate_automatic_dpi_awareness()

#set_widget_scaling(1)  # widget dimensions and text size
#set_window_scaling(2)  # window geometry dimensions

window.geometry('1500x760+10+10')
#ctk.enable_macos_darkmode()

####################################################

def esp_fun():
    global data 
    global esp_no
    global unique_id
    global pop

    try:
        #if entry.get():
        esp_no = esp_entry.get()

        ESP_NO = {"ESP_NO": str(esp_no)}
        n_data = json.dumps(ESP_NO)
        URL = "http://13.233.196.149:3000/esptrack/getautoincrement"
        r = requests.get(url=URL, data=ESP_NO)
        data = r.json()
        employee_dict = json.dumps(data)
        res_data = json.loads(employee_dict)
        main_data = res_data['result']
        
        esp_no = main_data['ESP_NO']
        unique_id = main_data['unique_id']
        pop = main_data['POP']
                
        data=(f"ESP_NO:{esp_no}\nUnique_Id:{unique_id}\nPOP:{pop}")
        
        print(data)

        QR()
    except Exception as e:
        messagebox.showerror("Error", f"Please Enter the Currect Value{e}")
        

def QR():
    global img ,qr

    j_creation = {
            "ModelNo": combobox1.get(),
            "ESP_NO": str(esp_no),
            "unique_id": unique_id,
            "POP": pop,
            "DeviceType": combobox2.get()
           }    
    
    if (len(esp_entry.get())!=0 ):

        data = json.dumps(j_creation)
        qr = pyqrcode.create(data)
        img = BitmapImage(data = qr.xbm(scale=5),background="white")
    try:
        display_code()
    except: 
        pass 
def display_code():
        images.configure(image = img) 
        
        showdata.delete('1.0',END)

        showdata.insert(END, f'CLIENT: {entry.get()}\nESP_NO: {esp_no}\nMODULE: {combobox1.get()}\nTYPE: {combobox2.get()}\nUUID: {unique_id}\nPOP: {pop}\nMODE: non-Replica\nPLATE: {combobox3.get()}')        

       
   
def save_qr():
    if qr is not None:

        defaultPath = "D:/Skroman/Skroman QR/"
        
        file_types = [('PNG', '.png')]
        file_name='C:/Espressif/frameworks/esp-idf-v4.4.4/SK/eeprom_elite_module/spiffs_dir/images.png'
        duplicate = defaultPath + unique_id + ".png"
        
        if file_name:
            qr.png(file_name, scale=8)
            qr.png(duplicate, scale=8)
            
qr=None
img=None

#####################################################################################

def email():
    try:
        esp_no=esp_entry.get()
        
        msg = EmailMessage()
        msg['Subject'] = f"Skroman Device (ESP_NO:{esp_no},Unique_Id:{unique_id},POP:{pop},Module:{combobox1.get()},Module Name:{combobox2.get()},no-replica,{combobox3.get()})"        
        msg['From'] = 'teams7602@gmail.com'
        msg['To'] =  'sawantamol048@gmail.com'

        with open('C:/Espressif/frameworks/esp-idf-v4.4.4/SK/eeprom_elite_module/spiffs_dir/images.png',"rb") as f:
            file_data = f.read()
            #print("file send",file_data)
            filetype = imghdr.what(f.name)
            file_name = f.name
            #print("File name is",file_name)
            msg.add_attachment(file_data, maintype="image", subtype=filetype, filename=file_name)
            

        with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
                server.login("teams7602@gmail.com","xksppcalztrlfiwo")
                server.send_message(msg)
                os.remove(file_name)
        messagebox.showinfo("Information", f"Successfully Get")
    except Exception as e:
        messagebox.showerror("Error", f"Email Not send{e}")




def txtfile():
    
    try:
        esp_no=esp_entry.get()
        file_path = os.path.join("C:/Espressif/frameworks/esp-idf-v4.4.4/SK/eeprom_elite_module/spiffs_dir/info", "device_info.txt")
        with open (file_path,'w') as file:
            file.write(f"V1!\n{combobox1.get()}!\n{esp_no}!\n{unique_id}!\n{pop}!\nnon_replica!\n{combobox4.get()}!\n{entry.get()}!")
        list=[esp_no,unique_id,pop,combobox1.get(),combobox2.get(),combobox4.get(),"non-replica"]
    except:
        messagebox.showerror("showerror"," txt file not save")
        
    try:
        esp_no=esp_entry.get()
        file_path2=os.path.join('C:/Espressif/frameworks/esp-idf-v4.4.4','data.csv')
        with open('data.csv','a',newline='') as file:
            Writer=writer(file)
            if file.tell()==0:
                Writer.writerow(["ESP NO","Unique ID","POP","Module","Module Type","plate","Type"])
            Writer.writerow(list)
            #messagebox.showinfo("information","CSV save")
    except:
        messagebox.showerror("showerror","CSV file not save")
        



################## Combo Box ########################

sites = [
    "44010","46000","66010","68000","88010","87020","80000","13000","20000","23000"
]

sites2=[
    
    "Switch Box","2 -Module","MOOD Switch"
]

def callback(*args):
    selection=combobox1.get()

    if selection== "13000":
    
       combobox2.set(sites2[2])
       
    elif selection=="20000":
       
        combobox2.set(sites2[1])
        

    elif selection=="23000":
       
        combobox2.set(sites2[1])
    else:
        
        combobox2.set(sites2[0])



color = ["Black", "White", "Gold", "Silver", "P5", "P6", "P7", "P8", "P9"]
code = ["1","2","3","4", "5", "6", "7", "8", "9"]

def fatch(*args):
    select=combobox3.get()
    
    if select == color[0]:
        combobox4.set(code[0])

    elif select == color[1]:
        combobox4.set(code[1])
        

    elif select == color[2]:
        combobox4.set(code[2])
        
    elif select == color[3]:
        combobox4.set(code[3])

    elif select == color[4]:
        combobox4.set(code[4])

    elif select == color[5]:
        combobox4.set(code[5])

    elif select == color[6]:
        combobox4.set(code[6])

    elif select == color[7]:
        combobox4.set(code[7])

    elif select == color[8]:
        combobox4.set(code[8])




################ third Combo box ###################################


def upload():
    try:
        
        files = filedialog.askopenfilenames(initialdir = "D:/Skroman/Skroman Clients", title = 'Choose a File')
        
        for file in files:
            shutil.copy(file,'C:/Espressif/frameworks/esp-idf-v4.4.4/SK/eeprom_elite_module/spiffs_dir/cert')
                    
        if files:
            file=files[0]
            filename=os.path.basename(file)
            foldername= os.path.basename(os.path.dirname(file))
            entry.delete('0',END)
            entry.insert(0,str(foldername))
            
            clientName = foldername
            
    except :
        messagebox.showerror("Error", "Error: Certificate Not Selected Yet!")
   
####################################################################


def eeprom():
    if esp_entry.get():
        terminal.run_command('sh eeprom_elite_module.sh') 
    else:
        messagebox.showerror("Error", "Certificates Not Selected Yet!")



def burning():
    if esp_entry.get() and entry.get():
        entry.delete('0',END)
        esp_entry.delete('0',END)
        try:
                
            os.remove('C:/Espressif/frameworks/esp-idf-v4.4.4/SK/eeprom_elite_module/spiffs_dir/cert/AmazonRootCA1.pem')
            os.remove('C:/Espressif/frameworks/esp-idf-v4.4.4/SK/eeprom_elite_module/spiffs_dir/cert/certificate.pem.crt')
            os.remove('C:/Espressif/frameworks/esp-idf-v4.4.4/SK/eeprom_elite_module/spiffs_dir/cert/private.pem.key')

            
        except:
            messagebox.showerror("ERROR","Folder is Not Empty")
           
        getModule = combobox1.get()
        
        if getModule == "44010":
           # os.system('start cmd /k "sh build_elite_44010.sh"')
            terminal.run_command('sh build_elite_44010.sh')
           

        elif getModule == "46000":
            #os.system('start cmd /k "sh build_elite_46000.sh"')
             terminal.run_command('sh build_elite_46000.sh')

        elif getModule == "66010":
            #os.system('start cmd /k "sh build_elite_66010.sh"')
             terminal.run_command('sh build_elite_66010.sh')

        elif getModule == "68000":
            #os.system('start cmd /k "sh build_elite_68000.sh"')
             terminal.run_command('sh sh build_elite_68000.sh')

        elif getModule == "88010":
            #os.system('start cmd /k "sh build_elite_88010.sh"')
             terminal.run_command('sh build_elite_88010.sh')

        elif getModule == "87020":
            #os.system('start cmd /k "sh build_elite_87020.sh"')
             terminal.run_command('sh sh build_elite_87020.sh')

        elif getModule == "80000":
            #os.system('start cmd /k "sh build_elite_80000.sh"')
             terminal.run_command('sh build_elite_80000.sh')

        elif getModule == "13000":
            #os.system('start cmd /k "sh build_elite_13000.sh"')
             terminal.run_command('sh build_elite_13000.sh')

        elif getModule == "20000":
            #os.system('start cmd /k "sh build_elite_20000.sh"')
             terminal.run_command('sh eeprom_elite_module.sh')

        elif getModule == "23000":
            #os.system('start cmd /k "sh build_elite_23000.sh"')
             terminal.run_command('sh build_elite_23000.sh')

def dummy1():
    print("ELITE OLD SERVICE INVOKED!")

    if esp_entry.get() and entry.get():
        entry.delete('0',END)
        esp_entry.delete('0',END)
        try:
                
            os.remove('C:/Espressif/frameworks/esp-idf-v4.4.4/SK/eeprom_elite_module/spiffs_dir/cert/AmazonRootCA1.pem')
            os.remove('C:/Espressif/frameworks/esp-idf-v4.4.4/SK/eeprom_elite_module/spiffs_dir/cert/certificate.pem.crt')
            os.remove('C:/Espressif/frameworks/esp-idf-v4.4.4/SK/eeprom_elite_module/spiffs_dir/cert/private.pem.key')

            
        except:
            messagebox.showerror("ERROR","Folder is Not Empty")
           
        getModule = combobox1.get()
        
        if getModule == "44010":
            #os.system('start cmd /k "sh build_elite_old_44010.sh"')
            terminal.run_command('sh build_elite_old_44010.sh')

        elif getModule == "46000":
            #os.system('start cmd /k "sh build_elite_old_46000.sh"')
            terminal.run_command('sh build_elite_old_46000.sh')

        elif getModule == "66010":
            #os.system('start cmd /k "sh build_elite_old_66010.sh"')
            terminal.run_command('sh build_elite_old_66010.sh')

        elif getModule == "68000":
            #os.system('start cmd /k "sh build_elite_old_68000.sh"')
            terminal.run_command('sh build_elite_old_68000.sh')

        elif getModule == "88010":
            #os.system('start cmd /k "sh build_elite_old_88010.sh"')
            terminal.run_command('sh build_elite_old_88010.sh')

        elif getModule == "87020":
            #os.system('start cmd /k "sh build_elite_old_87020.sh"')
            terminal.run_command('sh build_elite_old_87020.sh')

        elif getModule == "80000":
            #os.system('start cmd /k "sh build_elite_old_80000.sh"')
            terminal.run_command('sh build_elite_old_80000.sh')

#####################################################################


label=CTkLabel(window,text="Skroman Production",fg_color="#0b3bcf",width=1480,height=35,corner_radius=6,font=("Arial", 25, "bold"))
label.place(x=10,y=0)
mainframe=CTkFrame(window,fg_color="#000000",border_width=2,border_color="#0b3bcf",width=1480,height=710)
mainframe.place(x=10,y=40)
frame=CTkFrame(mainframe,width=680,height=690,fg_color="#363636",corner_radius=10)
frame.place(x=10,y=10)

frame1=CTkFrame(mainframe,width=760,height=690,fg_color="#363636",corner_radius=10)

terminal = Terminal(mainframe,pady=5,height=53,width=116, padx=5,background="Black",foreground="white",insertbackground="white",borderwidth=2,relief=GROOVE)
terminal.shell = True
terminal.basename= "CMD >>"
terminal.tag_config("basename", foreground="white",font=('calibri',12,'bold'))

terminal.tag_config("output", foreground="white",font=('calibri',12))

terminal.place(x=890,y=15)

#frame1.place(x=700,y=10)

qrframe=CTkFrame(frame,width=300,height=250,fg_color="white",corner_radius=10)
qrframe.place(x=50,y=10)

showdata=CTkTextbox(frame,text_color="black",width=250,height=250,fg_color="white",corner_radius=10)
showdata.place(x=370,y=10)

images =CTkLabel(qrframe,text="") 
images.place(x=20,y=0)


line=CTkFrame(frame,width=600,height=2,fg_color="white",corner_radius=10)
line.place(x=40,y=270)

label=CTkLabel(frame,text="ESP NO.",font=("Arial", 12, "bold"))
label.place(x=100,y=280)

label1=CTkLabel(frame,text="MODULE",font=("Arial", 12, "bold"))
label1.place(x=310,y=280)


label2=CTkLabel(frame,text="PLATE",font=("Arial", 12, "bold"))
label2.place(x=510,y=280)


esp_entry=CTkEntry(frame,width=170,height=25,border_width=2,border_color="white",corner_radius=10)
esp_entry.place(x=50,y=310)

combobox1 = CTkComboBox(frame,width=170,border_width=2,border_color="white",corner_radius=10,values=sites,command=callback)
combobox1.place(x=260,y=310)


combobox2 = CTkComboBox(frame,width=170,border_width=2,border_color="white",corner_radius=10,values=sites2,command=callback)
#combobox2.place(x=450,y=290)

combobox3 = CTkComboBox(frame,width=170,border_width=2,border_color="white",corner_radius=10,values=color,command=fatch)
combobox3.place(x=450,y=310)
combobox4 = CTkComboBox(frame,width=170,border_width=2,border_color="white",corner_radius=10,values=code,command=fatch)
#combobox4.place(x=450,y=290)

framedoc=CTkFrame(frame,width=600,height=105,corner_radius=10)
framedoc.place(x=40,y=360)

label2=CTkLabel(framedoc,text="CLIENT CRTS ",font=("Arial", 14, "bold"))
label2.place(x=90,y=10)


docbutton=CTkButton(framedoc,text="Brows",width=240,corner_radius=15,command=upload)
docbutton.place(x=30,y=40)

label2=CTkLabel(framedoc,text="CLIENT NAME ",font=("Arial", 14, "bold"))
label2.place(x=400,y=10)

entry=CTkEntry(framedoc,width=240,height=30,border_width=2,border_color="white",corner_radius=15)
entry.place(x=340,y=40)


lastframe=CTkFrame(frame,border_width=2,border_color="white",fg_color="#363636",width=600,height=150,corner_radius=10)
lastframe.place(x=40,y=490)


Get_button1=CTkButton(lastframe,text="Get Data",height=40,corner_radius=15,fg_color="#363636",border_width=2,border_color="red",command=lambda:[esp_fun(),save_qr(),txtfile(),email()])
Get_button1.place(x=40,y=20)

button2=CTkButton(lastframe,text="EEPROM",height=40,corner_radius=15,border_width=2,fg_color="#363636",border_color="red",command=eeprom)
button2.place(x=250,y=20)

docbutton3=CTkButton(lastframe,text="BURNING",height=40,corner_radius=15,border_width=2,fg_color="#363636",border_color="red",command=burning)
docbutton3.place(x=430,y=20)

docbutton4=CTkButton(lastframe,text="ELITE-OLD",height=40,corner_radius=15,border_width=2,fg_color="#363636",border_color="red",command=dummy1)
docbutton4.place(x=40,y=80)

docbutton5=CTkButton(lastframe,text="dummy2",height=40,corner_radius=15,border_width=2,fg_color="#363636",border_color="red")
docbutton5.place(x=250,y=80)

docbutton6=CTkButton(lastframe,text="dummy3",height=40,corner_radius=15,border_width=2,fg_color="#363636",border_color="red")
docbutton6.place(x=430,y=80)


window.mainloop()
