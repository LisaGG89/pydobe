// Launch node server
function SetupConnection() {
    var http = require('http');
    var hostname = '127.0.0.1';
    var port = 2000;

    function handleConnection(req, res){
        res.statusCode = 200;
        if(req.method == "GET"){
            // ping
            res.setHeader('Content-Type', 'text/plain');
            res.end('AfterEffects is alive');
        }
        if(req.method == "POST"){
            // download all body data (req only get header)
            var data = []
            req.on('data', function(chunk){
                data.push(chunk)
            })
            req.on('end', function(){
                // when everything is downloaded, send it to extend script, sending back the response
                var parsed_data = JSON.parse(data);
                console.log("\nExtendScript code to be executed :")
                console.log(parsed_data["to_eval"]);
                var cs = new CSInterface;
                cs.evalScript(parsed_data["to_eval"], function(extendScript_return){
                    console.log("ExtendScript sent back :")
                    console.log(extendScript_return);
                    // html response
                    res.setHeader('Content-Type', 'text/plain');
                    res.end(extendScript_return);
                });
            })
        }
    }

    var server = http.createServer(handleConnection);

    server.listen(port, hostname, function(){
      console.log('Server running at http://' + String(hostname) + ':' + String(port));
    });
}