
window.onload=function() {
    //alert("scripts are loading");


    

    var categories = document.getElementsByTagName("c");

    for (var i = 0; i < categories.length; i++) { //prepares all category buttons for later use
        categories[i].id="category_"+i;
        categories[i].className="catoption";
        categories[i].addEventListener('click', function() {HighlightCategory(this)});
    }
    

    document.addEventListener("fullscreenchange", function() { // Handles the user leaving fullscreen, but NOT using the provided button
        //alert(document.fullscreenElement.id);
        if (!document.fullscreenElement) {
            OpenFullscreen(-1);
        }
    });

    //alert("scripts are loaded");
};

/*
document.onkeydown=function(event) {
    alert("keypress: "+event.key);
    if (event.key=="Escape") {
        
    }
};
*/

function HighlightCategory(catelement) { // toggles highlight of the category buttons when pressed 
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
    
    if (document.fullscreenElement || visbox==-1) { // this runs if you leave fullscreen

        document.exitFullscreen();

        var fullscreenvisframes=document.getElementsByClassName("visframe fullscreen");
        for (var i=0; i<fullscreenvisframes.length; i++) {
            fullscreenvisframes[i].classList.remove("fullscreen");
        }

    } else { // this runs when you go to fullscreen

        var visbox_=document.getElementById("visbox_"+visbox);
        visbox_.requestFullscreen();

        var visframes=document.getElementsByClassName("visframe");
        for (var j=0; j<visframes.length; j++) {

            visframes[j].classList.add("fullscreen");
        }

    } 
}

function selectVis(visbox, vischoice) { // 
    var vis=document.getElementById("visbox_"+visbox);
    if (vischoice==0) {
        //vis.style.display="none"; //
    } else {
        vis.style.display="inline-block";
    }

    var options=document.getElementsByClassName("visoption");
    for (var i=0; i<options.length ; i++) {
        if (options[i].id.includes("choice_"+visbox)){
            if (options[i].id == "choice_" + visbox + "_" + vischoice) {
            options[i].classList.add("visselected");
            } else {
            options[i].classList.remove("visselected");
            }
        }
        
    }
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
}


function searchNode(searchboxnum) {
    alert("searchbox: "+searchboxnum+" (does not work yet)");
    var searchbox=document.getElementById("search_"+searchboxnum);
    //window.location="website.php?search=searchbox.value";
    //alert("search node(s) with name: "+searchbox.value+" (not functional)");
}

// settings popup
function OpenSettings() {
    //alert("test123");
    document.getElementById("set_popup").style.display = "block";
};

function CloseSettings() {
    //alert("test456");
    document.getElementById("set_popup").style.display="none";
};

window.onclick=function(event) {
    if (event.target == document.getElementById("set_popup")) {
        CloseSettings();
    }
};
