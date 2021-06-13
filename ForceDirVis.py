import numpy as np
import pandas as pd
import matplotlib as plt
import networkx as nx
from bokeh.io import output_file, show, save, curdoc
from bokeh.layouts import row, column
from bokeh.models import Plot, Range1d, MultiLine, Circle, TapTool, OpenURL, HoverTool, CustomJS, Slider, Column
from bokeh.models import BoxSelectTool, BoxZoomTool, Circle, EdgesAndLinkedNodes, HoverTool, MultiLine, NodesAndLinkedEdges, Plot, Range1d, ResetTool, TapTool
from bokeh.palettes import Spectral4, Spectral8
from bokeh.plotting import figure
from bokeh.models.graphs import from_networkx
from datetime import date
from bokeh.models import CustomJS, DateRangeSlider, Dropdown, ColumnDataSource
from bokeh.transform import factor_cmap
import os
import glob
import re
import subprocess
import time
import atexit



try: # This mess gets the string of the file suffix: either "" or "_example"
    args = curdoc().session_context.request.arguments
    weirdstring=str(args.get('exampledata')[0])
    cleanstring = ( re.findall("\'(.*?)\'", weirdstring )[0] )
except (ValueError, TypeError, AttributeError):
    cleanstring="_example"


csv_files = glob.glob(os.path.join('uploads', "inputdata"+cleanstring+".csv"))
for f in csv_files:
    enronData = pd.read_csv(f)


enronData['date'] = pd.to_datetime(enronData['date']).dt.date
#enronData = enronData.sort_values(by=['date'])
enronData['edge_color'] = 'red'
enronData.loc[enronData['sentiment'] >= 0, 'edge_color'] = 'green'


G = nx.Graph()
G = nx.from_pandas_edgelist(enronData, 'fromEmail', 'toEmail', edge_attr=['date', 'sentiment','edge_color'],create_using=nx.Graph())


plot = figure(plot_width=700, plot_height=700,
            x_range=Range1d(-2,2), y_range=Range1d(-2,2))
plot.title.text = "Force Directed Graph"


degrees = dict(nx.degree(G))
nx.set_node_attributes(G, name='degree', values=degrees)

number_to_adjust_by = 5
number_to_multiply_by = 0.5
adjusted_node_size = dict([(node, (degree+number_to_adjust_by)*number_to_multiply_by) for node, degree in nx.degree(G)])
nx.set_node_attributes(G, name='adjusted_node_size', values=adjusted_node_size)

size_by_this_attribute = 'adjusted_node_size'

list(G.nodes)

uniquely = enronData[['toEmail','toJobtitle','toId']].drop_duplicates()



unique_list = []
for job in enronData['toJobtitle']:
    if job not in unique_list:
        unique_list.append(job)
        
uniquely['node_color'] = 'black'
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

plot.xgrid.visible = False
plot.ygrid.visible = False

plot.xaxis.visible = False
plot.yaxis.visible = False

# create bokeh graph
#graph_renderer = from_networkx(G, nx.kamada_kawai_layout, scale=1.7, center=(0,0))
graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))

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

from bokeh.io import show
from bokeh.models import CheckboxButtonGroup, CustomJS

LABELS = list(enronData.toJobtitle.unique())
checkbox_button_group = CheckboxButtonGroup(labels=LABELS,active=[])


source = ColumnDataSource(data={'x': enronData})
code = """ 
const data = source.data;
var Datey = eDate.slice();
var fromEm = fromE.slice();
var toEm = toE.slice();
var col = colors.slice();
var emot = senti.slice();
var fromJob = fJob.slice();
var JobIndexes = []
ActiveLab = []


var myArray = this.active;
    var arrayLength = myArray.length;
for (var i = 0; i < arrayLength; i++) {
    ActiveLab.push(label[myArray[i]]);
}

for (const [key, value] of Object.entries(fJob)) {
    for (var i = 0; i < arrayLength; i++) {
    if (`${value}` == ActiveLab[i]){
    JobIndexes.push(`${key}`)
    }
}
  }
  
function maskMe(listed){
var copied = []
lenJob = JobIndexes.length
for (const [key, value] of Object.entries(listed)) {
    for (var i = 0; i < lenJob; i++) {
    if (`${key}` == JobIndexes[i]){
    copied.push(`${value}`)
    }
}
  }
  listed = copied;
  copied = [];
  return listed;
}

Datey = maskMe(Datey);
fromEm = maskMe(fromE);
col = maskMe(col);
emot = maskMe(emot);
toEm = maskMe(toEm);

new_data_edge = {'date': Datey, 'start': fromEm,'sentiment':emot,'edge_color':col,'end':toEm};
graph_renderer.edge_renderer.data_source.data = new_data_edge;  
"""
callback = CustomJS(args = dict(graph_renderer = graph_renderer,
                                source=source,toE = enronData['toEmail'],
                                fromE = enronData['fromEmail'],eDate = enronData['date'],senti = enronData['sentiment'],colors = enronData['edge_color'],fJob = enronData['fromJobtitle'],label = LABELS),code=code)



checkbox_button_group.js_on_change("active", callback)

bokeh_layout = column(checkbox_button_group,plot)

curdoc().add_root(bokeh_layout)
#output_file("static/force_dir"+examplestring+".html", title="Force Directed Graph")
#save(bokeh_layout) # Please do not use the show() or save() functions.
#show(bokeh_layout) # Please do not use the show() or save() functions.


if __name__=="__main__": # This only runs when you run ForceDirVis.py standalone
    forcedir_process = subprocess.Popen(
    ['python', '-m', 'bokeh', 'serve', '--allow-websocket-origin=127.0.0.1:5000', '--port', '5002', '--allow-websocket-origin=localhost:5002', 'ForceDirVis.py'], stdout=subprocess.PIPE)
    
    print("You have 15 seconds to view the visualisation. Please do not ctrl+c")
    time.sleep(15)

    def kill_temp_server():
        print("Automatically killing bokeh server")
        forcedir_process.kill()
    atexit.register(kill_temp_server)
