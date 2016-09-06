//all js goes here
$( document ).ready(function() {
    
    // // EVENT LISTENERS
    $('#schedule_date_filter #date_form_filter').on( 'submit', scheduleShow);
    if ($('#date_form_filter input[name=date_filter]').val()){
        //render map if the date filter is already populated from session data
        initMap();
    }
// SCHEDULE /////////////////////////////////////////////////////////////////////

    //@todo get business address as default starting route using geocode latlong

    function initMap() {
        var directionsService = new google.maps.DirectionsService();
        var directionsDisplay = new google.maps.DirectionsRenderer();        //Constructor creates a new map - only center and zoom are required.
        var map = new google.maps.Map(document.getElementById('map'), {
            center: {lat: 37.5015665, lng: -121.9730203},
            zoom: 13
        });
        //documentation for this implementation of directionsservice
        //https://developers.google.com/maps/documentation/javascript/directions
        directionsDisplay.setMap(map);

            calcRoute(directionsService, directionsDisplay);
    }


    function calcRoute(directionsService, directionsDisplay) {
        //@todo get business address as default starting route using geocode latlong
        var start = {lat: 37.5015665, lng: -121.9730203};
        var end = '2 Graham Place, Oakland, CA 94619';
        var waypoints = getWaypoints();
        var request = {
            origin: start,
            destination: end,
            waypoints: waypoints,
            optimizeWaypoints: true,
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
        var locations = [];

        $('#scheduled_address_list li').each(function(index_position){
            var waypoint = $(this).data('address');
            locations.push({ location: waypoint, stopover: true });
                    //     get lat/long for each address
                    // @todo append each lat/long as marker to map
        });

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
            $(divID).append('<li id=\''+animal_id+'\' data-address=\''+address+'\'>'+ animal_name + ', '+ address + '</li>');
        });

    }  

    function scheduleShow(evt){
        evt.preventDefault();
        var formID = '#date_form_filter';
        var formData = $(formID).serialize();
        $.get('/reservation/date/format_json', formData, function(result){
            scheduleDrawWaypoints(result);
            initMap();
       });
    }

// initMap();
});
