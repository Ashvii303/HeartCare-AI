function predict(){
    var r = Math.random();

    if(r > 0.5){
        document.getElementById("result").innerHTML =
        "⚠️ HIGH RISK";
        document.getElementById("result").style.color = "red";
        document.getElementById("fill").style.width="90%";
        document.getElementById("fill").style.background="red";
    }
    else{
        document.getElementById("result").innerHTML =
        "✅ LOW RISK";
        document.getElementById("result").style.color = "green";
        document.getElementById("fill").style.width="30%";
        document.getElementById("fill").style.background="green";
    }
    function fetchData(){
    fetch('/get_data')
    .then(response => response.json())
    .then(data => {
        document.getElementById("hr").innerText = data.heart_rate;
        document.getElementById("bp").innerText = data.bp;
        document.getElementById("temp").innerText = data.temp;
    });
}

setInterval(fetchData,2000);
}
 