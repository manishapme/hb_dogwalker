//all js goes here
$( document ).ready(function() {
    
    // OPENING VIEW
    // var url = window.location;
    // // Will only work if string in href matches with location
    // $('ul.nav a[href="'+ url +'"]').parent().addClass('active');

    // BUSINESS

    // // EVENT LISTENERS
    $('#bizToolbarAddPet').on('click', divToggleHidden);

    $('#bizToolbarAddService').on('click', function(evt){});

    // BUSINESS TOOLBAR
    $('#bizToolbarEdit').on('click', function(evt){
        // enable inputs on update form when toolbar clicked
        if ($('#business_form_update input').prop('disabled')){
            
            $('#business_form_update :input').prop( 'disabled', false );
            $('#business_form_update input[type=submit]').removeClass('hidden');
        } 
    });



    function cleanupAfterAjax(divID, formID){
        $(divID).toggleClass('hidden');
        $(formID).trigger('reset');
    }

    function divToggleHidden(event){
        var divID = '#' + $(this).data('target-div-id');
        $(divID).toggleClass('hidden');
        // as javascript    this.attr('data-target-div-id')
        // jquery target    console.log(event.target.attr('data-target-div-id');
    }


    // BUSINESS FORMS
    // BUSINESS UPDATE
    $( '#business_form_update').on( 'submit', function(evt) {
        evt.preventDefault();

        if ($('#business_form_update input').is(':enabled')){

           var formData = $('#business_form_update').serialize();
           //update screen with returned json
           $.post('/business/update', formData, function(result){
                $('#business_form_update :input').prop( 'disabled', true);
            $('#business_form_update input[type=submit]').addClass('hidden');
                console.log(result);
           });

        }
    });

    // ADD PET
    $('#animal_form_add').on('submit', function(evt){
        evt.preventDefault();

        var formData = $('#animal_form_add').serialize();

        $.post('/animal/add', formData, function(result){
            console.log(result);
        });
    });



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
