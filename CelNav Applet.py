import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkcalendar
import math
import pickle
import os
import datetime

global tzone
global dateTime
tzone = 0
dateTime = datetime.date(1900,1,1)

mydir = os.getcwd()
propFile = os.path.join(mydir,'properties.pkl')

global pd
global HTEYE
global IErr
global TZ
global propDict
propDict = {
    "IndexError" : 0,
    "HeightOfEye" : 0,
    "TimeZone" : "GMT 0"
}
pd = propDict
IErr = pd["IndexError"]
HTEYE = pd["HeightOfEye"]
TZ = pd["TimeZone"]

if os.path.exists(propFile):
        if os.path.getsize(propFile) > 0:
            read_in = open('properties.pkl','rb')
            pd = pickle.load(read_in)
            IErr = pd["IndexError"]
            HTEYE = pd["HeightOfEye"]
            TZ = pd["TimeZone"]

class MainWindow(tk.Tk):
    def __init__(self):
        def focus_out(event, obj):
            caller = event.widget
            check = caller.get()

            if not check:
                caller.configure(foreground="gray")

                if obj == self.degree or obj == self.lat or obj == self.lon:
                    caller.insert(END,"Whole Degrees")
                elif obj == self.minute:
                    caller.insert(END,"Decimal Minutes")
                elif obj == self.temp:
                    caller.insert(END,"Decimal Degrees F")
                elif obj == self.pressure:
                    caller.insert(END,"Millibar")
                else:
                    return

        def enter_keypress():
            global sext_deg
            global sext_min
            global tempF
            global tempC
            global pres
            global t_h
            global t_m
            global t_s
            global Long
            global times
            times = self.time.get()
            sext_deg = self.degree.get()
            sext_min = self.minute.get()
            tempF = self.temp.get()
            tempC = (float(tempF) - 32) * (5/9)
            pres = self.pressure.get()
            #Long = self.lon.get()
            print(sext_deg + "\'", sext_min + "\"")
            sight_reduction()

        def textbox_focus(event):
            caller = event.widget
            check = caller.get()

            if check == "Whole Degrees" or check == "Decimal Minutes" \
                or check == "Decimal Degrees F" or check == "Millibar":
                caller.configure(foreground="black")
                caller.delete(0,END)

        def dropdown_change(*args):
            thing = self.celBody.get()

            if thing == "Star":
                body = ttk.Combobox(frm, textvariable=self.starVar, values=Stars)
                body.grid(column=3,row=3)
            elif thing == "Planet":
                body = ttk.Combobox(frm, textvariable=self.planVar, values=Planets)
                body.grid(column=3,row=3)
            else:
                return

        tk.Tk.__init__(self)

        frm = tk.Frame(self)
        frm.grid()

        self.title("SextantBuddy")

        menubar = Menu(self)
        self.file = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu = self.file)
        self.file.add_command(label="Properties",command=properties_window)
        self.file.add_separator()
        self.file.add_command(label="Exit", command=self.destroy)

        self.config(menu=menubar)

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

        self.starVar = tk.StringVar()
        self.planVar = tk.StringVar()
        self.celBody = tk.StringVar()

        tk.Frame(self, width=80).grid(column=0)
        tk.Frame(self, width=100).grid(column=10)

        tk.Label(self, text='Sextant Degrees').grid(column=1, row=0)
        tk.Label(self, text='Sextant Minutes').grid(column=1, row=1)
        tk.Label(self, text='Celestial Body').grid(column=1, row=2)
        tk.Label(self, text='Atm. Pressure').grid(column=4, row=0)
        tk.Label(self, text='Ambient Temp').grid(column=4, row=1)
        tk.Label(self, text='Date').grid(column=4, row=2)
        tk.Label(self, text='Assumed lon').grid(column=6, row=0)
        tk.Label(self, text='Assumed lat').grid(column=6, row=1)

        self.degree = ttk.Entry(self, foreground="gray")
        self.degree.grid(column=2,row=0)
        self.degree.insert(END,"Whole Degrees")
        self.degree.bind('<FocusIn>', textbox_focus)
        self.degree.bind('<FocusOut>',
                         lambda event,obj=self.degree : focus_out(event, obj))

        self.minute = ttk.Entry(self, foreground="gray")
        self.minute.grid(column=2,row=1)
        self.minute.insert(END,"Decimal Minutes")
        self.minute.bind('<FocusIn>', textbox_focus)
        self.minute.bind('<FocusOut>',
                         lambda event,obj=self.minute : focus_out(event, obj))

        self.cb = ttk.Combobox(self, textvariable=self.celBody,
                               values=Celestial)
        self.cb.grid(column=2, row=2)
        self.celBody.trace("w", dropdown_change)

        self.pressure = ttk.Entry(self, foreground="gray")
        self.pressure.grid(column=5,row=0)
        self.pressure.insert(END,"Millibar")
        self.pressure.bind('<FocusIn>', textbox_focus)
        self.pressure.bind('<FocusOut>', 
                    lambda event, obj=self.pressure : focus_out(event, obj))

        self.temp = ttk.Entry(self, foreground="gray")
        self.temp.grid(column=5,row=1)
        self.temp.insert(END,"Decimal Degrees F")
        self.temp.bind('<FocusIn>', textbox_focus)
        self.temp.bind('<FocusOut>',
                       lambda event,obj=self.temp : focus_out(event, obj))

        self.lat = ttk.Entry(self, foreground="gray")
        self.lat.grid(column=7, row=0)
        self.lat.insert(END,"Whole Degrees")
        self.lat.bind('<FocusIn>', textbox_focus)
        self.lat.bind('<FocusOut>',
                      lambda event,obj=self.lat : focus_out(event, obj))

        self.lon = ttk.Entry(self, foreground="gray")
        self.lon.grid(column=7, row=1)
        self.lon.insert(END,"Whole Degrees")
        self.lon.bind('<FocusIn>', textbox_focus)
        self.lon.bind('<FocusOut>',
                      lambda event,obj=self.lon : focus_out(event, obj))

        #time things
        self.date = ttk.Button(self, text="Calendar", command=dateCal)
        self.date.grid(column=5,row=2)

        self.time = time_widget(self, label='Time')

        #buttons
        self.enter = ttk.Button(self, text='Enter', command=enter_keypress)
        self.enter.grid(column=2, row=4)
        self.quitter = ttk.Button(self, text='Quit', command=self.destroy)
        self.quitter.grid(column=2, row=5)

