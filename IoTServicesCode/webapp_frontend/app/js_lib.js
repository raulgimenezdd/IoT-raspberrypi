/*
 * Javascript file to implement client side usability for 
 * Operating Systems Desing exercises.
 */
var server_address = "http://35.242.211.241:5000/"



var get_current_sensor_data = function(){
	$.getJSON( server_address+"dso/measurements/", function( data ) {
		for (let i = 0; i < data.length; i++) {
			var fila="<tr><td>"+ data[i].measure_time +"</td><td>"+ data[i].temperature +"</td><td>" + data[i].humidity + "</td></tr>";
			var btn = document.createElement("TR");
   			btn.innerHTML=fila;
    		document.getElementById("content-measurements").appendChild(btn);
		}

	});
}

var get_device_list = function(){
	$.getJSON( server_address+"dso/devices/", function( data ) {
		var fila="<tr><td>"+ data[0].device_id +"</td><td>"+ data[0].status +"</td><td>" + data[0].location + "</td><td>"+ data[0].register_time +"</td><td><button id=\"medida\" type=\"button\" onclick=\"medida();\">Medidas</button></td></tr>";
		var btn = document.createElement("TR");
   		btn.innerHTML=fila;
    	document.getElementById("content-devices").appendChild(btn);
	});
}
var medida = function() {
	document.getElementById("bloque-medidas").style.display = "block";
	document.getElementById("bloque-devices").style.display = "none";
}

var atras = function() {
	document.getElementById("bloque-medidas").style.display = "none";
	document.getElementById("bloque-devices").style.display = "block";
}
get_device_list()
get_current_sensor_data()
//setInterval(get_current_sensor_data,2000)
