from tkinter import *
import requests
import os
from datetime import datetime
import math
from urllib.parse import quote as urlencode
import keyboard

weather_key = os.environ.get("OpenWeatherAPIKey")
geo_key = os.environ.get("GeoapifyAPIKey")

window = Tk()
images_path = os.path.dirname(os.path.abspath(__file__)) + "\\images\\"
images = {
    "icon": "appicon100x100.png",
    "refresh": "refresh50x50.png"
}
icon = PhotoImage(file=images_path+images["icon"])
refreshic = PhotoImage(file=images_path+images["refresh"])

location = None
generated = False

fullscreen = False

window.config(background="#00bfff")

def prepLabel(fonts, clr, rx, ry):
    l = Label(window,
                 font=("Calm", fonts or 15),
                 fg=clr or "white",
                 bg=window["background"])
    l.place(relx=rx or 0.5, rely=ry or 0.5, anchor=CENTER)
    return l

cityl = prepLabel(25, None, None, 0.05)
templ = prepLabel(35, None, None, 0.13)
descl = prepLabel(None, "#c1f0ff", None, 0.19)
maxl = prepLabel(None, None, 0.46, 0.25)
minl = prepLabel(None, None, 0.54, 0.25)
timel = prepLabel(None, None, 0.88, 0.95)
fll = prepLabel(None, None, 0.6, 0.13)
prsl = prepLabel(20, None, 0.3, 0.4)
huml = prepLabel(20, None, 0.5, 0.4)
cll = prepLabel(20, None, 0.7, 0.4)
windl = prepLabel(20, None, 0.5, 0.6)

def get_location():
    resp = requests.get("http://ip-api.com/json").json()

    if resp["status"] == "fail":
        print("Failed to get location based on IP.", resp["message"])
        if not generated:
            quit()
        else:
            return
        
    global location
    location = f'{resp["city"]}, {resp["region"]}, {resp["country"]}'
    return resp["lat"], resp["lon"]

def get_weather():
    resp = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_key}&units=metric").json()
    
    if resp["cod"] != 200:
        print("Failed to get weather.", resp["message"])
        if not generated:
            quit()
        else:
            return

    cityl.config(text=location)
    templ.config(text=str(resp["main"]["temp"])+"\u00b0")
    descl.config(text=resp["weather"][0]["description"])
    maxl.config(text="H:"+str(resp["main"]["temp_max"])+"\u00b0")
    minl.config(text="L:"+str(resp["main"]["temp_min"])+"\u00b0")
    timel.config(text="Time of last refresh: "+datetime.fromtimestamp(resp["dt"]).strftime("%H:%M:%S"),)
    fll.config(text="Feels like:\n"+str(resp["main"]["feels_like"])+"\u00b0")
    prsl.config(text="Pressure:\n"+str(resp["main"]["pressure"])+" hPa")
    huml.config(text="Humidity:\n"+str(resp["main"]["humidity"])+"%")
    cll.config(text="Clouds:\n"+str(resp["clouds"]["all"])+"%")
    windl.config(text="Wind:\n"
               +"Speed - "+str(math.floor(resp["wind"]["speed"]*3.6*100)/100)+" km/h\n"
               +"Direction - "+str(resp["wind"]["deg"])+"\u00b0")
    
def change_location(): #error check
    city = urlencode(city_entry.get())
    resp = requests.get(f"https://api.geoapify.com/v1/geocode/search?text={city}&format=json&apiKey={geo_key}").json()
    try:
        resp["error"]
    except:
        pass
    else:
        print("Failed to change the location.", resp["message"])
        return

    if len(resp["results"]) == 0:
        print("No search results found.")
        return
    
    res = resp["results"][0]
    global lat, lon
    lat, lon = res["lat"], res["lon"]
    global location
    location = res["formatted"]
    get_weather()

def key_input(event):
    global fullscreen
    if event.name == "esc":
        fullscreen = not fullscreen

    window.attributes("-fullscreen", fullscreen)
    
refreshb = Button(window,
                  image=refreshic,
                  command=get_weather,
                  bg=window["background"],
                  relief=FLAT,
                  activebackground=window["background"])
refreshb.place(relx=0.97, rely= 0.05, anchor=CENTER)

city_entry = Entry(window,
                   font=("Calm", 20))
city_entry.place(relx=0.13, rely=0.95, anchor=CENTER)

cntrbtn = Button(window,
                 text="Change location",
                 font=("Calm", 12, "italic"),
                 command=change_location,
                 relief=RAISED)
cntrbtn.place(relx=0.31, rely=0.95, anchor=CENTER)

keyboard.on_press(key_input)

window.title("Weather App v1")
window.geometry("1920x1080")
window.iconphoto(True, icon)

lat, lon = get_location()
get_weather()

generated = True
print("App running")

window.mainloop()