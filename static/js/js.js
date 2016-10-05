//all js goes here
$( document ).ready(function() {
    // OPENING VIEW
    function highlightNav(){
        var url = window.location.pathname;
        if(url.substring(0,12) === '/reservation'){
            // handle reservation/map & reservation/schedule
            $('.dropdown-toggle').parent().addClass('active');
            var searchString = 'a[href="' + url + '"]';
        } else {
            // arbitrary number to get beginning of path without / or ids
            url = url.substring(0, 7);
            var searchString = 'a[href*="' + url + '"]';
        }       
            $(searchString).parent().addClass('active');
    }
    highlightNav();


    // BUSINESS
    // // EVENT LISTENERS
    $('#bizToolbarEdit').on('click', divToggleHidden);
    $('#bizToolbarAddPet').on('click', divToggleHidden);
    $('#bizToolbarEditPet').on('click', divToggleHidden); //animal detail
    $('#bizToolbarAddService').on('click', divToggleHidden);
    $('#bizToolbarAddPersonToAnimal').on('click', divToggleHidden); //animal detail
    $('.service_li').on('click', divToggleHidden);
    $('#animal_form_add').on('submit', animalAdd);
    $('#business_form_update').on( 'submit', businessUpdate);

    function divToggleHidden(event){
        // activated on button click. shows correct form.
        var divID = '#' + $(this).data('target-div-id');
        var isHidden = $(divID).hasClass('hidden');

        // ensure all divs hidden before toggling the new selection
        $('#business_update,#animal_add,#service_add,#service_update,#animal_update,#person_add_to_animal').addClass('hidden')

        if (isHidden){
            $(divID).removeClass('hidden');
        } else {
            $(divID).addClass('hidden');
        }

        if( $(this).data('service-id') ){
            // prepopulate form data with the information from clicked on link
            $(divID+' form div input[name=id]').val($(this).data('service-id'));            
            $(divID+' form div input[name=description]').val($(this).data('service-description'));            
            $(divID+' form div input[name=cost]').val($(this).data('service-cost'));            
        }
        // as javascript    this.attr('data-target-div-id')
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
            businessDrawDetails(result, formID);
            cleanupAfterAjax(divID, formID);
       });
    }

    function businessDrawDetails(result, formID){
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
        // update hidden form with new values
        $(formID + ' input[name=business_name]').attr('value', business_name);            
        $(formID + ' input[name=street]').attr('value', street);            
        $(formID + ' input[name=city]').attr('value', city);            
        $(formID + ' input[name=state]').attr('value', state);            
        $(formID + ' input[name=zip]').attr('value', zip);            
        $(formID + ' input[name=phone]').attr('value', phone);            
        $(formID + ' input[name=url]').attr('value', url);            
        $(formID + ' input[name=license]').attr('value', license);            

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
});
