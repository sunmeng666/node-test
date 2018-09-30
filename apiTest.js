const os = require('os');

const fs = require('fs');

const buf1 = Buffer.alloc(10);

const buf2 = Buffer.alloc(10,1);
//delete
fs.unlink('/tmp/world',(err) => {
    if(err) throw err;
    console.log('successfully deleted /tmp/world');
});

try {
    fs.unlinkSync('/tmp/hello');
    console.log('successfully deleted /tmp/hello');
} catch (err){
    console.log(err);
};

//rename
fs.rename('/tmp/hello','/tmp/world', (err) => {
    if(err) throw err;
    console.log('重命名完成')
});//OK

fs.stat('/tmp/world',(err,stats) => {
    if(err) throw err;
    console.log(`文件属性： ${JSON.stringify(stats)}`)
})

fs.open('/tmp/world/world.txt','r',(err,fd) => {
    if(err) throw err;
    fs.close(fd,(err) => {
        if(err) throw err;
    });
});

fs.utimesSync('/tmp/world',(err,stats) => {
    if(err) throw err;
    console.log();
})

// console.log(os.arch());
// console.log(os.constants);
// console.log(os.cpus());
// console.log(os.hostname());
// console.log(os.networkInterfaces());
// console.log(fs);
console.log(buf1);