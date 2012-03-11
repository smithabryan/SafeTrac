$(function() {

    $.ajax({
		url: "/getGoals.py/",
		data: {},
        dataType: "json",
		success: function( data ) {
        }
	});

    $("form div.knobs").append('<div class="inc numbutton">+</div><div class="dec numbutton">-</div>');
    
    $(".numbutton").click(function() {
        var $button = $(this);
        var oldValue = $button.parent().find("input").val();
    
        if ($button.text() == "+") {
    	  var newVal = parseFloat(oldValue) + 1;
    	  // AJAX save would go here
    	} else {
    	  // Don't allow decrementing below zero
    	  if (oldValue >= 1) {
    	      var newVal = parseFloat(oldValue) - 1;
    	      // AJAX save would go here
    	  }
    	}
    	$button.parent().find("input").val(newVal);
    });
});
