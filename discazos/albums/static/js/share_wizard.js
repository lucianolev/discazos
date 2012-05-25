//Javascript helper functions for the 'share a discazo' wizard

$(document).ready(function() {
  //switch artist form fields depending on artist type
  $("input[name='artist_type']").change(function() {
    var checkedValue = $(this).filter(":checked").val(); 
    if(checkedValue == 'P') {
      $("#group-artist-extra-info").hide();
    } else if (checkedValue == 'G') {
      $("#group-artist-extra-info").show();
    }
  });
});
