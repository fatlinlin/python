/*
  what is bad about this design:
  - the client knows too much about the rules
  (for ex, don't play twice a box is coded on client and on server)
  - the human and computer are not treated the same

  a click on a box should send the id,
  and the server should eventually ask the human to play again

  the same should happen on the server side

  then, the server send the new grid & status to the client
*/

function xml_http_post(url, data, callback) {
    var req = new XMLHttpRequest();
    req.open("POST", url, true);
    req.onreadystatechange = function() {
        if (req.readyState == 4) {
            callback(req);
        }
    }
    req.send(data);
}

function set_status(status) {
    var elem = document.getElementById('response');
    elem.innerHTML =  "status: " + status;
}

function test_handle(req) {
    var response = JSON.parse(req.responseText);
    set_status(response.status)
    for (var box in ttt.grid)
    {
    ttt.grid[box].innerHTML = response.grid[box]
    }
}

function Player(symbol) {
    this.symbol = symbol;
}

Player.prototype.play = function(box_id) {
    var box = ttt.grid[box_id];
    box.innerHTML = this.symbol;
    box.onclick = function() {};
}

function getJSONGrid() {
    var res = {};
    for (var i in ttt.grid)
    {
    res[i] = ttt.grid[i].innerHTML
    }
    return JSON.stringify({grid : res});
}

var ttt = {
    players : {
    human : new Player("o"),
    computer : new Player("x")
    },
    grid : (function() {
    var res = {};
    var boxes = document.getElementsByTagName("td");
    for (var i = 0; i < 9; i++)
    {
        var box = boxes[i];
        var id = box.id;
        res[id] = box;
    }
    return res
    })()
}

function reset() {
    var reseter = new Player("");
    for (var i in ttt.grid)
    {
    reseter.play(i);
    }
    initEvents();
    xml_http_post("reset", {}, function() {})
}

function initEvents() {
    for (var i in ttt.grid)
    {
    var box = ttt.grid[i];
    box.onclick = (function() {
        var id = box.id;
        return function() {
        ttt.players.human.play(id);
        var data = getJSONGrid();
        xml_http_post("play/" + id, data, test_handle)
        };
    })();
    }
    document.getElementById("reset").onclick = reset
    windows.onload = reset
    set_status("start")
}
