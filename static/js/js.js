//all js goes here
$( document ).ready(function() {
    
    // OPENING VIEW
    var url = window.location.pathname;
    // remove id and slash if included in route
    url = url.substring(0, url.length - 2);
    var searchString = 'a[href*="' + url + '"]';
    $(searchString).parent().addClass('active');

    // BUSINESS

    // // EVENT LISTENERS
    $('#bizToolbarEdit').on('click', divToggleHidden);
    $('#bizToolbarAddPet').on('click', divToggleHidden);
    $('#bizToolbarEditPet').on('click', divToggleHidden);
    $('#bizToolbarAddService').on('click', divToggleHidden);
    $('#bizToolbarAddPersonToAnimal').on('click', divToggleHidden);
    $('.service_li').on('click', divToggleHidden);
    $('#animal_form_add').on('submit', animalAdd);
    $('#business_form_update').on( 'submit', businessUpdate);
    $('#schedule_date_filter #date_form_filter').on( 'submit', scheduleShow);

    function divToggleHidden(event){
        // activated on button click. shows correct form.
        var divID = '#' + $(this).data('target-div-id');
        $(divID).toggleClass('hidden');
        if( $(this).data('service-id') ){
            $(divID+' form div input[name=id]').val($(this).data('service-id'));            
        }
        // as javascript    this.attr('data-target-div-id')
        // jquery target    console.log(event.target.attr('data-target-div-id');
    }


    function cleanupAfterAjax(divID, formID){
        // activated on ajax success. hides and resets form.
        $(divID).toggleClass('hidden');
        $(formID).trigger('reset');
    }


    function animalDrawList(result){
        // activated on ajax success. parses result object and writes values to correct div.
        var divID = '#animal_list';
        //clear div before repopulating contents
        $(divID).empty();

        $(result).each(function(){
            var name = $(this).attr('name');
            var person = $(this).attr('person');
            var id = $(this).attr('id');
            $(divID).append("<p><a href='/animal/" + id + "'>"+ name + "</a>, " + person + "</p>");
        });
    }


    function animalAdd(evt){
        // activated on form submit. ADD PET via POST call
        evt.preventDefault();
        var formID = '#animal_form_add';
        var divID = '#animal_add';
        var formData = $(formID).serialize();

        $.post('/animal/add', formData, function(result){
            //result is list of sorted Animal objects 
            animalDrawList(result);
            cleanupAfterAjax(divID, formID);
        });
    }


    // BUSINESS FORMS
    // BUSINESS UPDATE
    function businessUpdate(evt) {
        evt.preventDefault();
        var formID = '#business_form_update';
        var divID = '#business_update';
        var formData = $(formID).serialize();
        //update screen with returned json
        $.post('/business/update', formData, function(result){
            businessDrawDetails(result);
            cleanupAfterAjax(divID, formID);
       });
    }

    function businessDrawDetails(result){
        // activated on ajax success. parses result object and writes values to correct div.
        var divID = '#business_details';
        //clear div before repopulating contents
        $(divID).empty();

        var business_name = $(result).attr('business_name');
        var street = $(result).attr('business_street');
        var city = $(result).attr('business_city');
        var state = $(result).attr('business_state');
        var zip = $(result).attr('business_zip');
        var phone = $(result).attr('business_phone');
        var url = $(result).attr('url');
        var license = $(result).attr('license');
        $(divID).append('<h3>'+business_name+'<h3>');
        $(divID).append('<p>'+ street + ', ' +  city + ', ' +  state + ' ' + zip + '</p>');
        $(divID).append('<p>'+ phone +'</p>');
        $(divID).append('<p>'+ url +'</p>');
        $(divID).append('<p>'+ license +'</p>');
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

        $('#draw_map').on('click', function(evt){
            calcRoute(directionsService, directionsDisplay);
        });

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
    }  

    function scheduleShow(evt){
        evt.preventDefault();
        var formID = '#date_form_filter';
        var formData = $(formID).serialize();
        $.get('/reservation/date/format_json', formData, function(result){
            scheduleDrawWaypoints(result);
       });
    }  



    //RESERVATION
    $('.service-radio').on('click', function(evt){
        var cost = $(this).data('service-cost');
        $('#cost').val(cost);
    });



    

    //@todo validate that state is 2 characters
    //@todo validate that telephone is no longer than 10 characters
    //@todo convert first and last to title case by default

//Common pattern
//test for success
//clear form
//hide form
//redraw part of screen
initMap();
});
