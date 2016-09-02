//all js goes here
$( document ).ready(function() {
    
    // // EVENT LISTENERS
    $('#scheduleTimeLine').on( 'click', drawTimeLine);


    function drawTimeLine(evt){
        //http://visjs.org/docs/timeline/
        //jquery returns a list, and we want only the div so need to call index position
        var container = $('#visualization')[0]; 
        // var container = document.getElementById('visualization')
        $.get('/reservation/timeline/json', function(result){
            console.log(result);
            var items = new vis.DataSet(result);
            var options = {
                groupOrder: 'content'  // groupOrder can be a property name or a sorting function
            };
            // var options = {
            //     // zoomable: false,
            //     // margin: 0
            // };
            var names = ['Walk', 'Board'];
            var groups = new vis.DataSet();
            for (var g = 0; g < 2; g++) {
                groups.add({id: g, content: names[g]});
            }
            var timeline = new vis.Timeline(container);
            timeline.setOptions(options);
            timeline.setGroups(groups);
            timeline.setItems(items);
        });
    }

drawTimeLine();
});
