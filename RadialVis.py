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
enronData = enronData.sort_values(by=['date'])
enronData['edge_color'] = 'red'
enronData.loc[enronData['sentiment'] >= 0, 'edge_color'] = 'green'

G = nx.Graph()
G = nx.from_pandas_edgelist(enronData, 'fromEmail', 'toEmail', edge_attr=['date', 'sentiment', 'edge_color'],create_using=nx.Graph())

date_range_slider = DateRangeSlider(value=(date(1998, 11, 12), date(2002, 6, 20)), start=date(1998, 11, 12), end=date(2002, 6, 20),step = 1)

uniquely = enronData[['toEmail', 'toJobtitle','toId']].drop_duplicates()

#figure or plot? Only time will tell/stackoverflow
plot = figure(plot_width=600, plot_height=600,
            x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1,1.1))
plot.title.text = "Radial Nodes and Links Graph"

node_hover_tool = HoverTool(
    tooltips=[('Email', '@toEmail'), ('ID', '@toId'), ('Job', '@toJobtitle')])
plot.add_tools(node_hover_tool, TapTool())

plot.xgrid.visible = False
plot.ygrid.visible = False

plot.xaxis.visible = False
plot.yaxis.visible = False

graph_renderer = from_networkx(G, nx.circular_layout, scale=1, center=(0, 0))



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
graph_renderer.node_renderer.data_source.data['toEmail'] = uniquely['toEmail']
graph_renderer.node_renderer.data_source.data['toJobtitle'] = uniquely['toJobtitle']

graph_renderer.edge_renderer.glyph = MultiLine(
    line_color="edge_color", line_alpha=0.8, line_width=1)

plot.renderers.append(graph_renderer)

pd.DataFrame(graph_renderer.edge_renderer.data_source.data)

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
        from_pos = (`${key}`)
break;
}

}
    for (const [key, value] of Object.entries(Datey).reverse()) {
    if (`${value}`<=cb_obj.value[1]){
        to_pos = (`${key}`)
break;
}
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
callback = CustomJS(args=dict(graph_renderer=graph_renderer, source=source, fromE=enronData['fromEmail'], toE=enronData['toEmail'], eDate=enronData['date'], senti=enronData['sentiment'], colors=enronData['edge_color']), code=code)
eDate = enronData['date']

date_range_slider.js_on_change('value', callback)

bokeh_layout = column(plot, date_range_slider)

curdoc().add_root(bokeh_layout)
#output_file("static/radial_nodes"+examplestring+".html", title="Radial Node and Link Visualisation")
#save(bokeh_layout) # Please do not use the show() or save() functions.
#show(bokeh_layout) # Please do not use the show() or save() functions.

if __name__=="__main__": # This only runs when you run RadialVis.py standalone
    radial_process = subprocess.Popen(
    ['python', '-m', 'bokeh', 'serve', '--allow-websocket-origin=127.0.0.1:5000', '--port', '5001', '--allow-websocket-origin=localhost:5001', 'RadialVis.py'], stdout=subprocess.PIPE)

    print("You have 15 seconds to view the visualisation. Please do not ctrl+c")
    time.sleep(15)

    def kill_temp_server():
        print("Automatically killing bokeh server after 15 sec")
        radial_process.kill()
    atexit.register(kill_temp_server)
    
