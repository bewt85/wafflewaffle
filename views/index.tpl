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

      .space-top {
        margin-top: 20px;
      }

      .space-bottom {
        margin-bottom: 20px;
      }

      @media (max-width: 500px) {
        #boringButton {
          width:100%;
        }
      }

    </style>
    <script src="/static/jquery.min.js"></script>
    <script src="/static/jquery.qrcode.min.js"></script>
    <link rel="stylesheet" href="/static/bootstrap.min.css">
    <script src="/static/bootstrap.min.js"></script>
    <link href="/static/c3.css" rel="stylesheet" type="text/css">
    <script src="/static/c3.min.js"></script>
    <script src="/static/d3.min.js"></script>
  </head>
  <body>
    <div class="container">
      <div class="row page-header col-md-12">
        <h1>WaffleWaffle</h1>
        <p class="lead">WaffleWaffle provides immediate feedback to presenters</p>
      </div>
      <div class="row col-md-12">
        <div class="alert alert-info"><strong>Spoiler</strong> You can only vote once every 10 seconds</div>
        <p>You can find the code on <a href="https://github.com/bewt85/wafflewaffle">my github account</a>.</p>
      </div>
      <div class="row col-md-12 space-top">
        <div id="countChart"></div>
        <form><input type="submit" name="boring" class="btn btn-primary btn-large" id="boringButton" value="Zzz"></form>
      </div>
      <div class="row col-md-12 space-top space-bottom">
        <h2>Spread the WaffleWaffle love</h2>
        <p>Why not share WaffleWaffle with your neighbour?</p>
        <div id="qrcode"></div>
      </div>
    </div>
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
            min: 0.1,
            padding: {
              bottom: 0.1
            } 
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
