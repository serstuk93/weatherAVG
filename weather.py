import requests
from datetime import datetime,timedelta
import itertools
import pandas as pd
import json
import plotly
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


today = forecast_days = datetime.today().replace(microsecond=0, minute=0, second=0)
cur_time = str(datetime.today().replace(microsecond=0))
print(cur_time)
forecast_days = str(forecast_days + timedelta(days=7))[:10].split("-")
today = str(today)[:10].split("-")

weather_data={}
weather_data1={}
weather_data2={}
weather_data3={}
city=""
api_key = open("api_key", "r").read()
units = "metric"
global lang 
lang = "en"
coordinates = [0,0] # long, lat
first_day_dict = {} 
open_meteo_avg={}

def openweather(city , language):
    global coordinates
    api_url = f'https://api.openweathermap.org/data/2.5/forecast?id=524901&appid={api_key}&units={units}&lang={language}&q={city}'
    api_get = requests.get(api_url)
    api_get_data = api_get.json()
    # error handlers 
    if api_get_data['message'] == 'city not found':
        api_get_data = ""
        return '404'
    if api_get_data["city"]['name']== "None":
        api_get_data = ""
        return '404'
    
    coordinates = [api_get_data["city"]["coord"]["lon"] , api_get_data["city"]["coord"]["lat"]]
    for p in api_get_data["list"]:
        weather_data1[p["dt_txt"]] = {"weather_decription" : p["weather"][0]["description"],
                                    "temperature":p["main"]["temp"],
                                    "feels_like" : p["main"]["feels_like"],
                                    "max_temp" : p["main"]["temp_max"],
                                    "min_temp" : p["main"]["temp_min"],
                                    "wind_speed" : p["wind"]["speed"],
                                    "humidity" : p["main"]["humidity"],
                                    "precipitation" : p["rain"]["3h"] if "rain" in p else "0",
                                    "weather-main" : p["weather"][0]["main"],
                                    "weather-icon" : ("http://openweathermap.org/img/w/%s.png" %p["weather"][0]["icon"]),
                                    "weather-icon2" : ("http://openweathermap.org/img/wn/%s@2x.png" %p["weather"][0]["icon"])
                                    
                                    }
    global act_time 
    global first_day_dict
    first_day_dict = dict(itertools.islice(weather_data1.items(), 9))
    act_time = list(first_day_dict.keys())[0]
    return coordinates


### open-meteo
def open_meteo():
    api_url2= f'https://api.open-meteo.com/v1/forecast?latitude={coordinates[1]}&longitude={coordinates[0]}&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation,windspeed_10m&daily=temperature_2m_max,temperature_2m_min&timezone=auto'
    api_get2 = requests.get(api_url2)
    api_get_data2 = api_get2.json()
    zipped = zip((api_get_data2["hourly"]["time"]),(api_get_data2["hourly"]["temperature_2m"]),(api_get_data2["hourly"]["apparent_temperature"]),(api_get_data2["hourly"]["precipitation"]),(api_get_data2["hourly"]["windspeed_10m"]),(api_get_data2["hourly"]["relativehumidity_2m"]))
    
    for i in zipped:
        # i[0] must have format like "2022-08-30 15:00:00" not '2022-09-25T00:00'
        time_formatted = f'{i[0][:10]} {i[0][11:16]}:00'
        weather_data2[time_formatted]={"temperature": i[1],
                            "feels_like": i[2],
                            "precipitation": i[3],
                            "wind_speed": i[4],
                            "humidity" : int(i[5]),
        }
        # create avg_data dict for everyday
        day = pd.Timestamp(f'{i[0][:10]}')
        if day.day_name() not in open_meteo_avg.keys():
            open_meteo_avg[day.day_name()] = {"date": f'{i[0][:10]}'}

    # add values to avg dict
    for keys, values in open_meteo_avg.items():
        divider_num =  len([0 for k in weather_data2.keys() if open_meteo_avg[keys]["date"] in k])
        x = sum(weather_data2[k]["temperature"] for k in weather_data2.keys() if open_meteo_avg[keys]["date"] in k)/divider_num
        open_meteo_avg[keys]["avg_temp"] = float("{:.1f}".format(x))


