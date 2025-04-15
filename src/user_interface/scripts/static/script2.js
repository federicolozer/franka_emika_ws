function interface() {
    $.ajax({
        url: '/getJson',
        type: 'GET',
        contentType: 'application/json',
        success: function(data) {
            const json = data;

            let count = 1;
            for (var key in json) {
                createSection(json[key], count++);
            }
        },
        error: function() {
            document.getElementById("msg").innerHTML = "Error: failed to load data";
        }
    });
}



function createSection(val, count) {
    if (val.substr(0,4) == "test" || val == "quit") {
        const button = document.createElement("button");
        button.innerHTML = val;
        button.id = "bt_" + count;

        defineButtonBehavior(button, val);
        document.getElementById("tests").appendChild(button);
        button.className = "traj"
    }
}



function defineButtonBehavior(button, val) {
    button.addEventListener("click", function() {executeTrajectory(val)});
}



function restoreMsg() {
    window.setTimeout(function() {document.getElementById('msg').innerHTML = '...';}, 3000);
}



function executeTrajectory(val) {
    document.getElementById('msg').innerHTML = "Executing trajectory...";
    
    $.ajax({
        url: '/sendExecuteTrajectoryRequest',
        type: 'SEND',
        contentType: 'application/json',
        data: JSON.stringify(val),
        success: function(response) {
            if (response.result == 1) {
                document.getElementById('msg').innerHTML = "Trajectory executed correctly";
            }
            else if (response.result == 0) {
                document.getElementById('msg').innerHTML = "No trajectory found";
            }
            else {
                document.getElementById('msg').innerHTML = "Error: failed to execute trajectory";
            }
            restoreMsg();
        },
        error: function() {
            document.getElementById('msg').innerHTML = "Error: failed to send request";
            restoreMsg();
        }
    });
}
