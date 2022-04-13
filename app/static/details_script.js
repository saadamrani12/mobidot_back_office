$(document).ready(function() {
    $("#force").click(function() {

        $('#span_ticket').css({
            'display': 'none'
        });
        $('#span_solde').css({
            'display': 'none'
        });

        $("#inp_ticket").css({
            'border-color': ''
        });
        $("#inp_solde").css({
            'border-color': ''
        });

        $("#inp_ticket").val("");
        $("#inp_solde").val("");

        $('#spn').css({
            'display': 'none'
        });
        if ($("#ticket_num").is(":visible") && $("#oc_solde").is(":visible")) {

            $('#inp_ticket').attr('type', 'hidden');
            $("#ticket_num").slideToggle("slow", "linear");
            $("#oc_solde").slideToggle("slow", "linear");
            $("#valider").slideToggle("slow", );
        } else if ($("#oc_solde").is(":visible")) {
            $('#inp_ticket').attr('type', 'text');
            $("#ticket_num").slideToggle("slow", );
//            $('#form').attr('action', '{{ url_for("back_office.force_reservation")}}');
            $('#form').attr('action', '/force');


        } else {
            $('#inp_ticket').attr('type', 'text');
            $("#ticket_num").slideToggle("slow", "linear");
            $("#oc_solde").slideToggle("slow", "linear");
//            $('#form').attr('action', '{{ url_for("back_office.force_reservation")}}');
            $('#form').attr('action', '/force');
            $("#valider").slideToggle("slow", );
        }
        ;
    });
})
$(document).ready(function() {
    $("#solde_ind").click(function() {

        $('#span_solde').css({
            'display': 'none'
        });

        $("#inp_ticket").css({
            'border-color': ''
        });
        $("#inp_solde").css({
            'border-color': ''
        });

        $("#inp_ticket").val("");
        $("#inp_solde").val("");
        $('#span_ticket').css({
            'display': 'none'
        });
        $('#spn').css({
            'display': 'none'
        });
        if ($("#ticket_num").is(":visible")) {
            $('#inp_ticket').attr('type', 'hidden');
            $("#ticket_num").slideToggle("slow", );
//            $('#form').attr('action', '{{ url_for("back_office.cancel_reservation")}}');
            $('#form').attr('action', '/soldeIndisponible');
        } else {
            $("#oc_solde").slideToggle("slow", "linear");
//            $('#form').attr('action', '{{ url_for("back_office.cancel_reservation")}}');
            $('#form').attr('action', '/soldeIndisponible');
            $("#valider").slideToggle("slow", );
        }
        ;
    });
})

$(document).ready(function() {
    $("#valider").click(function() {

        if ($('#inp_ticket').is(':empty')){
        $('#span_ticket').css('display','none')
        }

        if ($('#inp_ticket').is(':empty')){
        $('#span_ticket').css('display','none')
        }

        if ($('#ticket_num').css({
            'border-color': '#e68585'
        })) {
            $('#ticket_num').css({
                'border-color': 'green'
            });
        }
        ;

    });
})

$("form").on("submit", function() {

    var has_empty = false;

    $(this).find('input[type!="hidden"]').each(function() {

        if (!$(this).val()) {
            has_empty = true;

            $(this).css({
                'border-color': '#e68585'
            });
            $(this).fadeOut(200).fadeIn(200).fadeOut(200).fadeIn(200).fadeOut(200).fadeIn(200).fadeOut(200).fadeIn(200);

        }

    });

    if (has_empty) {
        return false;
    }
    var ticket = $('#inp_ticket').val();
    console.log(ticket)
    if ($("#ticket_num").is(":visible")) {
        if (!ticket.match(/^[A-Z0-9]+$/)) {
            $('#span_ticket').css({
                'display': 'block'
            });

            return false;
        }
    }

});

function changeHandler(val) {
    if ($('#dotation_code').val() == '1250'){
         if (Number(val.value) > 10000) {
            val.value = 10000;
            $('#span_solde').css({
            'display': 'block'
            });
            $('#span_solde').text('Solde limite 10000');
        }if (Number(val.value) < 10000) {
                $('#span_solde').css({
                'display': 'none'
                });
        }
    }if ($('#dotation_code').val() == '1820'){
         if (Number(val.value) > 15000) {
            val.value = 15000
            $('#span_solde').css({
            'display': 'block'
            });
            $('#span_solde').text('Solde limite 15000');
        }if (Number(val.value) < 15000) {
                $('#span_solde').css({
                'display': 'none'
                });
        }
    } else if ($('#dotation_code').val() == '302' || $('#dotation_code').val() == '301' || $('#dotation_code').val() == '303' ){
        if (Number(val.value) > 100000) {
        val.value = 100000
        $('#span_solde').css({
            'display': 'block'
        });
        $('#span_solde').text('Solde limite 100000');
        } if (Number(val.value) < 100000) {
                $('#span_solde').css({
                'display': 'none'
                });
        }
     } if (val.value.length == 0) {
        $('#span_solde').css({
            'display': 'none'
        });
         $('#inp_solde').css({
            'border-color': ''
        });
    }else if (val.value.length > 0) {

         $('#inp_solde').css({
            'border-color': ''
        });
    }
}

function ticketHandler(val) {
    if (val.value.length == 0) {

        $('#span_ticket').css({
            'display': 'none'
        });
    }else if (val.value.length > 0) {
     $('#inp_ticket').css({
            'border-color': ''
        });
    }
     var ticket = $('#inp_ticket').val();
    if ($("#ticket_num").is(":visible")) {
        if ($('#inp_ticket').val().length < 1) {
            $('#inp_ticket').css({
            'border-color': ''
         });
        $('#span_ticket').css({
                'display': 'none'
            });
        }
        else if (!ticket.match(/^[A-Z0-9]+$/)) {
            $('#span_ticket').css({
                'display': 'block'
            });
             $('#inp_ticket').css({
            'border-color': '#e68585'
            });

            return false;
        }else  if (ticket.match(/^[A-Z0-9]+$/)) {
            $('#span_ticket').css({
                'display': 'none'
            });
            $('#inp_ticket').css({
            'border-color': ''
            });

            return false;
      }
    }
}

 $(document).ready(function() {
    $("#retour").click(function() {
//        window.location = "{{ url_for('back_office.listreservation')}}"
        window.location = "/listreservation"

});
})

