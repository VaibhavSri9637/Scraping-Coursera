const fs=require("fs")

var freedetails1=JSON.parse(fs.readFileSync('./freedetails1.json'))

var freedetails=JSON.parse(fs.readFileSync('./freedetails.json'))

console.log(freedetails.length,freedetails1.length)
cdscds
for (var i=0;i<freedetails1.length;i++){
    var freedetail1=freedetails1[i];
    if(freedetail1.product_id!="NA"&&freedetail1.type!="NA"&&freedetail1.financial_aid!="NA"&&freedetail1.price!="NA"&&freedetail1.costfree!="NA"){
        var foundindex=freedetails.findIndex(f=>(f.product_id==freedetail1.product_id));
        freedetails[foundindex]=freedetail1;
    }
    else{
        console.log(freedetail1.product_id)
    }
}

fs.writeFile("freedetails.json",JSON.stringify(freedetails),function(err,data){
    if(err){console.log(err);}
})