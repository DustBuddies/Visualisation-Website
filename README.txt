~~ Welcome to Group 10BC's Visualisation Website ~~

Made by Yavuz Bozkurt, Prayag Joy, Stavros Kannavas, Sander van der Leek, Jeffrey Lint, Rik van Noort & Melih Şengül.

~~ How to use: ~~
1.  Unzip the Visualisation-Website.zip file and save it in a known location on your computer.
2.  Inside VSCode open the Visualisation-Website folder and run VisWeb.py with a python interpreter. 
    OR use a terminal to run VisWeb.py with a python interpreter. "python VisWeb.py"
    It is important to make sure the directory path is in the folder Visualisation-Website before running the website. EX: "C:\Users\[username]\Desktop\Visualisation-Website>"
3.  If you are missing a package type in the terminal "pip install [packagename]". Repeat this step multiple times if necessary.
4.  If everything is working you should see in the terminal the following output:
    "" 
    * Serving Flask app 'VisWeb' (lazy loading)
    * Environment: production
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
    * Debug mode: on
    * Restarting with stat
    * Debugger is active!
    * Debugger PIN: 884-726-530
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    ""
5.  Now you can open the website in your browser, paste in the searchbar of your internet browser "http://127.0.0.1:5000/" and hit enter. 


~~ Known Issues ~~

    - The search function is currently not functional. Using the search button instead flashes a message in the browser.
    - The category select function is currently not functional. This also flashes a message in the browser.
    - The slider of the Radial Visualisation is currently broken. 
    - Both Visualisations only create 1 node for each row in the .csv file  
    - In the Radial Visualisation hovering over a node unintentionally shows the email address of another person who sent an email TO that node instead of the email address of the hovered node. 
    - The website Visualisations are only scaled to fit on a widescreen monitor. They do not scale to fit the viewing device.
