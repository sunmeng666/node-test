var http = require("http");

http.createServer(function(request,response){
    response.writeHead(200,{'Content-Type':'text/plain'});
    response.end('hello world lalalal');
}).listen(8888)

console.log('Server running at http://127.0.0.1:8888')

function test(){
    return 111
}

module.exports = {
    test
}