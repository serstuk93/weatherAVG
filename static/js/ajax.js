function current_time(){
    var date = new Date();
    document.getElementById("current_time").innerHTML = date;
}
setInterval(current_time, 100);
