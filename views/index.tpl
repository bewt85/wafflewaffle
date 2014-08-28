<html>
  <head>
    <title>Cut the WaffleWaffle</title>
    <style>
      
      svg {
        font: 10px sans-serif;
      }
      
      .line {
        fill: none;
        stroke: #000;
        stroke-width: 1.5px;
      }
      
      .axis path,
      .axis line {
        fill: none;
        stroke: #000;
        shape-rendering: crispEdges;
      }

      #boringButton {
        height: 50px;
        width: 100px;
      }
      
    </style>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
    <script src="http://d3js.org/d3.v3.min.js"></script>
  </head>
  <body>
    <h1>WaffleWaffle</h1>
    <p>WaffleWaffle provides immediate feedback to presenters</p>
    <p>Spoiler: You can only make a vote up to every 10 seconds</p>
    <p>There is no harm mashing the Zzz button though, just in case</p>
    <p>You can find the code on <a href="https://github.com/bewt85/wafflewaffle">my github account</a>.</p>
    <div id=count></div>
    <form><input type="submit" name="boring" id="boringButton" value="Zzz"></form>
  <script>
  

    var n = 10*60,
        data = d3.range(n).map(function(e) { return 0 });
    
    var margin = {top: 20, right: 40, bottom: 20, left: 40},
        width = window.innerWidth - margin.left - margin.right,
        height = 200 - margin.top - margin.bottom;
    
    var x = d3.scale.linear()
        .domain([0, n - 1])
        .range([0, width]);
    
    var maxY = 5;

    var y = d3.scale.linear()
        .domain([0, maxY])
        .range([height, 0]);

    var yAxis = d3.svg.axis().scale(y).orient("left").tickFormat(d3.format(",.3f")).ticks(5);
    
    var line = d3.svg.line()
        .x(function(d, i) { return x(i); })
        .y(function(d, i) { return y(d); });
    
    var svg = d3.select("#count").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    svg.append("defs").append("clipPath")
        .attr("id", "clip")
      .append("rect")
        .attr("width", width)
        .attr("height", height);
    
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + y(0) + ")")
        .call(d3.svg.axis().scale(x).orient("bottom"));
    
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);
    
    var path = svg.append("g")
        .attr("clip-path", "url(#clip)")
      .append("path")
        .datum(data)
        .attr("class", "line")
        .attr("d", line);
    
    updateGraphs();
    
    function updateGraphs() {
   
     $.ajax({
       type: "GET",
       url: "/count",
       async: false,
       success: function(counts) { 
         data.push.apply(data, counts.history.reverse());
         data.splice(0,n) }
     });

    maxY = d3.max(data)

    if (maxY < 5) {
      maxY = 5;
    }

    y
        .domain([maxY, 0])
        .range([0, height]);

    var yAxis = d3.svg.axis().scale(y).orient("left").tickFormat(d3.format(",.0f")).ticks(5);

      // redraw the line, and slide it to the left
      path
          .attr("d", line)
          .attr("transform", null)
        .transition()
          .duration(1000)
          .ease("linear")
          .attr("transform", "translate(" + x(-1) + ",0)")
          .each("end", updateGraphs);
    
    svg.selectAll("g.y.axis")
            .call(yAxis);
    }

    $(document).ready(function () {
        setInterval(updateGraphs, 1000);
        $("#boringButton").click(function(e) {
          e.preventDefault();
          $.ajax({
            type: "POST",
            url: "/count",
          });
        });
    });
  
  </script>
  </body>
</html>
