
  var ticket = document.getElementById('ticket_num');
    var solde = document.getElementById('oc_solde');
    var force = document.getElementById('force');
    var solde_ind = document.getElementById('oc_ind');
    force.onclick = function(){
        if (ticket.style.display !==  "none" && solde.style.display !==  "none"){
            ticket.style.display =  "none";
            solde.style.display =  "none";

        }else{
            ticket.style.display =  "block";
            solde.style.display =  "block";
        }

    };
     $("#ticket_num").hide();
    $("#oc_solde").hide();
    $("#valider").hide();

    {{ url_for('back_office.force_reserve_form',num_id=num_id,type_id=type_id, request_id=request_id,first_name=first_name,last_name=last_name)}}

    {{ url_for('back_office.solde_indisponible_form',num_id=num_id,type_id=type_id,request_id=request_id,first_name=first_name,last_name=last_name)}}