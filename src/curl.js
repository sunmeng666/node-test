const http = require("http");

function download(url,callback){
    http.get(url,function(res){
        const data = "";
        res.on('data',function(chunk){
            data += chunk;
        });

        res.on('end',function(){
            callback(data);
        });
    }).on("error",function(){
        callback(null)
    });
}

exports.download = download;
