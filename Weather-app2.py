from tkinter import *
import requests
from datetime import datetime

def time_format_for_location(utc_with_tz, timezone):
    local_time = datetime.utcfromtimestamp(utc_with_tz + timezone)
    return local_time.strftime('%Y-%m-%d %H:%M:%S')

def showWeather():
    api_key = "f5daf8840578db8cb4c0a5be4a98f513"  # Replace with your OpenWeatherMap API key
 
    city_name = city_value.get()
    weather_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city_name + '&appid=' + api_key
 
    try:
        response = requests.get(weather_url)
        response.raise_for_status()
        weather_info = response.json()

        tfield.delete("1.0", "end")
 
        if weather_info['cod'] == 200:
            kelvin = 273
            temp = int(weather_info['main']['temp'] - kelvin)
            feels_like_temp = int(weather_info['main']['feels_like'] - kelvin)
            pressure = weather_info['main']['pressure']
            humidity = weather_info['main']['humidity']
            sunrise = weather_info['sys']['sunrise']
            sunset = weather_info['sys']['sunset']
            timezone = weather_info['timezone']
            cloudy = weather_info['clouds']['all']
            description = weather_info['weather'][0]['description']
 
            sunrise_time = time_format_for_location(sunrise, timezone)
            sunset_time = time_format_for_location(sunset, timezone)
 
            weather = f"\nWeather of: {city_name}\nTemperature (Celsius): {temp}°\nFeels like in (Celsius): {feels_like_temp}°\nPressure: {pressure} hPa\nHumidity: {humidity}%\nSunrise at {sunrise_time}\nSunset at {sunset_time}\nCloud: {cloudy}%\nInfo: {description}"
        else:
            weather = f"\n\tWeather for '{city_name}' not found!\n\tKindly Enter valid City Name !!"
 
    except requests.RequestException as e:
        weather = "\nError in fetching weather data!"

    tfield.insert(INSERT, weather)

# Initialize Window
root = Tk()
root.geometry("400x400")
root.resizable(0,0)
root.title("Weather App")

# Variable for city input
city_value = StringVar()

# GUI components
Label(root, text='Enter City Name', font='Arial 12 bold').pack(pady=10)
Entry(root, textvariable=city_value, width=24, font='Arial 14 bold').pack()
Button(root, command=showWeather, text="Check Weather", font="Arial 10", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5).pack(pady=20)
Label(root, text="The Weather is:", font='Arial 12 bold').pack(pady=10)
tfield = Text(root, width=46, height=10)
tfield.pack()

root.mainloop()