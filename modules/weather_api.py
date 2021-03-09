def commands():
    comm = [
            ["what's the weather"]
            ]
    classify = [
            "exact"
            ]
    return comm, classify

def getWeather(city_name):
        #reference https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/
        api_key = "5985bc671ecc377555ecb761fbc53914"
        base_url = "http://api.openweathermap.org/data/2.5/weather?q="
        msg = "\nusing city: "+city_name

        complete_url = base_url + city_name + "&appid=" + api_key 
        response = requests.get(complete_url)
        x = response.json()

        if x["cod"] != "404" and city_name.strip() != "": #404 = city not found                
                y = x["main"]
                current_temperature = y["temp"]
                current_pressure = y["pressure"] 
                current_humidiy = y["humidity"] 
                z = x["weather"] 
                weather_description = z[0]["description"]
                temperature = "{0:.2f}".format(current_temperature * 9 / 5 - 459.65) #temperature in celcius converted to fahrenheit
                #message for printing all values
                msg = (msg + " Temperature in degrees Fahrenheit = " +
                                temperature + 
                        "\n atmospheric pressure in hPa unit = " +
                                str(current_pressure) +
                        "\n humidity in percentage = " +
                                str(current_humidiy) +
                        "\n description = " +
                                weather_description +
                                "\n") 
                return msg, None
        else:
                msg += " City Not Found \n"
                return msg, None
        return 0
