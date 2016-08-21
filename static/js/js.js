//all js goes here
$( document ).ready(function() {
    
    // OPENING VIEW
    // var url = window.location;
    // // Will only work if string in href matches with location
    // $('ul.nav a[href="'+ url +'"]').parent().addClass('active');

    // BUSINESS FORMS
    $( '#business_form_update').on( 'submit', function(evt) {
        // business_update route. disable/enable inputs on update form
        if ($('#business_form_update input').prop('disabled')){
            
            evt.preventDefault();
            $('#business_form_update :input').prop( 'disabled', false );
            $('#business_form_update input[type=submit]').val( 'Submit changes' );
        } 
    });

    //RESERVATION
    $('.service-radio').on('click', function(evt){
        var cost = $(this).data('service-cost');
        $('#cost').val(cost);
    });

    //@todo validate that state is 2 characters
    //@todo validate that telephone is no longer than 10 characters
    //@todo convert first and last to title case by default



});