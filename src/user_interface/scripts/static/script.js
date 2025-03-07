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

    document.body.appendChild(div);
    document.getElementById("d_" + count).appendChild(p1);
    document.getElementById("d_" + count).appendChild(p2);
    document.getElementById("d_" + count).appendChild(button);
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
        
        const myIterator = data_set.values();
    });
}

function returnData() {
    $.ajax({
        url: '/process',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ 'value': 4321 }),
        success: function(response) {
            document.getElementById('output').innerHTML = response.result;
        },
        error: function(error) {
            console.log(error);
        }
    });
}