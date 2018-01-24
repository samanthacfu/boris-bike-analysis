#Make static maps!

#Imports
import pandas as pd
from bokeh.io import output_file, output_notebook, show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool, HoverTool
)
from bokeh.models.mappers import CategoricalColorMapper
from bokeh.palettes import brewer
from bokeh.io import curdoc
from bokeh.layouts import column, row, widgetbox

#Gmaps in Bokeh requires a Google API key from https://developers.google.com/maps/documentation/javascript/get-api-key
API_KEY = ""

#Import station data
file = '/Users/samanthafu/stations_clean.csv' 
stations = pd.read_csv(file, skiprows=0)

#Create static map by year added

#Set center of map to central London
map_options = GMapOptions(lat=51.504817, lng=-0.100186, map_type="roadmap", zoom=13)

plot = GMapPlot(
    x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, plot_width=1300, plot_height=700
)

#Format title
plot.title.text = "Stations by Year Added"
plot.title.text_font = "amatic sc"
plot.title.align = "center"
plot.title.offset = -20
plot.title.text_font_size="40px"

#Set api key
plot.api_key = API_KEY

#Create column data source

source = ColumnDataSource(
    data=dict(
        lat=stations.lat.tolist(),
        lon=stations.lon.tolist(),
        size=stations.docks.tolist(),
        color=stations.installed_year.tolist(),
        name=stations.station.tolist()
    )
)

color_mapper = CategoricalColorMapper(factors=[2017,2016,2015,2014,2013,2012,2011,2010], palette=brewer['Blues'][8])
circle = Circle(x="lon", y="lat",size="size",fill_color=dict(field='color',transform=color_mapper), fill_alpha=0.8, line_color=None)
plot.add_glyph(source, circle)

#Add tools
hover= HoverTool(tooltips = [
    ("station","@name"),
    ("docks","@size"),
    ("year added","@color")
])

plot.add_tools(PanTool(), WheelZoomTool(), hover)

output_file("stations_by_year.html")
output_notebook()
show(plot)


