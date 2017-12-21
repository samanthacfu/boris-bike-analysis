#Make static maps!

import pandas as pd

file = '/Users/samanthafu/stations_clean.csv' 
stations = pd.read_csv(file, skiprows=0)

#MAP BY BOROUGH
from bokeh.io import output_file, output_notebook, show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, LogColorMapper, BasicTicker, ColorBar,
    DataRange1d, PanTool, WheelZoomTool, BoxSelectTool, HoverTool, LabelSet
)
from bokeh.models.mappers import ColorMapper, LinearColorMapper, CategoricalColorMapper
from bokeh.palettes import brewer

map_options = GMapOptions(lat=51.504817, lng=-0.100186, map_type="roadmap", zoom=13)

plot = GMapPlot(
    x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, plot_width=1300, plot_height=800
)
plot.title.text = "Stations by Borough"
plot.title.text_font = "amatic sc"
plot.title.align = "center"
plot.title.text_font_size="40px"

plot.api_key = "AIzaSyDwcFI-fWLlqaLLm-vVomzJTzHej9QeW8Q"

source = ColumnDataSource(
    data=dict(
        lat=stations.lat.tolist(),
        lon=stations.lon.tolist(),
        size=stations.docks.tolist(),
        color=stations.borough.tolist(), 
        name=stations.station.tolist()
    )
)


#labels = LabelSet(x='lon', y='lat', text='station', level='glyph', x_offset=5, y_offset=5, source=source, render_mode='canvas')

color_mapper = CategoricalColorMapper(factors=['City of London','Islington','Camden','Westminster','Kensington and Chelsea','Hackney','Wandsworth','Lambeth','Southwark','Tower Hamlets','Hammersmith and Fulham'], palette=brewer['Set3'][11])
circle = Circle(x="lon", y="lat", size="size", fill_color=dict(field='color',transform=color_mapper), fill_alpha=0.8, line_color=None)
plot.add_glyph(source, circle)

hover= HoverTool(tooltips = [
    ("station","@name"),
    ("docks","@size")
])

#plot.add_layout(labels)
plot.add_tools(PanTool(), WheelZoomTool(), hover)

#output_file("stations_by_borough.html")
#output_notebook()
show(plot)

#MAP BY YEAR ADDED
from bokeh.io import output_file, output_notebook, show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, LogColorMapper, BasicTicker, ColorBar,
    DataRange1d, PanTool, WheelZoomTool, BoxSelectTool, HoverTool, Text
)
from bokeh.models.mappers import ColorMapper, LinearColorMapper, CategoricalColorMapper
from bokeh.palettes import brewer, Viridis
from bokeh.layouts import column, row, widgetbox

map_options = GMapOptions(lat=51.504817, lng=-0.100186, map_type="roadmap", zoom=13)

plot = GMapPlot(
    x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, plot_width=1300, plot_height=700
)

plot.title.text = "Stations by Year Added"
plot.title.text_font = "amatic sc"
plot.title.align = "center"
plot.title.offset = -20
plot.title.text_font_size="40px"

plot.api_key = "AIzaSyDwcFI-fWLlqaLLm-vVomzJTzHej9QeW8Q"

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

hover= HoverTool(tooltips = [
    ("station","@name"),
    ("docks","@size"),
    ("year added","@color")
])

plot.add_tools(PanTool(), WheelZoomTool(), hover)

output_file("stations_by_year.html")
output_notebook()
show(plot)


