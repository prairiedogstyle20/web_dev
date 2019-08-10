
var svg = d3.select("svg"),
 width = +svg.attr("width"),
 height = +svg.attr("height");

svg.selectAll("*").remove();

d3.json("karate_club_data_end.json").then(function(data){
  console.log(data)
    var nodes = data.nodes;
    var links = data.links;

    var simulation = d3.forceSimulation().nodes(nodes);

    simulation
    .force("charge_force", d3.forceManyBody())
    .force("center_force", d3.forceCenter(width / 2, height / 2));

    var node = svg.append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(nodes)
        .enter()
        .append("circle")
        .attr("r", 5)
        .attr("fill", "red");

    var link = svg.append("g")
          .attr("class", "links")
        .selectAll("line")
        .data(links)
        .enter().append("line")
          .attr("stroke-width", 2);

simulation.on("tick", tickActions );

var link_force =  d3.forceLink(links)
                        .id(function(d) { return d.id; })

simulation.force("links",link_force)

function tickActions() {
//update circle positions to reflect node updates on each tick of the simulation
node
    .attr("cx", function(d) { return d.x; })
    .attr("cy", function(d) { return d.y; })

link
    .attr("x1", function(d) { return d.source.x; })
    .attr("y1", function(d) { return d.source.y; })
    .attr("x2", function(d) { return d.target.x; })
    .attr("y2", function(d) { return d.target.y; });
}

var drag_handler = d3.drag()
    .on("drag", function(d) {
          d3.select(this)
            .attr("cx", d.x = d3.event.x  )
            .attr("cy", d.y = d3.event.y  );
            });
  drag_handler(node);

});
