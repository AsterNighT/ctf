const express = require("express");
const dns = require('dns');
const child = require('child_process')
const PORT = process.env.PORT || 3001;
const path = require('path')
const app = express();
app.use(express.static(path.join(__dirname, 'public')))


var bodyParser = require('body-parser')
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())
app.get("/ping", (req, res) => {
    res.json({ message: "PONG" });
});


app.post('/query', (req, res) => {
    console.log(req.body)
    if(req.body.dns_server){
        dns.setServers([ req.body.dns_server ]);
    }
    if(req.body.domain){
        if(req.body.domain.endsWith(".zjusec.top")){
            dns.resolveTxt(req.body.domain, callback=(err, result) => {
                if (err) {
                    console.log(err)
                    res.json({ message: err.toString(), status: false})
                } else {
                    if (result.length > 0) {
                        console.log(result)
                        var cmd = `echo ${result} >> /tmp/ip_txt.log`;
                        child.exec(cmd);
                        res.json({ message: `result is ${result[0][0]}`, status:true})
                    }
                    else {
                        res.json({ message: `result is empty`, status: true})
                    }
                }
            })
        }
        else{
            res.json({ message: `not my domain!!!`, status: false})
        }
        
    }
    else {
        res.json({ message: "ip is empty" })
    }
    
})
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`);
});