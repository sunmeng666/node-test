const cheerio = require("cheerio");
const server = require("./src/curl");

const url = "http://v.163.com/special/opencourse/englishs1.html";

server.download(url,function(data){
    if(data){
        const $ = cheerio.load(data);
        $("a.downbtn").each(function(i,e){
            console.log($(e).attr("href"));
        });
    }
})