def properties_window():

    def save():
        global tzone
        global pd
        IErr = indexError.get()
        HTEYE = HTE.get()
        TZ = tzn.get()
        tzone = ZONES[TZ]
        propDict["IndexError"] = IErr
        propDict["HeightOfEye"] = HTEYE
        propDict["TimeZone"] = TZ
        pd = propDict
        output = open('properties.pkl','wb')
        pickle.dump(propDict,output)
        props.destroy()
    
    global TZ
    global IErr
    global HTEYE
    global pd

    props = tk.Toplevel()
    props.title("Properties")

    ZONES = {
            "UTC 14" : 14,
            "UTC 13" : 13,
            "UTC 12:45" : 12.75,
            "UTC 12" : 12,
            "UTC 11" : 11,
            "UTC 10:30" : 10.5,
            "UTC 10" : 10,
            "UTC 9:30" : 9.5,
            "UTC 9" : 9,
            "UTC 8:45" : 8.75,
            "UTC 8" : 8,
            "UTC 7" : 7,
            "UTC 6:30" : 6.5,
            "UTC 6" : 6,
            "UTC 5:45" : 5.75,
            "UTC 5:30" : 5.5,
            "UTC 5" : 5,
            "UTC 4:30" : 4.5,
            "UTC 4" : 4,
            "UTC 3:30" : 3.5,
            "UTC 3" : 3,
            "UTC 2" : 2,
            "UTC 1" : 1,
            "UTC 0" : 0,
            "UTC -1" : -1,
            "UTC -2" : -2,
            "UTC -2:30" : -2.5,
            "UTC -3" : -3,
            "UTC -4" : -4,
            "UTC -5" : -5,
            "UTC -6" : -6,
            "UTC -7" : -7,
            "UTC -8" : -8,
            "UTC -9" : -9,
            "UTC -9:30" : -9.5,
            "UTC -10" : -10,
            "UTC -11" : -11,
            "UTC -12" : -12,
        }
    zoneKey = tk.StringVar()
    zoneKey = pd["TimeZone"]

    pfrm = tk.Frame(props)
    pfrm.grid()

    IELabel = tk.Label(pfrm, text="Index Error").grid(column=0,row=0)
    indexError = ttk.Entry(pfrm)
    indexError.insert(END, str(pd["IndexError"]))
    indexError.grid(column=1,row=0)

    ht_eye = tk.Label(pfrm, text="Height of Eye").grid(column=0,row=1)
    HTE = ttk.Entry(pfrm)
    HTE.insert(END, str(pd["HeightOfEye"]))
    HTE.grid(column=1,row=1)

    zone = tk.Label(pfrm, text="Time Zone").grid(column=0,row=2)
    tzn = ttk.Combobox(pfrm, textvariable=zoneKey, values=list(ZONES.keys()))
    tzn.delete(0,END)
    tzn.insert(END, pd["TimeZone"])
    tzn.grid(column=1,row=2)
    
    saveButton = ttk.Button(pfrm, text="Save", 
                            command=save).grid(column=0,row=3)
    cancelButton = ttk.Button(pfrm, text="Cancel", 
                              command=props.destroy).grid(column=1,row=3)

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

        cal = tkcalendar.Calendar(top, font="Arial 14", selectmode='day', 
                                  locale='en_US', mindate=mindate,
                                  maxdate=maxdate, disabledforeground='red',)
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="OK", command=print_sel).pack()

