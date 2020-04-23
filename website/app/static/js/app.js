$( document ).ready(function() {
  $("#submit_file").hide();
  var startSearch = null;

    $('#devices').on('click', '.clickable-row', function(event) {
      $(this).addClass('bg-primary').siblings().removeClass('bg-primary');
      var clickedBtnID = $(this).attr('id'); // or var clickedBtnID = this.id
      $("#receiver_name_1").val(clickedBtnID);
      $("#submit_file").show();
    });

    // $('#submit_file').on('click', function(event) {
    //   $('#upload_file_form').action = "{% url 'upload_file' %}";
    //   $('#upload_file_form').submit();

    // });

    $('#search').on('click', function(event) {
      $.get("/app/find")
        .done(function(data) {
        startSearch = setInterval(getDeviceList, 5000);
      }); 
    });

    $('#search-stop').on('click', function(event) {
      $.get("/app/find_stop")
        .done(function(data) {
          clearInterval(startSearch);
      }); 
    });

    $('#open').on('click', function(event) {
      $.get("/app/receive")
        .done(function(data) {
      }); 
    });

    $('#close').on('click', function(event) {
      $.get("/app/receive_stop")
        .done(function(data) {
      }); 
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
        var row = $("<tr class='clickable-row' id='"+ name +"'>").appendTo("#devices");
        $("<th>" + name + "</th>").appendTo(row);
        $("</tr>").appendTo("#devices");
    }
  }

});