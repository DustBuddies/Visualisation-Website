import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as plt
import networkx as nx
from bokeh.io import output_file, show, save
from bokeh.layouts import row, column
from bokeh.models import Plot, Range1d, MultiLine, Circle, TapTool, OpenURL, HoverTool, CustomJS, Slider, Column
from bokeh.models import (BoxSelectTool, BoxZoomTool, Circle, EdgesAndLinkedNodes, HoverTool, MultiLine, NodesAndLinkedEdges, Plot, Range1d, ResetTool, TapTool,)
from bokeh.palettes import Spectral4, Spectral8
from bokeh.plotting import figure
from bokeh.plotting import from_networkx
from datetime import date
from bokeh.models import CustomJS, DateRangeSlider,Dropdown
from bokeh.models import ColumnDataSource
from bokeh.io import output_notebook
from bokeh.embed import components
from bokeh.transform import factor_cmap

import os
import glob



csv_files = glob.glob(os.path.join('uploads', "inputdata.csv"))
for f in csv_files:
    enronData = pd.read_csv(f)

enronData['date'] = pd.to_datetime(enronData['date']).dt.date
#enronData = enronData.sort_values(by=['date'])
enronData['edge_color'] = 'red'
enronData.loc[enronData['sentiment'] >= 0, 'edge_color'] = 'green'

G = nx.karate_club_graph()
G = nx.from_pandas_edgelist(enronData, 'fromEmail', 'toEmail', edge_attr=['date', 'sentiment','edge_color'],create_using=nx.Graph())


plot = figure(plot_width=500, plot_height=500,
            x_range=Range1d(-1.1,1.1), y_range=Range1d(-1.1,1.1))
plot.title.text = "Force Directed Graph"


degrees = dict(nx.degree(G))
nx.set_node_attributes(G, name='degree', values=degrees)

number_to_adjust_by = 5
adjusted_node_size = dict([(node, degree+number_to_adjust_by) for node, degree in nx.degree(G)])
nx.set_node_attributes(G, name='adjusted_node_size', values=adjusted_node_size)

size_by_this_attribute = 'adjusted_node_size'

#node_positions = {node[0]: (node[1]['X'], -node[1]['Y']) for node in G.nodes(data=True)} # This code seems to be broken, but I'm not sure what is is even supposed to do?
#pos=dict(list(node_positions.items())[0:5])
#nx.draw_networkx_nodes(G, pos, node_size=size_by_this_attribute)

list(G.nodes)
enronData
uniquely = enronData[['toEmail','toJobtitle','toId']].drop_duplicates()
uniquely


unique_list = []
for job in enronData['toJobtitle']:
    if job not in unique_list:
        unique_list.append(job)
        
uniquely['node_color'] = 'white'
uniquely.loc[uniquely['toJobtitle'] == 'Unknown', 'node_color'] = 'yellow'
uniquely.loc[uniquely['toJobtitle'] == 'Trader', 'node_color'] = 'orange'
uniquely.loc[uniquely['toJobtitle'] == 'Vice President', 'node_color'] = 'purple'
uniquely.loc[uniquely['toJobtitle'] == 'Employee', 'node_color'] = 'springgreen'
uniquely.loc[uniquely['toJobtitle'] == 'Managing Director', 'node_color'] = 'silver'
uniquely.loc[uniquely['toJobtitle'] == 'Manager', 'node_color'] = 'palegoldenrod'
uniquely.loc[uniquely['toJobtitle'] == 'President', 'node_color'] = 'pink'
uniquely.loc[uniquely['toJobtitle'] == 'Director', 'node_color'] = 'cornflowerblue'
uniquely.loc[uniquely['toJobtitle'] == 'CEO', 'node_color'] = 'crimson'

#uniquely['toJobtitle'] = pd.Categorical(uniquely['toJobtitle'])
#uniquely['toJobtitle'].cat.codes

#cmap = plt.colors.ListedColormap(['yellow', 'orange', 'purple', 'springgreen', 'silver', 'palegoldenrod', 'pink', 'cornflowerblue', 'crimson'])
    
#nx.draw(G, node_color=uniquely['toJobtitle'].cat.codes, cmap=cmap)
    
node_hover_tool = HoverTool(tooltips=[('Email', '@toEmail'), ('ID', '@toId'), ('Job', '@toJobtitle')])
plot.add_tools(node_hover_tool, TapTool())

#plot.xgrid.visible = False
#plot.ygrid.visible = False

#plot.xaxis.visible = False
#plot.yaxis.visible = False

# create bokeh graph
graph_renderer = from_networkx(G, nx.spring_layout, scale=10, center=(0,0))

source = ColumnDataSource(data=enronData)

graph_renderer.node_renderer.data_source.add(uniquely['node_color'], 'color')
graph_renderer.node_renderer.glyph = Circle(size=size_by_this_attribute, fill_color="color")
graph_renderer.node_renderer.selection_glyph = Circle(size=15, fill_color=Spectral4[2])
graph_renderer.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])

graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=5)
graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=5)
graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=5)

graph_renderer.selection_policy = NodesAndLinkedEdges()
#graph_renderer.inspection_policy = NodesAndLinkedEdges()

graph_renderer.node_renderer.data_source.data['toId'] = uniquely['toId']
graph_renderer.node_renderer.data_source.data['toEmail'] = uniquely['toEmail']
graph_renderer.node_renderer.data_source.data['toJobtitle'] = uniquely['toJobtitle']

graph_renderer.edge_renderer.glyph = MultiLine(line_color="edge_color", line_alpha=0.8, line_width=1)

plot.renderers.append(graph_renderer)

unique_list

layout = column(plot)
output_file("static/force_dir.html",
            title="Force Directed Graph")
save(layout)
#show(layout)