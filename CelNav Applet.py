import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkcalendar
import math
import pickle
import os
import datetime

global HTEYE
global IErr
global dateTime
dateTime = datetime.date(1900,1,1)
root = tk.Tk()
root.title("SextantBuddy")

menubar = Menu(root)

mydir = os.getcwd()
propFile = os.path.join(mydir,'properties.pkl')

propDict = {
    "IndexError" : 0,
    "HeightOfEye" : 0
}
pd = propDict
IErr = pd["IndexError"]
HTEYE = pd["HeightOfEye"]
    
if os.path.exists(propFile):
    if os.path.getsize(propFile) > 0:
        read_in = open('properties.pkl','rb')
        pd = pickle.load(read_in)
        IErr = pd["IndexError"]
        HTEYE = pd["HeightOfEye"]

def properties_window():

    def save():
        IErr = indexError.get()
        HTEYE = HTE.get()
        propDict["IndexError"] = IErr
        propDict["HeightOfEye"] = HTEYE
        output = open('properties.pkl','wb')
        pickle.dump(propDict,output)
        props.destroy()
    
    props = tk.Toplevel()
    props.title("Properties")

    pfrm = tk.Frame(props)
    pfrm.grid()

    IELabel = tk.Label(pfrm, text="Index Error").grid(column=0,row=0)
    indexError = ttk.Entry(pfrm)
    if not pd == None:
        indexError.insert(END, str(pd["IndexError"]))
    indexError.grid(column=1,row=0)

    ht_eye = tk.Label(pfrm, text="Height of Eye").grid(column=0,row=1)
    HTE = ttk.Entry(pfrm)
    if not pd == None:
        HTE.insert(END, str(pd["HeightOfEye"]))
    HTE.grid(column=1,row=1)
    
    saveButton = ttk.Button(pfrm, text="Save", command=save).grid(column=0,row=2)
    cancelButton = ttk.Button(pfrm, text="Cancel", command=props.destroy).grid(column=1,row=2)

file = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu = file)
file.add_command(label="Properties",command=properties_window)
file.add_separator()
file.add_command(label="Exit", command=root.destroy)

root.config(menu=menubar)

frm = tk.Frame(root)
frm.grid()

def dateCal():
        global dateTime

        def print_sel():
            global dateTime
            dateTime = cal.selection_get()
            print(dateTime)
            cal.see(datetime.date(year=2016, month=2, day=5))
            top.destroy()

        top = tk.Toplevel(root)
        top.title("Choose Date")
        top.grab_set()

        today = datetime.date.today()

        mindate = today - datetime.timedelta(days=365000)
        maxdate = today + datetime.timedelta(days=365000)

        cal = tkcalendar.Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                       mindate=mindate, maxdate=maxdate, disabledforeground='red',)
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="OK", command=print_sel).pack()

def enter_keypress():
    global sext_deg
    global sext_min
    global tempF
    global tempC
    global pres
    global t_h
    global t_m
    global t_s
    sext_deg = degree.get()
    sext_min = minute.get()
    tempF = temp.get()
    tempC = (float(tempF) - 32) * (5/9)
    pres = pressure.get()
    t_h = hour.get()
    t_m = tmin.get()
    t_s = tsec.get()
    print(sext_deg + "\'", sext_min + "\"")
    sight_reduction()

def textbox_focus(event):
    caller = event.widget
    check = caller.get()

    if check == "Whole Degrees" or check == "Decimal Minutes" \
        or check == "Decimal Degrees F" or check == "Millibar":
        caller.configure(foreground="black")
        caller.delete(0,END)

def focus_out(event, obj):
    caller = event.widget
    check = caller.get()

    if not check:
        caller.configure(foreground="gray")

        if obj == degree:
            caller.insert(END,"Whole Degrees")
        elif obj == minute:
            caller.insert(END,"Decimal Minutes")
        elif obj == temp:
            caller.insert(END,"Decimal Degrees F")
        elif obj == pressure:
            caller.insert(END,"Millibar")
        else:
            return

def dropdown_change(*args):
    thing = celBody.get()

    if thing == "Star":
        body = ttk.Combobox(frm, textvariable=starVar, values=Stars)
        body.grid(column=3,row=3)
    elif thing == "Planet":
        body = ttk.Combobox(frm, textvariable=planVar, values=Planets)
        body.grid(column=3,row=3)
    else:
        return

