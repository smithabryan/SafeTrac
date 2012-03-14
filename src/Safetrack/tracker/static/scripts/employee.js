elem = document.getElementById('rightSide');	

var type = "N"
var yAxisType = "Noise"
var chartMaxItems = 10;
var chartSymbols = [
      	'circle', 
      	'diamond', 
      	'square', 
      	'triangle', 
      	'triangle-down'
      ]
var chartColors = [
     	'#4572A7', 
     	'#AA4643', 
     	'#89A54E', 
     	'#80699B', 
     	'#3D96AE', 
     	'#DB843D', 
     	'#92A8CD', 
     	'#A47D7C', 
     	'#B5CA92'
     ]

$(document).ready(function()
{    	    
    $('#download').hide();
    $("#outputData").hide();

    Downloadify.create('downloadBtn',{
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

    //initially assume that the data loaded in from the server is wrong, 
    //and that we need to get it again to set it on the chart
    //NOTE: this is an inefficient assumption

    getAllData();
    
    //chart switching functionality
	$(".chartSwitch").click(function(event) {
		var callName = "";
		if(event.target.id == "TemperatureButton")
		{
			callName = "/getTemperatureData/";
			type = "T"
			yAxisType = "Temperature"
		}
		else if(event.target.id == "HumidityButton")
		{
			callName = "/getHumidityData/";
			type = "H"
			yAxisType = "Humidity"			
		}
		else if(event.target.id == "NoiseButton")
		{
			callName = "/getNoiseData/";
			type = "N"
			yAxisType = "Noise"			
		}
		else if(event.target.id == "ImpactButton")
		{
			callName = "/getImpactData/";
			type = "I"
			yAxisType = "Impact"			
		}
		
		getAllData();
	});	    
});	

function filterAndAddData(data) {
	//remove everything from chart 
	while(chart.series.length > 0)
	    chart.series[0].remove(false);
	
	//set axis name
	chart.yAxis[0].setTitle({
		text: yAxisType
	});

	//set data
	var chartDataCopy;
	if (data.hasOwnProperty('e')) 
	{
		chartData = data['e'][type];
		if(chartData.length > chartMaxItems)
		{
			chartData = chartData.slice(0, chartMaxItems-1 );			
		}
		//needed for reference in goals
		chartDataCopy = chartData;
		chart.addSeries({	animation:false, 
							data:chartData, 
							name:"Employee",
							showInLegend: true, 
							color:chartColors[0],
				            marker: {
				                symbol: chartSymbols[0]
				            }
		},false,true);
	}
	
	//set goals
	//NOTE: Assumes only one item in each goal 
	if (data.hasOwnProperty('goals')) 
	{
		if (data['goals'].hasOwnProperty(type))
		{
			//make goals array the same length as data
			chartData = data['goals'][type];
			for (var i = data['goals'][type].length; i < chartDataCopy.length ; i++)
			{
				chartData.push(chartData[i-1]);
			}
			
			chart.addSeries({	animation:false, 
				data:chartData, 
				name:"Goals",
				showInLegend: true, 
				color:chartColors[1],
	            marker: {
	                symbol: chartSymbols[1]
	            }
			},false,true);
		}
	}
		
	//set times
	if (data.hasOwnProperty('times')) 
	{
		chartData = data['times'];
		if(chartData.length > chartMaxItems)
		{
			chartData = chartData.slice(0, chartMaxItems-1 );			
		}		
		chart.xAxis[0].setCategories(chartData, false);
	}
	chart.redraw();
}

function getAllData(){
	$.getJSON("/getAllData/", function(data){
		filterAndAddData(data);
	});
}

//background ajax calls every 30seconds
periodicCheck = setInterval(latestInfo,5000)

setInterval(function(){
	$.getJSON("/serialSafetyFeedback/",function(data){});
	$.getJSON("/serialSafetyRefresh/",function(data){
		$('#status').replaceWith(data);
	});
	
	getAllData();
}, 1000);

