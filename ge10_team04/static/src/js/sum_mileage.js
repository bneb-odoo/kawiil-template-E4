odoo.define('ge10_team04', ['web.ajax'], function(require, factory) {

    'use strict';
    var ajax = require('web.ajax');

    $(document).ready(function (){
        var container = document.getElementById("mileage_sum");

        if (container) {
            container.innerHTML = "";
            container.innerHTML = "<div class='col text-center'>Cargando</div>"

            ajax.jsonRpc('/mileage_sum', 'call', {}).then(function(data){
                container.innerHTML = "<div class='col text-center'>"+data+"</div>";
                    
            });
        }
    });
    
}); 
