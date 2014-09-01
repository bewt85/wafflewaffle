<html>
  <head>
    <title>Cut the WaffleWaffle</title>
    <style>
      
      #boringButton {
        height: 50px;
        width: 100px;
      }
      
      #countChart .c3-line-counts {
        stroke-width: 3px;
      }

    </style>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
    <script src="http://cdnjs.cloudflare.com/ajax/libs/jquery.qrcode/1.0/jquery.qrcode.min.js"></script>
    <link href="/static/c3.css" rel="stylesheet" type="text/css">
    <script src="/static/c3.min.js"></script>
    <script src="/static/d3.min.js"></script>
  </head>
  <body>
    <h1>WaffleWaffle</h1>
    <p>WaffleWaffle provides immediate feedback to presenters</p>
    <p>Spoiler: You can only make a vote up to every 10 seconds</p>
    <p>There is no harm mashing the Zzz button though, just in case</p>
    <p>You can find the code on <a href="https://github.com/bewt85/wafflewaffle">my github account</a>.</p>
    <div id="countChart"></div>
    <form><input type="submit" name="boring" id="boringButton" value="Zzz"></form>
    <p>Spread the wafflewaffle love</p>
    <div id="qrcode"></div>
  <script>
  
    var chart = c3.generate({
      bindto: "#countChart",
      data: {
        columns: [ ["counts"] ]
      },
      point: {
        show: false
      },
      legend: {
        show: false
      },
      axis: { 
        y: { 
          min: 0 
        }, 
        x: { 
          min: 0, 
          type: 'category', 
          tick: { 
            format: function(x) { return '' }, 
            count: 1 
          } 
        } 
      }
    });

    function updateGraphs() {
      $.ajax({
        type: "GET",
        url: "/count",
        async: false,
        success: function(counts) { 
          counts.history.reverse().unshift("counts");
          chart.load({
            columns: [ counts.history ]
          });
        }
      });
    }

    $(document).ready(function () {
      updateGraphs();
      setInterval(updateGraphs, 1000);
      $("#boringButton").click(function(e) {
        e.preventDefault();
        $.ajax({
          type: "POST",
          url: "/count",
        });
      });
      var whereIAm = $(location).attr('href');
      $('#qrcode').qrcode({
          width: 256,
          height: 256,
          text: whereIAm
      });
    });
  
  </script>
  </body>
</html>
