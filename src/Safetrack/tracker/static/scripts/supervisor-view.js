//TODO: factor out these common variables from the js file for each view
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

function addToMonitored(added) {
    monitored[added] = true;
    getAllData();
}

function rmFromMonitored(removed) {
    monitored[removed] = false;
    getAllData();
}

function getTeams() {
    $.ajax({
        url:getTeamsURL,
        dataType: 'json',
        success: function(data) {

            var optionTags = '<option value="">Please Select a Group</option>';

            for (var i = 0; i < data.length; i++) {
                optionTags += '<option value="';
                optionTags += data[i];
                optionTags += '">'+data[i]+'</option>';
            } 
    
            $('#teamSelect').html(optionTags);

        },
        failure: function (data) {
            console.log('Failed at getTeams');
        } 
    });
};

function getAllData(){
	$.getJSON("/getAllData/", function(data){
		filterAndAddData(data);
	});
};

$(document).ready(function() {    	    
    $("#outputData").hide();

    $("#tableHeader").click(function () {
        $("#memberTable").toggle();    
    });

    $("#all").click(function() {
        $.each(monitored, function (key,val) {
            addToMonitored(key)
            if (!$("#"+key).hasClass('highlighted')) {
                $("#"+key).addClass('highlighted');
            }
        })
    });
    $("#none").click(function () {
        $.each(monitored, function (key,val) {
            rmFromMonitored(key);
            if ($("#"+key).hasClass('highlighted')) {
                monitored[key] = false;
                $("#"+key).removeClass('highlighted');
            }
        })
    });

    if ($("#userType").text().substr(13,1)=="S") {
        getMembers(setViewInteractivity);
    }
    if ($("#userType").text().substr(13,1)=="M") {

        $("#teamSelect").change(function () {
            if ($(this).val() != "") {
                getMembers(setViewInteractivity,false,$(this).val()); 
            } 
            else {
                $("#member").empty();
            }
        });

        getTeams();
        initSearchbar(setViewInteractivity,false);
    }
    
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
	var chartDataCopy = [];
	var i = 0;
//	var users = {'e':0,'s':1,'m':2};
	for (user in monitored)
	{
		if(monitored[user] == true)
		{
			if (data.hasOwnProperty(user)) 
			{
				chartData = data[user][type];
				if(chartData.length > chartMaxItems)
				{
					chartData = chartData.slice(0, chartMaxItems-1 );			
				}
				//needed for reference in goals
				chartDataCopy = chartData;
				chart.addSeries({	animation:false, 
									data:chartData, 
									name:usernameToNameMap[user],
									showInLegend: true,
									color:chartColors[i+1],
						            marker: {
						                symbol: chartSymbols[i+1]
						            }
				},false,true);
			}
		}
		i++;
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
				color:chartColors[0],
	            marker: {
	                symbol: chartSymbols[0]
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

//set data at start
getAllData();

//background ajax calls
isConnected = setInterval(checkConnection,10000)
periodicCheck = setInterval(latestInfo,5000)
updateData = setInterval(getAllData,1000)
safetyFeedback = setInterval(serialSafetyFeedback,1000)
