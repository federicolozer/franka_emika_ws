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
    

    if (val.substr(0,4) == "test") {
        defineButtonBehavior(button, "test", val, count);
        document.getElementById("tests").appendChild(div);
        div.className = "tests"
    }
    else {
        defineButtonBehavior(button, "dataset", val, count);
        document.getElementById("dataset").appendChild(div);
        div.className = "dataset"
    }
    document.getElementById("d_" + count).appendChild(p1);
    document.getElementById("d_" + count).appendChild(p2);
    document.getElementById("d_" + count).appendChild(button);

    p1.className = "ndata"
    p2.className = "dataname"
}



function defineButtonBehavior(button, type, val, count) {
    button.addEventListener("click", function() {
        if (type == "dataset") {
            if (button.value == "Add") {
                dataset_list.add(val);
                button.value = "Remove";
                button.innerHTML = button.value;
                document.getElementById("d_" + count).setAttribute('style', 'background-color: rgb(86, 180, 86);');
            }
            else if (button.value == "Remove") {
                dataset_list.delete(val);
                button.value = "Add";
                button.innerHTML = button.value;
                document.getElementById("d_" + count).setAttribute('style', '');
            }
        }
        else if (type == "test") {
            if (button.value == "Add") {
                tests_list.add(val);
                button.value = "Remove";
                button.innerHTML = button.value;
                
                document.getElementById("d_" + count).setAttribute('style', 'background-color: rgb(86, 180, 86);');
            }
            else if (button.value == "Remove") {
                tests_list.delete(val);
                button.value = "Add";
                button.innerHTML = button.value;
                document.getElementById("d_" + count).setAttribute('style', '');
            }
        }
    });
}



function changeAll(type) {
    if (type == "dataset") {
        button = document.getElementById("challd");
        if (button.value == "Add") {
            button.value = "Remove";
            button.innerHTML = button.value;
            divs = document.getElementsByClassName("dataset");
            for (let i=0; i<divs.length; i++) {
                dataset_list.add(divs[i].children[1].innerHTML);
                divs[i].children[2].value = "Remove";
                divs[i].children[2].innerHTML = button.value;
                divs[i].setAttribute('style', 'background-color: rgb(86, 180, 86);');
            }
        }
        else if (button.value == "Remove") {
            button.value = "Add";
            button.innerHTML = button.value;
            divs = document.getElementsByClassName("dataset");
            for (let i=0; i<divs.length; i++) {
                dataset_list.delete(divs[i].children[1].innerHTML);
                divs[i].children[2].value = "Add";
                divs[i].children[2].innerHTML = button.value;
                divs[i].setAttribute('style', '');
            }
        }
    }
    else if (type == "tests") {
        button = document.getElementById("challt");
        if (button.value == "Add") {
            button.value = "Remove";
            button.innerHTML = button.value;
            divs = document.getElementsByClassName("tests");
            for (let i=0; i<divs.length; i++) {
                tests_list.add(divs[i].children[1].innerHTML);
                divs[i].children[2].value = "Remove";
                divs[i].children[2].innerHTML = button.value;
                divs[i].setAttribute('style', 'background-color: rgb(86, 180, 86);');
            }
        }
        else if (button.value == "Remove") {
            button.value = "Add";
            button.innerHTML = button.value;
            divs = document.getElementsByClassName("tests");
            for (let i=0; i<divs.length; i++) {
                tests_list.delete(divs[i].children[1].innerHTML);
                divs[i].children[2].value = "Add";
                divs[i].children[2].innerHTML = button.value;
                divs[i].setAttribute('style', '');
            }
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
        data: JSON.stringify(Array.from(dataset_list)),
        success: function(response) {
            if (response.result == 0) {
                document.getElementById('msg').innerHTML = "Dataset created correctly";
            }
            else if (response.result == 1) {
                document.getElementById('msg').innerHTML = "No data selected";
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
        data: JSON.stringify(Array.from(tests_list)),
        success: function(response) {
            if (response.result == 0) {
                document.getElementById('msg').innerHTML = "Test created correctly";
            }
            else if (response.result == 1) {
                document.getElementById('msg').innerHTML = "No data selected";
            }
            else {
                document.getElementById('msg').innerHTML = "Error: failed to create tests";
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