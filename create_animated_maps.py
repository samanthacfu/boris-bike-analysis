#Create animated maps!!
	#Resources
	#https://rebeccabilbro.github.io/interactive-viz-bokeh/
	#http://www.bigendiandata.com/2017-06-27-Mapping_in_Jupyter/
	#https://automating-gis-processes.github.io/2016/Lesson5-interactive-map-bokeh.html
	#https://data-dive.com/cologne-bike-rentals-interactive-map-bokeh-dynamic-choropleth 

#Hourly map of average daily rentals and returns

import pandas as pd

file = '/Users/samanthafu/input_hourly_fixed.csv' 
df = pd.read_csv(file, skiprows=0)

from bokeh.io import output_file, output_notebook, show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, LogColorMapper, BasicTicker, ColorBar,
    DataRange1d, PanTool, WheelZoomTool, BoxSelectTool, CustomJS, Slider, Toggle, Range1d, HoverTool, Text
)
from bokeh.models.mappers import ColorMapper, LinearColorMapper, CategoricalColorMapper
from bokeh.palettes import Viridis
from bokeh.layouts import column, row, widgetbox

map_options = GMapOptions(lat=51.504817, lng=-0.100186, map_type="roadmap", zoom=13)

plot = GMapPlot(
    x_range=Range1d(), y_range=Range1d(), map_options=map_options, plot_width=1300, plot_height=700
)
#plot.title.text = "Hourly Usage"
plot.title.text_font = "amatic sc"
plot.title.align = "center"
plot.title.text_font_size="40px"

plot.api_key = "AIzaSyDwcFI-fWLlqaLLm-vVomzJTzHej9QeW8Q"

sources = {}

for x in range(0, 24):
    newdf = df[df['hour']==x]
    sources['_{0}'.format(x)] = ColumnDataSource(
        data=dict(
            lat=newdf.lat.tolist(),
            lon=newdf.lon.tolist(),
            size_start=newdf.start_counts_daily.tolist(),
            size_end=newdf.end_counts_daily.tolist(),
            rate=newdf.hour.tolist(),
            name=newdf.station_name.tolist()
            
        )
    )

circle_start = Circle(x="lon", y="lat", size="size_start", fill_color='red', fill_alpha=0.8, line_color=None)
circle_end = Circle(x="lon", y="lat", size="size_end", fill_color='blue', fill_alpha=0.8, line_color=None)
                      
plot.add_glyph(sources['_0'], circle_start)
plot.add_glyph(sources['_0'], circle_end)

#Add tools

hover= HoverTool(tooltips = [
    ("station","@name"),
    ("starting journeys","@size_start"),
    ("ending journeys","@size_end")
])

plot.add_tools(PanTool(), WheelZoomTool(),hover)

#Create dict of sources

dictionary_of_sources = dict(zip([x for x in range(0,24)], ['_%s' % x for x in range(0,24)]))
js_source_array = str(dictionary_of_sources).replace("'", "")

#Add slider with callback to update data source

renderer_source = sources['_0']
code = """
    var year = cb_obj.value,
        sources = %s;
    var new_source_data = sources[year].data
    renderer_source.data = new_source_data;
""" % js_source_array

callback = CustomJS(args=sources, code=code)
slider = Slider(start=0, end=23, value=0, step=1, title="Time of Day",  callback=callback)

callback.args["renderer_source"] = renderer_source

callbackAnime = CustomJS(args=sources, code="""
        var f = cb_obj.active;
        var j = 0;

        if(f == true){
            var mytimer = setInterval(replace_data, 500);             
        } else {
            clearInterval(mytimer);
        }

        var sources = %s
        function replace_data() {
             j++;
             if(sources[j] === undefined) {
                 j=0;
             }
            
            plot.title.text = "Time of Day: " + j + ":00";
            new_source_data = sources[j].data;
            renderer_source.data = new_source_data;
        }
        """ % js_source_array)

callbackAnime.args["renderer_source"] = renderer_source
callbackAnime.args["plot"] = plot

btn = Toggle(label="Play/Stop Animation", button_type="success",
              active=False, callback=callbackAnime)

show(column(widgetbox(btn,slider),plot))

#show(column(widgetbox(slider),plot))

output_file("hourly.html")


#from bokeh.io import curdoc
#curdoc().clear()

#Map of yearly growth in stations

file = '/Users/samanthafu/stations.csv' 
df1 = pd.read_csv(file, skiprows=0)

from bokeh.io import output_file, output_notebook, show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, LogColorMapper, BasicTicker, ColorBar,
    DataRange1d, PanTool, WheelZoomTool, BoxSelectTool, CustomJS, Slider, Toggle, Range1d, HoverTool, Text
)
from bokeh.models.mappers import ColorMapper, LinearColorMapper, CategoricalColorMapper
from bokeh.palettes import Viridis
from bokeh.layouts import column, row, widgetbox

map_options = GMapOptions(lat=51.504817, lng=-0.100186, map_type="roadmap", zoom=13)

plot = GMapPlot(
    x_range=Range1d(), y_range=Range1d(), map_options=map_options, plot_width=1300, plot_height=700
)
plot.title.text = "Stations by Year Installed"
plot.title.text_font = "amatic sc"
plot.title.align = "center"
plot.title.text_font_size="40px"

plot.api_key = "AIzaSyDwcFI-fWLlqaLLm-vVomzJTzHej9QeW8Q"

sources = {}

for x in range(2010, 2018):
    newdf = df1[df1['year']==x]
    sources['_{0}'.format(x)] = ColumnDataSource(
        data=dict(
            lat=newdf.lat.tolist(),
            lon=newdf.lon.tolist(),
            size=newdf.docks.tolist(),
            rate=newdf.year.tolist(),
            name=newdf.commonName.tolist()
            
        )
    )

color_mapper = CategoricalColorMapper(factors=[2017,2016,2015,2014,2013,2012,2011,2010], palette=['#08306b','#08519c','#2171b5','#4292c6','#6baed6','#9ecae1','#c6dbef','#deebf7'])
circle = Circle(x="lon", y="lat", size="size", fill_color=dict(field='rate',transform=color_mapper), fill_alpha=0.8, line_color=None)
                      
plot.add_glyph(sources['_2010'], circle)

#Add tools

hover= HoverTool(tooltips = [
    ("station","@name"),
    ("docks","@size"),
    ("year installed","@rate")
])

plot.add_tools(PanTool(), WheelZoomTool(),hover)

#Create dict of sources

dictionary_of_sources = dict(zip([x for x in range(2010,2018)], ['_%s' % x for x in range(2010,2018)]))
js_source_array = str(dictionary_of_sources).replace("'", "")

#Add slider with callback to update data source

renderer_source = sources['_2010']
code = """
    var year = cb_obj.value,
        sources = %s;
    var new_source_data = sources[year].data
    renderer_source.data = new_source_data;
""" % js_source_array

callback = CustomJS(args=sources, code=code)
slider = Slider(start=2010, end=2017, value=0, step=1, title="Year Installed",  callback=callback)

callback.args["renderer_source"] = renderer_source

show(column(widgetbox(slider),plot))

output_file("stations_slider.html")

