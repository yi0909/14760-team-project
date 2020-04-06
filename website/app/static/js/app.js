$( document ).ready(function() {
  var startSearch = null;
    $('#devices').on('click', '.clickable-row', function(event) {
      $(this).addClass('bg-primary').siblings().removeClass('bg-primary');
    });

    $('#search').on('click', function(event) {
      $.get("/app/find")
        .done(function(data) {
        startSearch = setInterval(getDeviceList, 5000);
      }); 
    });

    $('#search-stop').on('click', function(event) {
      clearInterval(startSearch);
    });

    function getDeviceList() {
      $.get("/app/find_list")
        .done(function(data) {
          updateDeviceList(data);
      });
    }

    function updateDeviceList(data) {
      $('#devices').empty();
      for(var i = 0; i < data.devices.length; i++) {
        console.log(data.devices[i])
        var name = data.devices[i].name;
        var row = $("<tr class='clickable-row'>").appendTo("#devices");
        $("<th>" + name + "</th>").appendTo(row);
        $("</tr>").appendTo("#devices");
    }
  }
});