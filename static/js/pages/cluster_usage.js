$(document).ready(function () {

    const memoryDiv = document.getElementById('memoryDiv');

    const source = new EventSource("/memory", {withCredentials: true});

    source.onmessage = function (event) {
        
        // Parsing data
        const data = JSON.parse(event.data);
        console.log(data);
        const keys = [];
        for (var k in data)
            keys.push(k);
        
        console.log(keys);

        // Building string
        var textMemory = "";

        function humanFileSize(bytes, si) {
            var thresh = si ? 1000 : 1024;
            if(Math.abs(bytes) < thresh) {
                return bytes + ' B';
            }
            var units = si
                ? ['kB','MB','GB','TB','PB','EB','ZB','YB']
                : ['KiB','MiB','GiB','TiB','PiB','EiB','ZiB','YiB'];
            var u = -1;
            do {
                bytes /= thresh;
                ++u;
            } while(Math.abs(bytes) >= thresh && u < units.length - 1);
            return bytes.toFixed(1)+' '+units[u];
        }        

        // Appending memory
        for (var i = 0; i < keys.length; i++) {
            textMemory += "<p><h5>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i style='color: #0073b7;' class='fa fa-check'></i> ";
            textMemory += keys[i] + ": " + humanFileSize(data[keys[i]], true);
            textMemory += " </h5></p>";
        }

        // Setting text
        memoryDiv.innerHTML = textMemory;
    }
});