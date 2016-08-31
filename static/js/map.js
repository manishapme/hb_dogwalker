//all js goes here
$( document ).ready(function() {
    
    console.log('top of map.js file');

    // // EVENT LISTENERS
    $('#schedule_date_filter #date_form_filter').on( 'submit', scheduleShow);
    if ($('#date_form_filter input[name=date_filter').val()){
        //render map if the date filter is already populated from session data
        console.log('top of map.js file line 32');
        scheduleShow();
    }
// SCHEDULE /////////////////////////////////////////////////////////////////////

    //@todo get business address as default starting route using geocode latlong

    function initMap() {
        var directionsService = new google.maps.DirectionsService();
        var directionsDisplay = new google.maps.DirectionsRenderer();        //Constructor creates a new map - only center and zoom are required.
        var map = new google.maps.Map(document.getElementById('map'), {
            center: {lat: 40.7413549, lng: -73.9980244},
            zoom: 13
        });
        //documentation for this implementation of directionsservice
        //https://developers.google.com/maps/documentation/javascript/directions
        directionsDisplay.setMap(map);
        console.log('top of map.js file line 23');

        // $('#schedule_date_filter #date_form_filter').on('change', function(evt){
        //     console.log('top of map.js file line 26');
        //     calcRoute(directionsService, directionsDisplay);
        // });

        // if ($('#date_form_filter input[name=date_filter').val()){
        //     //render map if the date filter is already populated from session data
        //     console.log('top of map.js file line 32');
            calcRoute(directionsService, directionsDisplay);
        // }
    }


    function calcRoute(directionsService, directionsDisplay) {
        //@todo get business address as default starting route using geocode latlong
        var start = '43621 Pacific Commons Blvd.,Fremont,CA 94538';
        var end = '2 Graham Place, Oakland, CA 94619';
        var waypoints = getWaypoints();
        console.log('called calcRoute');
        var request = {
            origin: start,
            destination: end,
            waypoints: waypoints,
            travelMode: 'DRIVING'
        };
        directionsService.route(request, function(result, status) {
            if (status == 'OK') {
                directionsDisplay.setDirections(result);
            } else {
                window.alert('Directions request failed due to ' + status);
            }
        });
    }


    //no need to declare index_position. here so I understand what gets passed by default
    //this loop grabs all necessary address
    function getWaypoints(){
        console.log('called getWaypoints');
        var locations = [];
        $('#scheduled_address_list li').each(function(index_position){
            var waypoint = $(this).text();
            locations.push({ location: waypoint, stopover: true });
                    //     get lat/long for each address
                    // append each lat/long as marker to map
        });
        console.log('getwaypoints');

        return locations
    }

    function getLatLong() {

    }



    function scheduleDrawWaypoints(result){
        // activated on ajax success. parses result object and writes values to correct div.
        var divID = '#scheduled_address_list';
        //clear div before repopulating contents
        $(divID).empty();
        $(result).each(function(){
            var animal_id = $(this).attr('animal_id');
            var animal_name = $(this).attr('animal_name');
            var address = $(this).attr('address');
            $(divID).append('<li id='+animal_id+' data-animal-name='+animal_name+'>'+ address + '</li>');
        });
        console.log('inside send of draw waypoints');

    }  

    function scheduleShow(evt){
        evt.preventDefault();
        console.log('inside scheduleShow');
        var formID = '#date_form_filter';
        var formData = $(formID).serialize();
        $.get('/reservation/date/format_json', formData, function(result){
            console.log('inside scheduleShow get route');
            scheduleDrawWaypoints(result);
            initMap();
       });
    }  

// initMap();
});
