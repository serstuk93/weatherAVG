# WEATHER AVG
#### Video Demo:  <https://youtu.be/uo0FEX8mI-4>
#### Description:
This app is created with FLASK, Boostrap, Python, Javascript, Html, CSS, API + its resposive.
There are 2 basic website htmls, first one is index from where user can search for city and also there is info about project.
Site with result is /temperatures where actual weather info like current temperature, feeling temperature, humidity, user time, wind speed and current weather type like raining, snowing etc is shown.
Weather description of type "mist","smoke","haze","dust","fog","sand","dust","ash","squall","tornado" are described as mist only becouse it would require a lot of background images.
For that reason clear cloud, cloudy, drizzle, mist, rain, snow, thunderstorm are handled only. So background image will change accordingly. Images are stored in static/weather_img folder.
App grabs API data from various weather service providers.
API keys are intentionally left in the code so this program will work when checked by CS50 team.
At top part of page there are shown data fetched from OpenWeatherMaps with changing icons for current state of weather in seleced city.
Icons for upcoming hours forecast are dynamically changing according to provided data.
Background image from that "top-widget" section is variable according to weather.
So city with snow will give another background than city where it is raining right now.
There is script to automatically update time based on user time every 100 miliseconds.
Hourly temperature forecast is showing temperatures for every 3 hours during 24 hours ( including ).
Those hourly forecast data  are from OpenWeatherMaps.
At lower part of website there is "average daily temperature forecast" where averaged weather data from 3 free API providers (Openweathermaps, Open meteo, Meteomatics) are presented.
Those averaged data are shown for upcoming 7 days.
Names of days are handled by function where datetime is transformed into name.
API datas are first processed individually and then merged and shown together in mentioned section.
Website also shows 3 graphs.
Those graphs are handled by function where every graph is of different type. First is created by lines and markers, second by lines and last graph merges bars into stack.  Graphs are created with Plotly library and are imported into HTML via script.
Graphs can be modified by clicking at layout. They are responsive. Some adjustments require refreshing page howerer. For example changing resolution of webpage. Graphs can be zoomed in , zoomed out or saved as png files. Some data can be hidden by clicking at name of source for example at clicking at Meteomatics text field near graph, the data for that API will dissapear.
Graphs are describing Wind, Temperature, Precipitation data.
Errors are handled by redirecting user to another htmls when conditions are not met. There is meme image with short description of problem and button to go back.
For example when user dont write any existing page he is redirected into page where he can see error described and he can return back to fix his mistake.
The similar thing happens for sending empty submit.
Whole project is in metric and Celsius units.
This was CS50x!