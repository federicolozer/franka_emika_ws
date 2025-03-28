function interface() {
    $.ajax({
        url: '/getJson',
        type: 'GET',
        contentType: 'application/json',
        success: function(data) {
            const json = data;

            let count = 1;
            for (var key in json) {
                createSection(key, json[key], count++);
            }
        },
        error: function() {
            document.getElementById("msg").innerHTML = "Error: failed to load data";
        }
    });
}



function createSection(key, val, count) {
    const div = document.createElement("div");
    div.id = "d_" + count;
    const p1 = document.createElement("p");
    p1.innerHTML = key;
    const p2 = document.createElement("p");
    p2.innerHTML = val;
    const button = document.createElement("button");
    button.value = "Add";
    button.innerHTML = button.value;
    button.id = "bt_" + count;
    defineButtonBehavior(button, val, count);

    document.getElementById("inst").appendChild(div);
    document.getElementById("d_" + count).appendChild(p1);
    document.getElementById("d_" + count).appendChild(p2);
    document.getElementById("d_" + count).appendChild(button);

    div.className = "data"
    p1.className = "ndata"
    p2.className = "dataname"
}



function defineButtonBehavior(button, val, count) {
    button.addEventListener("click", function() {
        if (button.value == "Add") {
            data_set.add(val);
            button.value = "Remove";
            button.innerHTML = button.value;
            document.getElementById("d_" + count).setAttribute('style', 'background-color: rgb(86, 180, 86);');
        }
        else if (button.value == "Remove") {
            data_set.delete(val);
            button.value = "Add";
            button.innerHTML = button.value;
            document.getElementById("d_" + count).setAttribute('style', '');
        }
    });
}



function changeAll() {
    button = document.getElementById("chall");
    if (button.value == "Add") {
        button.value = "Remove";
        button.innerHTML = button.value;
        divs = document.getElementsByClassName("data");
        for (let i=0; i<divs.length; i++) {
            data_set.add(divs[i].children[1].innerHTML);
            divs[i].children[2].value = "Remove";
            divs[i].children[2].innerHTML = button.value;
            divs[i].setAttribute('style', 'background-color: rgb(86, 180, 86);');
        }
    }
    else if (button.value == "Remove") {
        button.value = "Add";
        button.innerHTML = button.value;
        divs = document.getElementsByClassName("data");
        for (let i=0; i<divs.length; i++) {
            data_set.delete(divs[i].children[1].innerHTML);
            divs[i].children[2].value = "Add";
            divs[i].children[2].innerHTML = button.value;
            divs[i].setAttribute('style', '');
        }
    }
}



function restoreMsg() {
    window.setTimeout(function() {document.getElementById('msg').innerHTML = '...';}, 3000);
}



function createDataset() {
    document.getElementById('msg').innerHTML = "Creating dataset...";
    
    $.ajax({
        url: '/sendDatasetCreatorRequest',
        type: 'SEND',
        contentType: 'application/json',
        data: JSON.stringify(Array.from(data_set)),
        success: function(response) {
            if (response.result == 0) {
                document.getElementById('msg').innerHTML = "Dataset created correctly";
            }
            else {
                document.getElementById('msg').innerHTML = "Error: failed to create dataset";
            }
            restoreMsg();
        },
        error: function() {
            document.getElementById('msg').innerHTML = "Error: failed to send request";
            restoreMsg();
        }
    });
}



function createTest() {
    document.getElementById('msg').innerHTML = "Creating test...";
    
    $.ajax({
        url: '/sendTestCreatorRequest',
        type: 'SEND',
        contentType: 'application/json',
        data: JSON.stringify(Array.from(data_set)),
        success: function(response) {
            if (response.result == 0) {
                document.getElementById('msg').innerHTML = "Test created correctly";
            }
            else {
                document.getElementById('msg').innerHTML = "Error: failed to create test";
            }
            restoreMsg();
        },
        error: function() {
            document.getElementById('msg').innerHTML = "Error: failed to send request";
            restoreMsg();
        }
    });
}



function trainNN() {
    document.getElementById('msg').innerHTML = "Training neural network...";

    $.ajax({
        url: '/sendTrainingNNRequest',
        type: 'SEND',
        contentType: 'application/json',
        data: JSON.stringify({"value": 1}),
        success: function(response) {
            if (response.result == 0) {
                document.getElementById('msg').innerHTML = "Neural network training has ended correctly";
            }
            else {
                document.getElementById('msg').innerHTML = "Error: failed to train neural network";
            }
            restoreMsg();
        },
        error: function() {
            document.getElementById('msg').innerHTML = "Error: failed to send request";
            restoreMsg();
        }
    });
}