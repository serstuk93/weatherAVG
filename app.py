from crypt import methods
from flask import Flask, render_template, request
import weather

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")



@app.route("/temperatures", methods=["GET","POST"])
def temperature_show():

    if request.method == "POST":
        if not request.form.get("search"):
            return render_template("failure.html")

    city = request.form.get("search")
    lang = "en"

    weather_res = weather.history_graphs(city, lang)
    if weather_res == '404':
        return render_template("notfound.html")
    # create data for html jinja2
    graphs = weather_res[0]
    coords = weather_res[1]
    weather_d1 = weather_res[2]
    weather_d2 = weather_res[3]
    weather_d3 = weather_res[4]
    city_corrected = weather_res[5]
    act_time = list(weather_res[2].keys())[0]
    first_day = weather_res[7]
    cur_time = weather_res[8]
    avg_dict = weather_res[9]
    widg_temp = first_day[act_time]["weather-main"].lower()
    # atm types of misty and similar types of weather in openweathermaps
    # instead of multiple images 1 is used for those conditions
    atmosphere = ["mist","smoke","haze","dust","fog","sand","dust","ash","squall","tornado"]
    # widg_img_name = f"url('/static/weather_img/thunderstorm.jpg')" 
    if widg_temp in atmosphere:
        widg_img_name = f"url('/static/weather_img/mist.jpg')"
    else: 
        widg_img_name = f"url('/static/weather_img/{widg_temp}.jpg')" 
    widg_img_name= ('"' + widg_img_name + '"')

    if request.method == "GET":
        return render_template("index.html")

    return render_template("temperatures.html", graphs12 =graphs[0], graph3 = graphs[1], coords = coords, wd1 = weather_d1, wd2 = weather_d2, wd3 = weather_d3, city_corrected = city_corrected, act_time = act_time, first_day =first_day, cur_time = cur_time ,avg_dict= avg_dict, widg_img_name= widg_img_name)