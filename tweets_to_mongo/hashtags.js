var map = function() {
    var ht_list = this.entities.hashtags;
    if (ht_list.length>0) { 
        for(var i = 0; i < ht_list.length; i++){
           var hasht = ht_list[i].text;
            hasht = hasht.toLowerCase();
            emit({"ht":hasht}, this.sentimiento);
        }
    }
};

var reduce = function( key, values ) {    
    var pos = 0;
    var neg = 0;
    var neu = 0;  
    values.forEach(function(v) {            
        if(v=="positive"){
            pos++;
        }               
        else if(v=="negative"){
            neg++;
        }             
        else if(v=="neutral"){
            neu++;
        }  
    });
    return {"pos":pos,"neg":neg,"neu":neu};
}

db.getCollection('tweets').mapReduce(map, reduce, {out: "ht_sentimientos"})