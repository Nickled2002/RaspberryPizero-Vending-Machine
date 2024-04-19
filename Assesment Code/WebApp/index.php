<!doctype html>
<html lang="en">
    <head>
    <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- Bootstrap CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztc$
        <link rel="stylesheet" href="maincss.css">
        <!-- MQTT JS -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/paho-mqtt/1.0.2/mqttws31.min.js" type="text/javascript"></script>
        <script>
        clientID = "Cmp408-WebApp";
        host = "44.203.96.38";
        port = 9001;
        userId  = "Cmp408";
        passwordId = "raspberry";
        client = new Paho.MQTT.Client(host,Number(port),clientID);
        client.connect({
        onSuccess: onConnect,
        userName: userId,
        password: passwordId
        });

        function onConnect(){
        document.getElementById("messages").innerHTML += "<span>Online</span>";
        topic =  "instructions";
        client.subscribe(topic);
        };
        function publishMessage1(){
        msg = "dispence 2";
        topic = "instructions";
        Message = new Paho.MQTT.Message(msg);
        Message.destinationName = topic;
        client.send(Message);
        document.getElementById("messages").innerHTML += "<span>, Food Dispencing</span>";
        };

        function publishMessage2(){
        msg = "dispence 3";
        topic = "instructions";
        Message = new Paho.MQTT.Message(msg);
        Message.destinationName = topic;
        client.send(Message);
        document.getElementById("messages").innerHTML += "<span>, Food Dispencing</span>";
        };
        </script>
        
        <title>Cmp408 - IoT Vending Machine</title>
        </head>
        <body>

        <!-- header row -->
        <div id="header1234" class="card text-center">
                <div class="jumbotron text-center" style="background-color:white;margin-bottom:0;">
                        <div style="text-align: left;"><img src="Logo.jpg" width="250" alt="Not yet done" /></div>
                        <div class="card-img-overlay">
                        <h1 class="card-title">Cmp408 - IoT Vending Machine</h1>
                        <h2 class="card-title">Vending Machine orders</h2>
                        </div>
                        </div>
                </div>
        </div>
        <br/>
        <div class="row">
                <div class="col-lg-2 col-md-2 col-sm-2">
                </div>
                <!-- Display items -->
                <div class="col-lg-4 col-md-4 col-sm-4">
                        <div class="card">
                        <div class="card-header">Chocolate Bar</div>
                        <div class="card-block">
                        <p>Description: 100gram chocolate bar made from coco beans</p>
                        <p>Price: £3</p>
                        </div>
                        <div class="card-footer">
                        <input type="button" onclick="publishMessage1()" class="btn btn-primary" value="Dispence">
                        </div>
                        </div>
                </div>
                <div class="col-lg-4 col-md-4 col-sm-4">
                        <div class="card">
                        <div class="card-header">Crisp Bag</div>
                        <div class="card-block">
                        <p>Description: 100gram packet of crisps  made from potatoes</p> 
                        <p>Price: £4</p>
                        </div>
                        <div class="card-footer">
                        <input type="button" onclick="publishMessage2()" class="btn btn-primary" value="Dispence">
                        </div>
                        </div>
                </div>
        </div>
        <br/>
        <br/>
        <div class="row">
                <div id="messages">Status: </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfA$
       </body>
</html>