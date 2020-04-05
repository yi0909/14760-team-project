$( document ).ready(function() {
    $('#devices').on('click', '.clickable-row', function(event) {
      $(this).addClass('bg-primary').siblings().removeClass('bg-primary');
    });
});