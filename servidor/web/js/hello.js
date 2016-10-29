$(document).ready(function() {
    lista = []
    objeto_consulta1 = {}
    objeto_consulta2 = {}
    objeto_consulta3 = {}
    objeto_consulta_seguidores = {}
    objeto_consulta_robots = {}

     url_get_consulta1 = "http://localhost:8080/consulta1"
        $.ajax({
        type: "GET",
        url: url_get_consulta1
        }).then(function(data) {
            var data_json = JSON.parse(data)
            console.log("data: ")
            console.log(data_json)
            lista = data_json.lista
            objeto_consulta1 = data_json.objeto
        $.each(lista, function (i, item) {
            $('#selector_consulta_1').append($('<option>', { 
                value: item,
                text : item 
            }));
        });
    });

    url_get_consulta2 = "http://localhost:8080/consulta2"
        $.ajax({
        type: "GET",
        url: url_get_consulta2
        }).then(function(data) {
            var data_json = JSON.parse(data)
            console.log("data: ")
            console.log(data_json)
            objeto_consulta2 = data_json.objeto
    });

    url_get_consulta3 = "http://localhost:8080/consulta3"
        $.ajax({
        type: "GET",
        url: url_get_consulta3
        }).then(function(data) {
            var data_json = JSON.parse(data)
            console.log("data: ")
            console.log(data_json)
            objeto_consulta3 = data_json.objeto
    });

    url_get_consulta_seguidores = "http://localhost:8080/consulta_seguidores"
        $.ajax({
        type: "GET",
        url: url_get_consulta_seguidores
        }).then(function(data) {
            var data_json = JSON.parse(data)
            console.log("data consulta seguidores: ")
            console.log(data_json)
            objeto_consulta_seguidores = data_json[0]
    });

    url_get_consulta_robots = "http://localhost:8080/consulta_robots"
        $.ajax({
        type: "GET",
        url: url_get_consulta_robots
        }).then(function(data) {
            var data_json = JSON.parse(data)
            console.log("data consulta robots: ")
            console.log(data_json)
            objeto_consulta_robots = data_json[0]
    });

    $( "#selector_consulta_1" )
    .change(function () {
        var str = "";
        $( "select option:selected" ).each(function() {
          str += $( this ).text() + " ";
        });
        str = str.replace(/\s/g, '');
        $( "#titulo_tuitero" ).text( /*JSON.stringify(*/str/*)*/ );
        $( "#resultado_1_consulta_1" ).text( /*JSON.stringify(*/objeto_consulta1[str].promedio_seguidores/*)*/ );
        $( "#resultado_2_consulta_1" ).text( /*JSON.stringify(*/objeto_consulta1[str].promedio_RT/*)*/ );
        $( "#resultado_3_consulta_1" ).text( /*JSON.stringify(*/objeto_consulta1[str].relacion/*)*/ );
        $( "#resultado_1_consulta_2" ).text( /*JSON.stringify(*/objeto_consulta2[str].promedio_tuits/*)*/ );
        $( "#resultado_2_consulta_2" ).text( /*JSON.stringify(*/objeto_consulta2[str].promedio_RT/*)*/ );
        $( "#resultado_3_consulta_2" ).text( /*JSON.stringify(*/objeto_consulta2[str].relacion/*)*/ );
        $( "#resultado_1_consulta_3" ).text( /*JSON.stringify(*/objeto_consulta3[str].promedio_faveado/*)*/ );
        $( "#resultado_2_consulta_3" ).text( /*JSON.stringify(*/objeto_consulta3[str].promedio_favs/*)*/ );
        $( "#resultado_3_consulta_3" ).text( /*JSON.stringify(*/objeto_consulta3[str].relacion/*)*/ );
        $( "#resultado_robots_imagen img" ).remove();
        $( "#resultado_robots_imagen" ).append( /*JSON.stringify(*/"<img src=\""+objeto_consulta_robots[str].imagen+"\">"/*)*/ );
        $( "#resultado_robots_cuenta" ).text( /*JSON.stringify(*/objeto_consulta_robots[str].cuenta/*)*/ );
        $( "#resultado_robots_cantidad" ).text( /*JSON.stringify(*/objeto_consulta_robots[str].num_tweets/*)*/ );
        $( "#resultado_robots_fecha" ).text( /*JSON.stringify(*/objeto_consulta_robots[str].fecha/*)*/ );
        console.log(objeto_consulta_seguidores)
        console.log(objeto_consulta_seguidores[str])
        $('#tabla_resultados tr').not(':first').remove();
        $.each(objeto_consulta_seguidores[str], function (i, item) {
                console.log(item)
                $('#tabla_resultados').append("<tr><td>"+item['fecha']+"</td><td>"+item['tweet']+"</td><td>"+item['retweets']+"</td><td>"+item['seguidores']+"</td><td>"+item['delta']+"</td></tr>");
            });
  })
  .change();

});