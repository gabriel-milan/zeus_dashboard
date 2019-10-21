$(document).ready(function () {

    const servicesDiv = document.getElementById('servicesDiv');
    const toolsDiv = document.getElementById('toolsDiv');

    const source = new EventSource("/status", {withCredentials: true});

    source.onmessage = function (event) {
        
        // Parsing data
        const data = JSON.parse(event.data);
        const services = data.services;
        const tools = data.tools;
        
        // Building string
        var textServices = "";
        var textTools = "";

        // Appending services
        for (var i = 0; i < services.length; i++) {
            textServices += "<p><h5>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i style='color: #0073b7;' class='fa fa-check'></i> ";
            textServices += services[i];
            textServices += " </h5></p>";
        }

        // Appending tools
        for (var i = 0; i < tools.length; i++) {
            textTools += "<p><h5>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i style='color: #0073b7;' class='fa fa-check'></i> ";
            textTools += tools[i];
            textTools += " </h5></p>";
        }

        // Setting text
        servicesDiv.innerHTML = textServices;
        toolsDiv.innerHTML = textTools;
    }
});