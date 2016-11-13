//Global var
var actualArray = [];


// jQuery helpers for FORM
$(document).ready(function () {
    $('#SubmitData').click(function () {
        var input = $('#getFromInput').val();
        var arr = input.split(",");
        postArr(arr);
    });
    //postIncrement
    $('#SubmitIncrement').click(function () {
        var input = $('#getIncrement').val();
        var number = Number(input);
        postIncrement(number);
    });

    //postDeleteElem
    $('#SubmitDeleteElem').click(function () {
        var input = $('#getDelete').val();
        var number = Number(input);
        postDeleteElem(number);
    });

    //ReadTree
    $('#ReadTree').click(function () {
        requestFile();
    });

    //ReadTree
    $('#SaveTree').click(function () {
        saveFile();
    });
});

//end jQuery


/*REST API   json biz*/
function saveFile() {
    console.log(actualArray)
    $.ajax({
        type: "POST",
        url: '/api/save',
        data: {
            arr: actualArray
        },
        success: function (data) {
            console.log(data)
            askForJSON(data);
            console.log("success")
        },
        dataType: 'json'
    });

    alert('Archivo Guardado con exito');
}

function requestFile() {
    $.ajax({
        type: "POST",
        url: '/api/read',
        data: {
            arr: {}
        },
        success: function (data) {
            //alert(data);
            askForJSON(data);
            console.log("success")
        },
        dataType: 'json'
    });

    alert('Archivo Abierto con exito');
}

function postArr(myArr) {
    console.log(myArr)
    $.ajax({
        type: "POST",
        url: /send/,
        data: {
            arr: myArr
        },
        //{csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value}
        success: function (data) {
            console.log(data)
            askForJSON(data);
            console.log("success")
        },
        dataType: 'json'
    });
}

function postIncrement(increment) {
    actualArray.push(increment);
    console.log(actualArray)
    $.ajax({
        type: "POST",
        url: /send/,
        data: {
            arr: actualArray
        },
        success: function (data) {
            console.log(data)
            askForJSON(data);
            console.log("success")
        },
        dataType: 'json'
    });
}

function postDeleteElem(elem) {
    var index = actualArray.indexOf(elem);
    if (index >= 0) {
        console.warn(actualArray[index])
        actualArray.splice(index, 1);
        console.warn(actualArray)
        $.ajax({
            type: "POST",
            url: /send/,
            data: {
                arr: actualArray
            },
            success: function (data) {
                console.log(data)
                askForJSON(data);
                console.log("success")
            },
            dataType: 'json'
        });

    } else {
        alert('No existe');
        return;
    }
}
// end json biz 

/*
    var table =[];
    
table = [{"parent": "2", "name": "1"}, {"parent": "3", "name": "2"}, {"parent": "5", "name": "3"}, {"parent": "3", "name": "4"}, {"parent": "13", "name": "5"}, {"parent": "8", "name": "6"}, {"parent": "5", "name": "8"}, {"parent": "10", "name": "9"}, {"parent": "8", "name": "10"}, {"parent": "", "name": "13"}, {"parent": "36", "name": "14"}, {"parent": "14", "name": "27"}, {"parent": "13", "name": "36"}, {"parent": "76", "name": "75"}, {"parent": "77", "name": "76"}, {"parent": "36", "name": "77"}, {"parent": "77", "name": "78"}, {"parent": "78", "name": "90"}]

*/

// d3 with Promise
var root = [];

function todo(rawData) {
    var strat = Promise.resolve();
    strat.then(function (success, error) {
        return new Promise(function (yey, nop) {
                root = d3.stratify()
                    .id(function (d) {
                        return d.name;
                    })
                    .parentId(function (d) {
                        return d.parent;
                    })
                    (rawData);
                yey();
            })
            //success();

    }).then(function () {
        //init root
        console.log('Init roo after Promise')
        root.x0 = height / 2;
        root.y0 = 0;

        function collapse(d) {
            if (d.children) {
                d._children = d.children;
                d._children.forEach(collapse);
                d.children = null;
            }
        }

        //root.children.forEach(collapse);
        update(root);

    });
}