def sight_reduction():
    Hs = (float(sext_deg) + (float(sext_min) / 60))
    dip = (0.97 * math.sqrt(float(HTEYE)))*-1
    refr = (1 / math.tan(Hs + (7.31/(Hs + 4.4)))) * ((float(pres) / 1010)*(283 / tempC))

    Hc = Hs + (float(IErr) + dip + refr)/60

    if dateTime.month < 3:
        JD_Year = int(dateTime.year) - 1
        JD_Month = int(dateTime.month) + 12
    else:
        JD_Year = int(dateTime.year)
        JD_Month = int(dateTime.month)
    
    JD_Day = int(dateTime.day) + ((int(t_h) + (int(t_m) + int(t_s)/60) / 60) / 24)

    JD_A1 = math.modf(JD_Year / 100)
    JD_A = JD_A1[1]
    JD_A_DIV = math.modf(JD_A / 4)

    JD_B = 2 - JD_A + JD_A_DIV[1]

    JD_Part1 = math.modf(365.25 * (JD_Year + 4716))
    JD_Part2 = math.modf(30.6 * (JD_Month + 1))
    JD = JD_Part1[1] + JD_Part2[1] + JD_Day + JD_B - 1524.5

    print(str(Hs) + "\'")
    print("dip:", dip)
    print("refr:", refr)
    print("ALT:", Hc)
    print(JD_Day,JD)


    
Celestial = [
    'Sun',
    'Moon',
    'Planet',
    'Star'
]

Stars = [
    'Polaris',
    'Vega',
    'Arcturus',
    'Zuben\'elegenubi'
]

Planets = [
    'Venus',
    'Mars',
    'Jupiter',
    'Saturn'
]

starVar = tk.StringVar()
planVar = tk.StringVar()
celBody = tk.StringVar()

tk.Frame(frm, width=80).grid(column=0)
tk.Frame(frm, width=100).grid(column=10)

tk.Label(frm, text='Alt. Degrees').grid(column=1, row=0)
tk.Label(frm, text='Alt. Minutes').grid(column=1, row=1)
tk.Label(frm, text='Celestial Body').grid(column=1, row=2)
tk.Label(frm, text='Atm. Pressure').grid(column=4, row=0)
tk.Label(frm, text='Ambient Temp').grid(column=4, row=1)
tk.Label(frm, text='Date').grid(column=4, row=2)
tk.Label(frm, text='Time').grid(column=4, row=3)

degree = ttk.Entry(frm, foreground="gray")
degree.grid(column=2,row=0)
degree.insert(END,"Whole Degrees")
degree.bind('<FocusIn>', textbox_focus)
degree.bind('<FocusOut>', lambda event, obj=degree : focus_out(event, obj))

minute = ttk.Entry(frm, foreground="gray")
minute.grid(column=2,row=1)
minute.insert(END,"Decimal Minutes")
minute.bind('<FocusIn>', textbox_focus)
minute.bind('<FocusOut>', lambda event, obj=minute : focus_out(event, obj))

cb = ttk.Combobox(frm, textvariable=celBody, values=Celestial)
cb.grid(column=2, row=2)
celBody.trace("w", dropdown_change)

pressure = ttk.Entry(frm, foreground="gray")
pressure.grid(column=5,row=0)
pressure.insert(END,"Millibar")
pressure.bind('<FocusIn>', textbox_focus)
pressure.bind('<FocusOut>', lambda event, obj=pressure : focus_out(event, obj))

temp = ttk.Entry(frm, foreground="gray")
temp.grid(column=5,row=1)
temp.insert(END,"Decimal Degrees F")
temp.bind('<FocusIn>', textbox_focus)
temp.bind('<FocusOut>', lambda event, obj=temp : focus_out(event, obj))

#time things

date = ttk.Button(frm, text="Calendar", command=dateCal)
date.grid(column=5,row=2)

HOUR = [
    "00",
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23"
]

TMIN = [
    "00",
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
    "26",
    "27",
    "28",
    "29",
    "30",
    "31",
    "32",
    "33",
    "34",
    "35",
    "36",
    "37",
    "38",
    "39",
    "40",
    "41",
    "42",
    "43",
    "44",
    "45",
    "46",
    "47",
    "48",
    "49",
    "50",
    "51",
    "52",
    "53",
    "54",
    "55",
    "56",
    "57",
    "58",
    "59"
]

TSEC = [
    "00",
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
    "26",
    "27",
    "28",
    "29",
    "30",
    "31",
    "32",
    "33",
    "34",
    "35",
    "36",
    "37",
    "38",
    "39",
    "40",
    "41",
    "42",
    "43",
    "44",
    "45",
    "46",
    "47",
    "48",
    "49",
    "50",
    "51",
    "52",
    "53",
    "54",
    "55",
    "56",
    "57",
    "58",
    "59"
]

hourVar = StringVar()
tminVar = StringVar()
tsecVar = StringVar()

hour = ttk.Combobox(frm, textvariable=hourVar, values=HOUR)
hour.grid(column=5, row=3)

HMcolon = tk.Label(frm, text=":").grid(column=6,row=3)

tmin = ttk.Combobox(frm, textvariable=tminVar, values=TMIN)
tmin.grid(column=7, row=3)

MScolon = tk.Label(frm, text=":").grid(column=8,row=3)

tsec = ttk.Combobox(frm, textvariable=tsecVar, values=TSEC)
tsec.grid(column=9, row=3)

enter = ttk.Button(frm, text='Enter', command=enter_keypress)
enter.grid(column=2, row=4)
quitter = ttk.Button(frm, text='Quit', command=root.destroy)
quitter.grid(column=2, row=5)



root.mainloop()
