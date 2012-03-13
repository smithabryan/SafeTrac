elem = document.getElementById('rightSide');	
$(document).ready(function()
{    	    
    $('#download').hide();
    $("#outputData").hide();

/*    Downloadify.create('downloadBtn',{
				filename: 'employeeData',
				data: function(){ 
					return document.getElementById('outputData').value;
				},
				onComplete: function(){ alert('Your File Has Been Saved!'); },
				onCancel: function(){ alert('You have cancelled the saving of this file.'); },
				onError: function(){ alert('You must put something in the File Contents or there will be nothing to save!'); },
				transparent: false,
				swf: '/static/assets/downloadify.swf',
				downloadImage: '/static/assets/download.png',
				width: 100,
				height: 30,
				transparent: true,
				append: false
			});
*/
	$(".chartSwitch").click(function(event) {
	var callName = "";
	var type = "";
	if(event.target.id == "TemperatureButton")
	{
		callName = "/getTemperatureData/";
		type = "Temperature"
	}
	else if(event.target.id == "HumidityButton")
	{
		callName = "/getHumidityData/";
		type = "Humidity"
	}
	else if(event.target.id == "NoiseButton")
	{
		callName = "/getNoiseData/";
		type = "Noise"
	}
	else if(event.target.id == "ImpactButton")
	{
		callName = "/getImpactData/";
		type = "Impact Force"
	}
	//set session (do on server through call)
	
	$.getJSON(callName,
        function(data){
	    	chart.yAxis[0].setTitle({
    			text: type
			});
			chart.series[0].setData(data[0],false);
			chart.xAxis[0].setCategories(data[1], false);
			chart.redraw();
        }
	);		
	  		
});	    
});	
setInterval(function(){
	$.getJSON("/serialSafetyFeedback/",function(data){});
	$.getJSON("/serialSafetyRefresh/",function(data){
		$('#status').replaceWith(data);
	});
	
	$.getJSON("/getNewChartData/",
        function(data){
        	if(data.length>0)
        	{
        		if(chart.series[0].data.length < 10)
        		{
				    chart.series[0].addPoint(
				    	{y:data[0][1]},
				    	false,
						false
				   	);
        		}
         		else 
        		{
				    chart.series[0].addPoint(
				    	{y:data[0][1]},
				        false,
				        true
				   	);
        		}
				categories = chart.xAxis[0].categories;
				categories.push(data[0][0]);
				chart.xAxis[0].setCategories(categories, false);
				chart.redraw();
        	}
        }
    );
}, 1000);

//background ajax calls every 30seconds
periodicCheck = setInterval(latestInfo,5000)
