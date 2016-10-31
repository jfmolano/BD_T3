var map = function() {
    var ht_list = this.entities.hashtags;
    var user = this.user.screen_name
    if (ht_list.length>0) { 
        for(var i = 0; i < ht_list.length; i++){
           var hasht = ht_list[i].text;
            hasht = hasht.toLowerCase();
            emit({"ht":hasht,"usuario":user}, 1);
        }
    }
};

var reduce = function( key, values ) { 
        var cont = 0
    values.forEach(function(v) {            
        cont += v 
    });
    return cont;
}

db.getCollection('tweets').mapReduce(map, reduce, {out: "ht_lugares"})