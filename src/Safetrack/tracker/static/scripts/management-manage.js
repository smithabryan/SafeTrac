$(function() {

     $.ajax({
		url: "/getConstraints.py/",
		data: {
        },
        dataType: "json",
		success: function(data) {
            $("#tempMax").attr('value',data['T']['max']);
            $("#tempMin").attr('value',data['T']['min']);
            $("#humidMin").attr('value',data['H']['min']);
            $("#humidMax").attr('value',data['H']['max']);
            $("#impactMax").attr('value',data['I']['max']);
            $("#impactMin").attr('value',data['I']['min']);
            $("#noiseMax").attr('value',data['N']['max']);
            $("#noiseMin").attr('value',data['N']['min']);
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
    $("#submit").click(function () {
        $.ajax({
		    url: "/setConstraints.py/",
		    data: {"data":[
                {"type":"T","max":$("#tempMax").val(),"min":$("#tempMin").val()},
                {"type":"N","max":$("#noiseMax").val(),"min":$("#noiseMin").val()},
                {"type":"I","max":$("#impactMax").val(),"min":$("#impactMax").val(),},
                {"type":"H","max":$("#humidMax").val(),"min":$("#humidMax").val(),},
            ]},
            dataType: "json",
		    success: function( data ) {
            }
	    });

 
    })
});
