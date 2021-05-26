import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
import glob
from flask import Flask, flash, render_template, request
from werkzeug.utils import secure_filename
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from bokeh.io import output_file, show, save, output_notebook
from bokeh.layouts import row, column
from bokeh.models import Plot, Range1d, MultiLine, Circle, TapTool, OpenURL, HoverTool, CustomJS, Slider, Column, CustomJS, DateRangeSlider, Dropdown, ColumnDataSource
from bokeh.models import BoxSelectTool, BoxZoomTool, Circle, EdgesAndLinkedNodes, HoverTool, MultiLine, NodesAndLinkedEdges, Plot, Range1d, ResetTool, TapTool
from bokeh.palettes import Spectral4
from bokeh.plotting import figure
from bokeh.models.graphs import from_networkx
from datetime import date
from bokeh.embed import components


#
# BEFORE RUNNING THIS FILE MAKE SURE YOU ARE IN THE FOLDER 'Flask Website'
# 

app = Flask(__name__, template_folder='./templates', static_folder='./static')

@app.route('/')
def homepage():
    return render_template("home.html")

@app.route('/visualisation', methods = ["GET", "POST"])
def vispage():
    if request.method=="POST":
        if 'file' not in request.files: # page shown when a submitted form does not contain any 'file'-named part
            #flash('no file part in the form?')
            return render_template("visualisation.html", message="What happened?")
        
        file = request.files["file"]
        
        if file.filename=='': # page shown when the user did not submit any file at all
            #flash('No file detected')
            return render_template("visualisation.html", message="You have not uploaded anything. >:(")
        if file and allowed_file(file.filename): # page shown when the user successfully uploads a valid file
            #flash('file is now uploaded')
            sec_filename=secure_filename("inputdata.csv") #file.filename
            file.save(os.path.join("uploads", sec_filename))

            os.system("python RadialVis.py") # This .py script generates the visualisation and places radial_nodes_vis.html in the static folder
            inputdata = pd.read_csv("uploads/inputdata.csv")
            uniquejobs=["test1", "test2"]
            uniquejobs = inputdata.toJobtitle.unique()

            return render_template('visualisation.html', message = "Succesfully uploaded a Dataset!", categories=uniquejobs)
        else: # page shown when the user successfully uploads an invalid file
            return render_template("visualisation.html", message="Illegal file type!")
    else:

        #if os.path.exists("static/radial_nodes_vis.html"): # This code below automatically removes the old vis
            #os.remove("static/radial_nodes_vis.html") 
            #flash("deleted static/radial_nodes_vis.html")

        paths=''
        for el in [x for x in Path('.').iterdir() ]: #if x.is_dir()  this is for debugging 
            paths=paths+str(el)+" ||| "

        return render_template('visualisation.html', message = "Please upload a data file.", debug_msg="") #+paths



ALLOWED_EXTENSIONS={'csv'} #, 'png'   ONLY allow csv files or the vis programs will break!
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/about') # about page
def aboutpage():
    return render_template("about.html")





if __name__ == '__main__':
    app.secret_key="secret" # Not sure why this is necessary
    app.run(debug=True)