def meteomatics():
    username= "none_ersuk"
    password= "vawNC41R3u"
    api_url3 = f'https://{username}:{password}@api.meteomatics.com/{today[0]}-{today[1]}-{today[2]}T00:00:00Z--{forecast_days[0]}-{forecast_days[1]}-{forecast_days[2]}T00:00:00Z:PT1H/t_2m:C,precip_1h:mm,wind_speed_10m:ms/{coordinates[1]},{coordinates[0]}/json'
    api_get3 = requests.get(api_url3)
    api_get_data3 = api_get3.json()
    tmp_time = [i["date"] for i in api_get_data3["data"][0]["coordinates"][0]["dates"]]
    tmp_temper = [i["value"] for i in api_get_data3["data"][0]["coordinates"][0]["dates"]]
    tmp_precip = [i["value"] for i in api_get_data3["data"][1]["coordinates"][0]["dates"]]
    tmp_win = [i["value"] for i in api_get_data3["data"][2]["coordinates"][0]["dates"]]
    for i in range(len(tmp_time)):
        time_formatted = f'{tmp_time[i][:10]} {tmp_time[i][11:19]}'
        weather_data3[time_formatted]={"temperature": tmp_temper[i],
                            "precipitation": tmp_precip[i],
                            "wind_speed": tmp_win[i],
        }


# TODO create SQL database for temperatures change of earth
# display graphs with those datas

def history_graphs(city, lang):
    searched_city = city 
    language = lang

    #plotly graph


    #define data 
    if openweather(searched_city, language) == "404" or len(weather_data1) == 0 :
        # delete values when there is another search with error
        weather_data1.clear()
        weather_data2.clear()
        weather_data3.clear()
        global coordinates
        coordinates = ["",""]
        first_day_dict.clear()
        open_meteo_avg.clear()
        return '404'
    #openweather(searched_city , language)
    open_meteo()
    meteomatics()
    # return values for html
    return [multi_graph_generator(weather_data1,weather_data2,weather_data3), coordinates, weather_data1 , weather_data2 , weather_data3, searched_city,act_time, first_day_dict, cur_time, open_meteo_avg]

    


def graph_generator(data):

    x_values = list(data.keys())
    y_values = []
    for keys,values in data.items():
        y_values.append(values["temperature"])

    # openweathermaps graph 
    fig = go.Figure()
    # Create and style traces
    fig.add_trace(go.Scatter(x=x_values, y=y_values, 
                         line=dict(color='yellowgreen', width=4)))

    # Edit the layout
    fig.update_layout(title='Weather graph',
                   xaxis_title='Day',
                   yaxis_title='Temperature [°C]',
                    width=1000,
                    height=500,)
    fig.show()
united_dict= {}


def unite_dicts(dict , yvals, xvals, pos):
    """ creates united dictionary with rain data for every datetime"""
    united_dict = dict 
    for k in united_dict.keys():
        if k in xvals:
            ind = xvals.index(k)
            val = yvals[ind]
            if type(val) == float:
                vl = united_dict[k]
                vl[pos] = val 
                d1 = {k : vl}
                united_dict.update(d1)
    return united_dict