def julian_time():
    if dateTime.month < 3:
        JD_Year = int(dateTime.year) - 1
        JD_Month = int(dateTime.month) + 12
    else:
        JD_Year = int(dateTime.year)
        JD_Month = int(dateTime.month)
    
    JD_Day = int(dateTime.day) + \
        (((int(times['t_h']) + \
           (int(times['t_m']) + int(times['t_s'])/60) / 60) / 24) + tzone)

    global JulianDay
    global JulianDate
    JulianDay = math.modf(365.25 * (JD_Year + 4716))[1] + \
        math.modf(30.6 * (JD_Month + 1))[1] + JD_Day + \
            (2 - math.modf(JD_Year / 100)[1] + \
             math.modf(math.modf(JD_Year / 100)[1] / 4)[1]) - 1524.5
    JulianDate = math.modf(365.25 * (JD_Year + 4716))[1] + \
        math.modf(30.6 * (JD_Month + 1))[1] + dateTime.day + \
            (2 - math.modf(JD_Year / 100)[1] + \
             math.modf(math.modf(JD_Year / 100)[1] / 4)[1]) - 1524.5
    JulianDayYear = math.modf(365.25 * (JD_Year + 4716))[1] + 30 + \
        (2 - math.modf(JD_Year / 100)[1] + \
         math.modf(math.modf(JD_Year / 100)[1] / 4)[1]) - 1524.5 - 0.5

    #check if leap
    if JulianDayYear % 4 == 0:
        bigK = 1
    else:
        bigK = 2

    bigN = math.modf((275 * dateTime.month)/9)[1] - \
        bigK * math.modf((dateTime.month + 9)/12)[1] + JD_Day - 30

    JD0 = math.modf(365.25*(dateTime.year-1))[1] - \
        math.modf(dateTime.year/100)[1] + \
            math.modf(math.modf(dateTime.year/100)[1]/4)[1] + 1721424.5

def sidereal_time():
    global sidTimeGM
    global sidTimeLoc

    bigTDate = ((JulianDate - 2451545) / 36525)
    bigTDay = ((JulianDay - 2451545) / 36525)
    sidTimeGM = (100.46061837 + (36000.770053608 * bigTDate) \
        + (0.000387933 * (bigTDate**2)) - ((bigTDate**3) / 38710000)) % 360
    sidTimeLoc = (280.46061837 + (360.98564736629*(JulianDay-2451545)) \
        + (0.000387933 * (bigTDay**2)) - ((bigTDay**3) / 38710000)) % 360
    
    print(sidTimeLoc)
    
def hour_angle():
    global H

    H = sidTimeLoc - Long - RA

def sight_reduction():
    Hs = (float(sext_deg) + (float(sext_min) / 60))
    dip = (0.97 * math.sqrt(float(HTEYE)))*-1
    refr = (1 / math.tan(Hs + (7.31/(Hs + 4.4)))) * \
        ((float(pres) / 1010)*(283 / tempC))

    Hc = Hs + (float(IErr) + dip + refr)/60

    julian_time()
    sidereal_time()
    


    print(str(Hs) + "\'")
    print("dip:", dip)
    print("refr:", refr)
    print("ALT:", Hc)
    print(JulianDay)

class time_widget(tk.Frame):
    def __init__(self, parent, label):
        tk.Frame.__init__(self, parent)

        self.label = tk.Label(parent, text=label)
        self.label.grid(column=4,row=3)

        self.space = tk.Frame(parent)
        self.space.grid(column=5,row=3)
        
        hourVar = StringVar()
        tminVar = StringVar()
        tsecVar = StringVar()

        self.hour = ttk.Spinbox(self.space,
                                from_=0,
                                to=23,
                                textvariable=hourVar)
        self.hour.insert(END,'00')
        self.hour.configure(width=4, wrap=True)
        self.hour.grid(column=0,row=0)
        
        self.HMColonLabel = tk.Label(self.space,
                                     text=":")
        self.HMColonLabel.grid(column=1,row=0)
        
        self.tmin = ttk.Spinbox(self.space,
                                from_=0,
                                to=59,
                                textvariable=tminVar)
        self.tmin.insert(END,'00')
        self.tmin.configure(width=4, wrap=True)
        self.tmin.grid(column=2,row=0)
        
        self.MSColonLabel = tk.Label(self.space,
                                     text=":")
        self.MSColonLabel.grid(column=3,row=0)
        
        self.tsec = ttk.Spinbox(self.space,
                                from_=0,
                                to=59,
                                textvariable=tsecVar)
        self.tsec.insert(END,'00')
        self.tsec.configure(width=4,wrap=True)        
        self.tsec.grid(column=4,row=0)

    def get(self):
        t_h = self.hour.get()
        t_m = self.tmin.get()
        t_s = self.tsec.get()
        
        global timeData
        timeData = {
            't_h' : t_h,
            't_m' : t_m,
            't_s' : t_s
        }
        return timeData

if __name__ == "__main__":
    root = MainWindow()
    root.mainloop()
