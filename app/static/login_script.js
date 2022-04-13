  $( "form" ).on( "submit", function() {

        var has_empty = false;

        $(this).find( 'input[type!="hidden"]' ).each(function () {

        if ( ! $(this).val() ) {
            has_empty = true;
            $(this).fadeOut(200).fadeIn(200).fadeOut(200).fadeIn(200).fadeOut(200).fadeIn(200)

            }
   });

   if ( has_empty ) { $('#span').css('display','block') ;return false; }
});
 $( document ).ready(function() {
        $("#details").css('display','none')
    });
