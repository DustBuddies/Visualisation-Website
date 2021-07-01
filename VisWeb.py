from bokeh.embed.server import server_document
from flask import Flask, flash, render_template, request
from werkzeug.utils import secure_filename

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

#
# BEFORE RUNNING THIS FILE MAKE SURE YOU ARE IN THE FOLDER 'Visualisation-Website'
# 

app = Flask(__name__, template_folder='./templates', static_folder='./static')

radial_process = subprocess.Popen(['python', '-m', 'bokeh', 'serve', '--allow-websocket-origin=127.0.0.1:5000', '--port', '5001', '--allow-websocket-origin=localhost:5001', 'RadialVis.py'], stdout=subprocess.PIPE)


@atexit.register
def kill_servers():
    radial_process.kill()


@app.route('/')
def homepage():
    return render_template("home.html")

exampledata = pd.read_csv("uploads/inputdata_example.csv")
examplejobs=sorted(np.unique(exampledata[["fromJobtitle", "toJobtitle"]].values))

@app.route('/visualisation', methods = ["GET", "POST"])
def vispage():
    if request.method=="POST":
        if 'file' not in request.files: # page shown when a submitted form does not contain any 'file'-named part, like the 'show default' button
            #flash('no file part in the form?')
            radial_script=server_document(url="http://localhost:5001/RadialVis", arguments={'exampledata':"_example"})
            return render_template("visualisation.html", Radial=radial_script, message="Showing example dataset.", categories=examplejobs) #ForceDir=forcedir_script,
        
        file = request.files["file"]
        
        if file.filename=='': # page shown when the user did not submit any file at all
            #flash('No file detected')
            radial_script=server_document(url="http://localhost:5001/RadialVis", arguments={'exampledata':"_example"})
            return render_template("visualisation.html", Radial=radial_script, message="You have not uploaded anything. :(", categories=examplejobs) 
        if file and allowed_file(file.filename): # page shown when the user successfully uploads a valid file
            #flash('file is now uploaded')
            sec_filename=secure_filename("inputdata.csv") #file.filename
            file.save(os.path.join("uploads", sec_filename))

            radial_script=server_document(url="http://localhost:5001/RadialVis", arguments={'exampledata':""})
            inputdata = pd.read_csv("uploads/inputdata.csv")
            uniquejobs = sorted(np.unique(inputdata[["fromJobtitle", "toJobtitle"]].values))

            return render_template('visualisation.html', Radial=radial_script, message = "Succesfully uploaded a Dataset!", categories=uniquejobs)
        else: # page shown when the user successfully uploads an invalid file

            radial_script=server_document(url="http://localhost:5001/RadialVis", arguments={'exampledata':"_example"})
            return render_template("visualisation.html", Radial=radial_script, message="Wrong file type!", categories=examplejobs)
    else: # page shown when first loading the page

        radial_script=server_document(url="http://localhost:5001/RadialVis", arguments={'exampledata':"_example"})
        return render_template('visualisation.html', Radial=radial_script, message="Please upload a data file.", categories=examplejobs, debug_msg="")



ALLOWED_EXTENSIONS={'csv'} #ONLY allow csv files or the vis programs will break!
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/about') # about page
def aboutpage():
    return render_template("about.html")



if __name__ == '__main__':
    app.secret_key="secret" # Not sure why this is necessary
    app.run(debug=True)