def multi_graph_generator(data,data2,data3):
    x_values = list(data.keys())
    x_values2 = list(data2.keys())
    x_values3 = list(data3.keys())
    y_values = []
    for keys,values in data.items():
        y_values.append(values["temperature"])
    y_values2 = []
    for keys,values in data2.items():
        y_values2.append(values["temperature"])
    y_values3 = []
    for keys,values in data3.items():
        y_values3.append(values["temperature"])

    y_valuesp = []
    for keys,values in data.items():
        y_valuesp.append(values["precipitation"])
    y_values2p = []
    for keys,values in data2.items():
        y_values2p.append(values["precipitation"])
    y_values3p = []
    for keys,values in data3.items():
        y_values3p.append(values["precipitation"])

    #create united list of time values
    united_x_vals = sorted(set(x_values + x_values2 + x_values3))

    # create a dict for values of all meteoservices with key as date
    united_dict = { x : [0,0,0] for x in united_x_vals}

    unite_dicts(united_dict , y_valuesp , x_values , 0)
    unite_dicts(united_dict , y_values2p, x_values2 ,1)
    unite_dicts(united_dict , y_values3p, x_values3 ,2)

    
    # openweathermaps graph 
  #  fig = go.Figure()
    fig = make_subplots(rows=3, cols=1, subplot_titles=("Temperature Data", "Precipitation Data"))

    # Create and style traces
    fig.add_trace(go.Scatter(x=x_values, y=y_values, name = "Openweathermaps",
                         line=dict(color=' #ff0f2b   ', width=4)
                         ),
                         row=1, col=1)
    fig.add_trace(go.Scatter(x=x_values2, y=y_values2, name = "Open-meteo",
                         line=dict(color=' #01FF70  ', width=4)
                         ),
                         row=1, col=1)
    fig.add_trace(go.Scatter(x=x_values3, y=y_values3, name = "Meteomatics",
                        line=dict(color='  #FFDC00  ', width=4)
                        ),
                        row=1, col=1)

   # fig.show()
  #  fig.write_html("multi_graphs.html")

    fig.add_trace(go.Bar(x=x_values, y=y_valuesp, name = "Openweathermaps"),
                         row=2, col=1)
    fig.add_trace(go.Bar(x=x_values2, y=y_values2p, name = "Open-meteo",),
                         row=2, col=1) 
    fig.add_trace(go.Bar(x=x_values3, y=y_values3p, name = "Meteomatics",),
                         row=2, col=1) 
   

    df=pd.DataFrame.from_dict(united_dict,orient='index', columns=['Openweathermaps','Open-meteo','Meteomatics']) #.transpose()
    fx = px.bar(df,x=df.index, y=['Openweathermaps','Open-meteo','Meteomatics'] ,title='All in one')
    #fx.show()

  
    # Update xaxis properties
    fig.update_xaxes(title_text="Day", showgrid=False, row=1, col=1)
    fig.update_xaxes(title_text="Day",showgrid=False, row=2, col=1)
    fig.update_yaxes(title_text="Temperature [°C]", showgrid=True,row=1, col=1)
    fig.update_yaxes(title_text="Precipitation [mm]", showgrid=True, row=2, col=1)

    # Edit the layout
    fig.update_layout(title='Weather data comparisson',
                    height=1000,
                    barmode='stack',
                   # showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor=  "rgba(0, 0, 0, 0)"
                    )

    #fig.show()

    #graph with wind data 
    y_valueswind = []
    for keys,values in data.items():
        y_valueswind.append(values["wind_speed"])
    y_valueswind2 = []
    for keys,values in data2.items():
        y_valueswind2.append(values["wind_speed"])
    y_valueswind3 = []
    for keys,values in data3.items():
        y_valueswind3.append(values["wind_speed"])
    # create 3rd graph
    fg3 = go.Figure()
    fg3.add_trace(go.Scatter(x=x_values, y=y_valueswind,
                        mode='lines',
                        name='Openweathermaps'))
    fg3.add_trace(go.Scatter(x=x_values2, y=y_valueswind2,
                        mode='lines+markers',
                        name='Open-meteo'))
    fg3.add_trace(go.Scatter(x=x_values3, y=y_valueswind3,
                        mode='markers', name='Meteomatics'))

    fg3.update_layout(title='Wind data comparisson',
                height=600,
             #   barmode='stack',
                # showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor=  "rgba(0, 0, 0, 0)"
                )
    fg3.update_yaxes(title_text="Wind speed [m/s]")

   # fg3.show()

    #export to html as json
    graphs12 = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)
    graph3 = json.dumps(fg3,cls=plotly.utils.PlotlyJSONEncoder)
    graphs = [graphs12, graph3]
    return graphs


if __name__ == "__main__":
    if city !="":
        city = ""
    history_graphs(city, lang)    