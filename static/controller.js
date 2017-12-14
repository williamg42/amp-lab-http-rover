var control_forward = function() {
    var r = new XMLHttpRequest();
    r.open("GET", "/api/control/forward");
    r.send();
    reset_color();
    document.getElementById("forward-button").style.backgroundColor = "lightgray";
};

var control_left = function() {
    var r = new XMLHttpRequest();
    r.open("GET", "/api/control/left");
    r.send();
    reset_color();
    document.getElementById("left-button").style.backgroundColor = "lightgray";
};

var control_right = function() {
    var r = new XMLHttpRequest();
    r.open("GET", "/api/control/right");
    r.send();
    reset_color();
    document.getElementById("right-button").style.backgroundColor = "lightgray";
};

var control_stop = function() {
    var r = new XMLHttpRequest();
    r.open("GET", "/api/control/stop");
    r.send();
    reset_color();
    document.getElementById("stop-button").style.backgroundColor = "lightgray";
};

var reset_color = function() {
    document.getElementById("forward-button").style.backgroundColor = "white";
    document.getElementById("left-button").style.backgroundColor = "white";
    document.getElementById("right-button").style.backgroundColor = "white";
    document.getElementById("stop-button").style.backgroundColor = "white";
};

var forward = false;
var left = false;
var right = false;

document.getElementById("forward-button").onmousedown = function() {
    if (!forward) {
        control_forward();
        forward = true;
    }
};

document.getElementById("left-button").onmousedown = function() {
    if (!left) {
        control_left();
        left = true;
    }
};

document.getElementById("right-button").onmousedown = function() {
    if (!right) {
        control_right();
        right = true;
    }
};

document.onmouseup = function() {
    forward = false;
    left = false;
    right = false;
    stop();
};

document.onkeydown = function(e) {
    if (e.keyCode == '37') {
        // left arrow
        if (!left) {
            control_left();
            left = true;
        }
    }
    else if (e.keyCode == '38') {
        // up arrow
        if (!forward) {
            control_forward();
            forward = true;
        }
    }
    else if (e.keyCode == '39') {
        // right arrow
        if (!right) {
            control_right();
            right = true;
        }
    }
};

document.onkeyup = function(e) {
    if (e.keyCode == '37') {
        // left arrow
        left = false;
    }
    else if (e.keyCode == '38') {
        // up arrow
        forward = false;
    }
    else if (e.keyCode == '39') {
        // right arrow
        right = false;
    }
    if (!left && !forward && !right) {
        stop();
    }
};
