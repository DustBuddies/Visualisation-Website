
window.onload=function() {
    //alert("scripts are loading");

    var categories = document.getElementsByTagName("c");

    for (var i = 0; i < categories.length; i++) { //prepares all category buttons for later use
        categories[i].id="category_"+i;
        categories[i].className="catoption";
        categories[i].addEventListener('click', function() {HighlightCategory(this)});
    }
    
};


document.onkeydown=function(event) { // This allows the user to interact with their keyboard
    //alert("keypress: "+event.key);
    switch(event.key) {
        case "Escape":
            OpenFullscreen(-1);
            break;
        case "1":
            selectVis(1,0);
            break;
        case "2":
            selectVis(1,1);
            break;
        case "3":
            selectVis(1,2);
            break;
        //case "4":
            selectVis(2,0);
            break;
        //case "5":
            selectVis(2,1);
            break;
        //case "6":
            selectVis(2,2);
            break;
    }
};


function HighlightCategory(catelement) { // NOT USED toggles highlight of the category buttons when pressed 
    var catclass=catelement.className;
    //alert("id: "+catelement.id+" class: "+catclass+" content: "+catelement.textContent);

    if (catclass=="catoption") {
        catelement.className="catselected";
        
        alert("highlight all "+catelement.textContent+" (not functional)");
    } else {
        catelement.className="catoption";
        alert("un-highlight all "+catelement.textContent+" (not functional)");
    }

}



function OpenFullscreen(visbox) { // This function makes the fullscreen buttons work
    var fullvisbox = document.getElementsByClassName("visbox fullscreen");
    if (fullvisbox.length>0 || visbox==-1) { // Triggers if the website is already showing a vis fullscreen
        fullvisbox[0].classList.remove("fullscreen");
    } else { 
        var visboxes = document.getElementsByClassName("visbox");
        for (var k=0; k<visboxes.length; k++) {
            if (visboxes[k].id=="visbox_"+visbox) {
                visboxes[k].classList.add("fullscreen");
            }
        }        
    }

}

function selectVis(visbox, vischoice) { // Shows the selected visualisation
    
    // This code fragment colors the dropdown buttons
    var options=document.getElementsByClassName("visoption");
    for (var i=0; i<options.length ; i++) {
        if (options[i].id.includes("choice_"+visbox)){ // Only affects the buttons of 1 box not both 
            if (options[i].id == "choice_" + visbox + "_" + vischoice) { 
            options[i].classList.add("visselected"); // Colors the selected button
            } else {
            options[i].classList.remove("visselected"); // Removes colors from all unselected buttons
            }
        }
    }

    // This code fragment makes the selected visualisation visible (they are invisible by default)
    var visframes=document.getElementsByClassName("visframe");
    for (var j = 0; j < visframes.length; j++) {
        if (visframes[j].id.includes("visualisation_" + visbox)) {
            if (visframes[j].id == "visualisation_" + visbox + "_" + vischoice) {
                visframes[j].classList.add("visible")
            } else {
                visframes[j].classList.remove("visible");
            } 
        }   
    }
    
    // This code fragment can hide the entire visbox
    var vis = document.getElementById("visbox_" + visbox);
    if (vischoice == 0) { // Triggers if the '-Remove Visualisation-' button is pressed
        vis.classList.add("vishidden"); // this class gives attribute: 'visiblity: hidden', the visbox will still occupy space on the website

        if (document.getElementsByClassName("visbox fullscreen").length>0) {
            OpenFullscreen(-1); // If the user was viewing in fullscreen, exit fullscreen
        }
    } else {
        vis.classList.remove("vishidden"); // The visbox will become visible by default (if it wasn't already)
    }
}


function searchNode(searchboxnum) { // NOT USED
    alert("searchbox: "+searchboxnum+" (does not work yet)");
    var searchbox=document.getElementById("search_"+searchboxnum);
    //window.location="website.php?search=searchbox.value";
    //alert("search node(s) with name: "+searchbox.value+" (not functional)");
}


function OpenSettings() { // NOT USED settings popup
    //alert("test123");
    document.getElementById("set_popup").style.display = "block";
};

function CloseSettings() { // NOT USED
    //alert("test456");
    document.getElementById("set_popup").style.display="none";
};

window.onclick = function (event) { // NOT USED
    if (event.target == document.getElementById("set_popup")) {
        CloseSettings();
    }
};
