import pandas as pd
import requests

## Dummy DataFrame for testing
df = pd.DataFrame(
    {
        "City": ["Buenos Aires", "Brasilia", "Santiago", "Bogota", "Caracas"],
        "Latitude": [-34.58, -15.78, -33.45, 4.60, 10.48],
        "Longitude": [-58.66, -47.91, -70.66, -74.08, -66.86],
    }
)

# Function to construct url based on lat-long pairs
def generate_url(_lat, _lng):
    coord_API_endpoint = "https://pro.openweathermap.org/data/2.5/forecast/climate?"
    lat_long = "lat=" + str(_lat) + "&lon=" + str(_lng)
    join_key = "&appid=" + "xyz"        ##Replace xyz with Key
    units = "&units=metric"
    weather_url = coord_API_endpoint + lat_long + join_key + units
    return weather_url


# Initializing an empty DataFrame
data = pd.DataFrame()

# Loading JSON returned by openweather to a pandas dataframe
for row in range(len(df)):
    lat = df["Latitude"].values[row]
    long = df["Longitude"].values[row]
    city_s = df["City"].values[row]

    # Acquiring JSON data
    forecast_json_data = requests.get(generate_url(lat, long)).json()

    df_predictions = pd.DataFrame()

    prediction_num = 0

# Defining empty lists
    date = []
    city = []
    latitude = []
    longitude = []
    temp = []
    temp_min = []
    temp_max = []
    wind_speed = []
    rain = []
    snow = []
    humidity = []

# Running loop to query data from JSON into an empty list
    for num_forecasts in forecast_json_data['list']:
        date.append(forecast_json_data['list'][prediction_num]['dt'])
        city.append(forecast_json_data['city']['name'])
        latitude.append(forecast_json_data['city']['coord']['lat'])
        longitude.append(forecast_json_data['city']['coord']['lon'])
        temp.append(forecast_json_data['list'][prediction_num]['temp']['day'])
        temp_min.append(
            forecast_json_data['list'][prediction_num]['temp']['min'])
        temp_max.append(
            forecast_json_data['list'][prediction_num]['temp']['max'])
        wind_speed.append(forecast_json_data['list'][prediction_num]['speed'])
        humidity.append(forecast_json_data['list'][prediction_num]['humidity'])
        try:
            rain.append(forecast_json_data['list'][prediction_num]['rain'])
            snow.append(forecast_json_data['list'][prediction_num]['snow'])
        except:
            pass

        prediction_num += 1

# Populating dataframe columns
    df_predictions['Date'] = date
    df_predictions['City'] = city_s
    df_predictions['TAVG_Forecast'] = temp
    df_predictions['TMIN_Forecast'] = temp_min
    df_predictions['TMAX_Forecast'] = temp_max
    df_predictions['WINDSPEED_Forecast'] = wind_speed
    df_predictions['HUMIDITY_Forecast'] = humidity
    try:
        df_predictions['PRCP_Forecast'] = rain
        df_predictions['SNOW_Forecast'] = snow
    except ValueError:
        df_predictions['PRCP_Forecast'] = 0
        df_predictions['SNOW_Forecast'] = 0


    df_predictions["Date"] = pd.to_datetime(
        df_predictions['Date'], unit='s').dt.date

    data = pd.concat([data, df_predictions])
    


data = data[["Date", "City",
             "TAVG_Forecast", "TMIN_Forecast", "TMAX_Forecast", "WINDSPEED_Forecast", "HUMIDITY_Forecast", "PRCP_Forecast", "SNOW_Forecast"]]

print(data)