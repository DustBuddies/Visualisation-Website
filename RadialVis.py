import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx
from bokeh.io import output_file, show, save
from bokeh.layouts import row, column
from bokeh.models import Plot, Range1d, MultiLine, Circle, TapTool, OpenURL, HoverTool, CustomJS, Slider, Column
from bokeh.models import (BoxSelectTool, BoxZoomTool, Circle, EdgesAndLinkedNodes,
                          HoverTool, MultiLine, NodesAndLinkedEdges, Plot, Range1d, ResetTool, TapTool,)
from bokeh.palettes import Spectral4
from bokeh.plotting import figure, from_networkx
from datetime import date
from bokeh.models import CustomJS, DateRangeSlider, Dropdown
from bokeh.models import ColumnDataSource
from bokeh.io import output_notebook
from bokeh.embed import components

import os
import glob

import sys

if (len(sys.argv)==1): # if no extra argument is given then load inputdata.csv. ex: "py RadialVis.py"
    examplestring=""
else:
    examplestring=sys.argv[1] #If another argument is given this will be part of thefilename. ex: "py RadialVis.py _example"

csv_files = glob.glob(os.path.join('uploads', "inputdata"+examplestring+".csv"))
for f in csv_files:
    enronData = pd.read_csv(f)


enronData['date'] = pd.to_datetime(enronData['date']).dt.date
enronData = enronData.sort_values(by=['date'])
enronData['edge_color'] = 'red'
enronData.loc[enronData['sentiment'] >= 0, 'edge_color'] = 'green'

G = nx.Graph()
G = nx.from_pandas_edgelist(enronData, 'fromEmail', 'toEmail', edge_attr=['date', 'sentiment', 'edge_color'],create_using=nx.Graph())

date_range_slider = DateRangeSlider(value=(date(1998, 11, 12), date(2002, 6, 20)), start=date(1998, 11, 12), end=date(2002, 6, 20),step = 1)

uniquely = enronData[['toEmail', 'toJobtitle','toId']].drop_duplicates()

#figure or plot? Only time will tell/stackoverflow
plot = figure(plot_width=500, plot_height=500,
            x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1,1.1))
plot.title.text = "Radial Nodes and Links Graph"

node_hover_tool = HoverTool(
    tooltips=[('Email', '@index'), ('ID', '@toId'), ('Job', '@toJobtitle')])
plot.add_tools(node_hover_tool, TapTool())

graph_renderer = from_networkx(G, nx.circular_layout, scale=1, center=(0, 0))

source = ColumnDataSource(data=enronData)

#node color - none,selected,hover
graph_renderer.node_renderer.glyph = Circle(
    size=10, fill_color=Spectral4[0])
graph_renderer.node_renderer.selection_glyph = Circle(
    size=15, fill_color=Spectral4[2])
graph_renderer.node_renderer.hover_glyph = Circle(
    size=15, fill_color=Spectral4[1])

graph_renderer.edge_renderer.glyph = MultiLine(
    line_color="#CCCCCC", line_alpha=0.8, line_width=5)
graph_renderer.edge_renderer.selection_glyph = MultiLine(
    line_color=Spectral4[2], line_width=5)
graph_renderer.edge_renderer.hover_glyph = MultiLine(
    line_color=Spectral4[1], line_width=5)

graph_renderer.selection_policy = NodesAndLinkedEdges()
#graph_renderer.inspection_policy = NodesAndLinkedEdges()

graph_renderer.node_renderer.data_source.data['toId'] = uniquely['toId']
graph_renderer.node_renderer.data_source.data['toEmail'] = list(G.nodes)
graph_renderer.node_renderer.data_source.data['toJobtitle'] = uniquely['toJobtitle']

graph_renderer.edge_renderer.glyph = MultiLine(
    line_color="edge_color", line_alpha=0.8, line_width=1)

plot.renderers.append(graph_renderer)

#pd.DataFrame(graph_renderer.edge_renderer.data_source.data)

from bokeh.models import Slider

plot.renderers.append(graph_renderer)
source = ColumnDataSource(data={'x': enronData['date']})
code = """ 
    const data = source.data;
    var Datey = eDate.slice();
    var fromEm = fromE.slice();
    var toEm = toE.slice();
    var col = colors.slice();
    var emot = senti.slice();
    var Start = ((new Date(cb_obj.value[0])).toISOString()).substring(0,10);
    var End = ((new Date(cb_obj.value[1])).toISOString()).substring(0,10);
    var from_pos = cb_obj.value[0]
    var to_pos = cb_obj.value[1]

    for (const [key, value] of Object.entries(Datey)) {
    if (`${value}`>=cb_obj.value[0]){
break;
}
from_pos = (`${key}`)
}
    for (const [key, value] of Object.entries(Datey).reverse()) {
    if (`${value}`<=cb_obj.value[1]){
break;
}
to_pos = (`${key}`)
}
console.log(from_pos,to_pos)
    Datey = Datey.slice(from_pos,to_pos) 
    fromEm = fromEm.slice(from_pos,to_pos)
    toEm = toEm.slice(from_pos,to_pos)
    col = col.slice(from_pos,to_pos)
    emot = emot.slice(from_pos,to_pos)
    
    new_data_edge = {'date': Datey, 'start': fromEm,'end':toEm,'sentiment':emot,'edge_color':col};
    graph_renderer.edge_renderer.data_source.data = new_data_edge;  
    console.log(typeOf(new_data_edge))
"""
callback = CustomJS(args=dict(graph_renderer=graph_renderer,
                                source=source,
                                fromE=enronData['fromEmail'],
                                toE=enronData['toEmail'], eDate=enronData['date'], senti=enronData['sentiment'], colors=enronData['edge_color']), code=code)
eDate = enronData['date']

date_range_slider.js_on_change('value', callback)

layout = column(plot, date_range_slider)


output_file("static/radial_nodes"+examplestring+".html",
            title="Radial Node and Link Visualisation")
save(layout)
#show(layout) # keep this commented please :))

