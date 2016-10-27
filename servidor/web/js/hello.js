$(document).ready(function() {
    lista = []
    objeto_consulta1 = {}

     url_get = "http://localhost:8080/consulta1"
        console.log(url_get)
        $.ajax({
        type: "GET",
        url: url_get
        }).then(function(data) {
            var data_json = JSON.parse(data)
            console.log("data: ")
            console.log(data_json)
            lista = data_json.lista
            objeto_consulta1 = data_json.objeto
        $.each(lista, function (i, item) {
            $('#selector').append($('<option>', { 
                value: item,
                text : item 
            }));
        });
    });

    $( "#selector" )
    .change(function () {
    var str = "";
    $( "select option:selected" ).each(function() {
      str += $( this ).text() + " ";
    });
    str = str.replace(/\s/g, '');
    $( "#resultado_text" ).text( JSON.stringify(objeto_consulta1[str]) );
  })
  .change();

    $("#Get").click(function(){
        console.log(objeto_consulta1)
    });

    $("#Suma").click(function(){
        console.log("Suma")
        var A = $('#txt_A').val();
        var B = $('#txt_B').val();
        console.log("A " + A)
        console.log("B " + B)
        url_post = "http://localhost:5000/api/suma"
	var jsonData = "{\"A\":\""+A+"\",\"B\":\""+B+"\"}";
        console.log(url_post)
        console.log("JSON: "+jsonData)
        $.ajax({
	type: "POST",
  	data: jsonData,
    	contentType: "application/json; charset=utf-8",
  	dataType: "json",
        url: url_post
        }).then(function(data) {
            console.log("data: " + data)
	    console.log("data " + data.marca)
       $('#resultado_text').text(data);
    });
    });
});