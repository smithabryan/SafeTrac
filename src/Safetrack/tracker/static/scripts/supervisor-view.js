
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

function setInteractivity() {
    var groupBlk = $('#groupBlk ul');
    var members = groupBlk.find('li');
    $.each(members,function (ind) {
        $(members[ind]).qtip({
            content: $(members[ind]).attr('id')+"<br />"+$(members[ind]).attr('data-location'),
            show: 'mouseover',
            hide: 'mouseout',
            position: {
                corner: {
                    target: 'topRight',
                    tooltip: 'bottomLeft'
                }
            },
            style: {
                padding: 5,
                border: {
                    radius: 5
                }
            }
        });                          

        $(members[ind]).click(function () {

            if ($(this).hasClass('highlighted')) {
                $(this).removeClass('highlighted');
                rmFromMonitored($(this).attr('id'));
            }
            else {
                $(this).addClass('highlighted');
                addToMonitored($(this).attr('id')); 
            }
       }); 
    });
};

function getAllData(){
	$.getJSON("/getAllData/", function(data){
		filterAndAddData(data);
	});
};

$(document).ready(function()
	{    	    
    $("#tableHeader").click(function () {
        $("#memberTable").toggle();    
    });  
    $("#all").click(function() {
        $.each(monitored, function (key,val) {
            if (!$("#"+key).hasClass('highlighted')) {
                monitored[key] = true;
                $("#"+key).addClass('highlighted');
            }
        })
    });
    $("#none").click(function () {
        $.each(monitored, function (key,val) {
            if ($("#"+key).hasClass('highlighted')) {
                monitored[key] = false;
                $("#"+key).removeClass('highlighted');
            }
        })
    });

    if ($("#userType").text().substr(13,1)=="S") {
        getMembers(setInteractivity);
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
	var users = {'e':0,'s':1,'m':2};
	for (user in monitored)
	{
		if(monitored[user] == true)
		{
			if (data.hasOwnProperty( nameToUsernameMap[user] )) 
			{
				chartData = data[nameToUsernameMap[user]][type];
				if(chartData.length > chartMaxItems)
				{
					chartData = chartData.slice(0, chartMaxItems-1 );			
				}
				//needed for reference in goals
				chartDataCopy = chartData;
				chart.addSeries({	animation:false, 
									data:chartData, 
									name:user,
									showInLegend: true, 
									color:chartColors[i],
						            marker: {
						                symbol: chartSymbols[i]
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

//set data at start
getAllData();

//background ajax calls every 30seconds
periodicCheck = setInterval(latestInfo,5000)
updateData = setInterval(getAllData,1000)