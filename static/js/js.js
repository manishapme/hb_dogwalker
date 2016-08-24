//all js goes here
$( document ).ready(function() {
    
    // OPENING VIEW
    // var url = window.location;
    // // Will only work if string in href matches with location
    // $('ul.nav a[href="'+ url +'"]').parent().addClass('active');

    // BUSINESS FORMS
    $( '#business_form_update').on( 'submit', function(evt) {
        evt.preventDefault();

        // business_update route. disable/enable inputs on update form
        if ($('#business_form_update input').prop('disabled')){
            
            $('#business_form_update :input').prop( 'disabled', false );
            $('#business_form_update input[type=submit]').val( 'Submit changes' );
        } else {
           //if form was enabled, allow them to submit and post to DB.
           var formData = {}
           $('#business_form_update .form-control').each(function(){
                var key = $(this).attr('name');
                var val = $(this).val();
                formData[key] = val;
           });
           //update screen with returned json
           $.post('/business/update', formData, function(result){
                $('#business_form_update :input').prop( 'disabled', false );
                $('#business_form_update input[type=submit]').val( 'Edit Business Details' );
                console.log(result) 
           });

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