function askForJSON(data = []) {
    var api;
    if (data.length < 1) {
        api = "/api/data";
        d3.json(api, function (error, rawData) {
            if (error) throw error;
            todo(rawData[0]);
            actualArray = rawData[1]; //save actual array
        });
    } else {
        todo(data[0]);
        actualArray = data[1]; //save actual array
    }

} //askforJSON
askForJSON();

// d3 Promise


//D3 stuff
var margin = {
        top: 20,
        right: 120,
        bottom: 20,
        left: 120
    },
    width = 1200 - margin.right - margin.left,
    height = 750 - margin.top - margin.bottom;

var i = 0,
    duration = 750,
    root;

var tree = d3.layout.tree()
    .size([height, width]);

var diagonal = d3.svg.diagonal()
    .projection(function (d) {
        return [d.y, d.x];
    });

var svg = d3.select("#d3-one").append("svg")
    .attr("width", width + margin.right + margin.left)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");




d3.select(self.frameElement).style("height", "800px");

function update(source) {

    // Compute the new tree layout.
    var nodes = tree.nodes(root).reverse(),
        links = tree.links(nodes);

    // Normalize for fixed-depth.
    nodes.forEach(function (d) {
        d.y = d.depth * 120;
    });

    // Update the nodes…
    var node = svg.selectAll("g.node")
        .data(nodes, function (d) {
            return d.id || (d.id = ++i);
        });

    // Enter any new nodes at the parent's previous position.
    var nodeEnter = node.enter().append("g")
        .attr("class", "node")
        .attr("transform", function (d) {
            return "translate(" + source.y0 + "," + source.x0 + ")";
        })
        .on("click", click);

    nodeEnter.append("circle")
        .attr("r", 1e-6)
        .style("fill", function (d) {
            return d._children ? "lightsteelblue" : "#fff";
        });

    nodeEnter.append("text")
        .attr("x", function (d) {
            return d.children || d._children ? -10 : 10;
        })
        .attr("dy", ".35em")
        .attr("text-anchor", function (d) {
            return d.children || d._children ? "end" : "start";
        })
        .text(function (d) {
            return d.id;
        })
        .style("fill-opacity", 1e-6);

    // Transition nodes to their new position.
    var nodeUpdate = node.transition()
        .duration(duration)
        .attr("transform", function (d) {
            return "translate(" + d.y + "," + d.x + ")";
        });

    nodeUpdate.select("circle")
        .attr("r", 10.5)
        .style("fill", function (d) {
            return d._children ? "lightsteelblue" : "#fff";
        });

    nodeUpdate.select("text")
        .style("fill-opacity", 1);

    // Transition exiting nodes to the parent's new position.
    var nodeExit = node.exit().transition()
        .duration(duration)
        .attr("transform", function (d) {
            return "translate(" + source.y + "," + source.x + ")";
        })
        .remove();

    nodeExit.select("circle")
        .attr("r", 1e-6);

    nodeExit.select("text")
        .style("fill-opacity", 1e-6);

    // Update the links…
    var link = svg.selectAll("path.link")
        .data(links, function (d) {
            return d.target.id;
        });

    // Enter any new links at the parent's previous position.
    link.enter().insert("path", "g")
        .attr("class", "link")
        .attr("d", function (d) {
            var o = {
                x: source.x0,
                y: source.y0
            };
            return diagonal({
                source: o,
                target: o
            });
        });

    // Transition links to their new position.
    link.transition()
        .duration(duration)
        .attr("d", diagonal);

    // Transition exiting nodes to the parent's new position.
    link.exit().transition()
        .duration(duration)
        .attr("d", function (d) {
            var o = {
                x: source.x,
                y: source.y
            };
            return diagonal({
                source: o,
                target: o
            });
        })
        .remove();

    // Stash the old positions for transition.
    nodes.forEach(function (d) {
        d.x0 = d.x;
        d.y0 = d.y;

    });
}

// Toggle children on click.
function click(d) {
    if (d.children) {
        d._children = d.children;
        d.children = null;
    } else {
        d.children = d._children;
        d.children.forEach(expand); //Expand all at once
        d._children = null;
    }
    update(d);
}

function expand(d) {
    if (d._children) {
        d.children = d._children;
        d.children.forEach(expand);
        d._children = null;
    }
}