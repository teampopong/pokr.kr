module.load = function(me) {
    if (!me)
        me = 'jaeho.shin';
    neighbors =
        [{weight:1.0, facebookId:'jooddang'}
        ,{weight:0.3, facebookId:'Osing604'}
        ,{weight:0.7, facebookId:'100000136930302'}
        ,{weight:0.9, facebookId:'dmlord'}
        ,{weight:0.8, facebookId:'kyujin.shim'}
        ,{weight:0.4, facebookId:'dgtgrade'}
        ,{weight:0.8, facebookId:'pcpenpal'}
        ,{weight:0.2, facebookId:'1526484720'}
        ,{weight:0.3, facebookId:'1034516089'}
        ,{weight:0.5, facebookId:'galadbran'}
        ,{weight:1.0, facebookId:'cornchz'}
        ];

    module.display("frame.html").then(function(){
        // template with {number} for positional arguments
        String.prototype.format = function() {
            var formatted = this;
            for (var i = 0; i < arguments.length; i++) {
                var regexp = new RegExp('\\{'+i+'\\}', 'gi');
                formatted = formatted.replace(regexp, arguments[i]);
            }
            return formatted;
        };

        var profileTemplate = '<a href="http://www.facebook.com/profile.php?id={0}"><img src="{2}" alt=""><br>{1}</a>';
        function profileImage(facebookId) { return 'http://graph.facebook.com/' + facebookId + '/picture'; }

        // Facebook OAuth
        access_token = null;
        // TODO getcookie access_token = document.cookie;
        if (access_token) {
            loadFriends();
        } else {
            facebookRequestDeferred = $.Deferred();
            if (parent.location.host == "localhost")
                appid = "202877406434480";
            else
                appid = "228986207144654";
            open("https://www.facebook.com/dialog/oauth?client_id="+ appid 
                    +"&redirect_uri="+ escape("http://"+ parent.location.host + parent.location.pathname + module.base +"/facebookReceiver.html")
                    +"&response_type=token");
            facebookRequestDeferred.done(function(response){
                access_token = response.access_token;
                WM.debug("Facebook access_token", access_token);
                // TODO set cookie access_token
                loadFriends();
            });
        }

        // fetch friends from Facebook
        function loadFriends() {
            $.getJSON("https://graph.facebook.com/"+ me +"/friends?limit=10&access_token="+ escape(access_token) +"&callback=?",
                function(data){
                    // import friends
                    var facebookFriends = data.data;
                    WM.debug("Facebook friends of ", me, facebookFriends);
                    neighbors = [];
                    for (var i in facebookFriends) {
                        var f = facebookFriends[i];
                        neighbors.push({
                            name:f.name,
                            facebookId:f.id,
                            weight:Math.random() // FIXME
                        });
                    }
                    // fill page
                    $("#center")
                    .html(profileTemplate.format(me, me, profileImage(me)))
                    .addClass("object");
                    // fill list with neighbors
                    $("#neighbors").html("");
                    for (var i in neighbors) {
                        var neighbor = neighbors[i];
                        $("<li class='object'>")
                        .html(profileTemplate.format(neighbor.facebookId, neighbor.name, profileImage(neighbor.facebookId)))
                        .each(function() { this.info = neighbor; })
                        .appendTo("#neighbors")
                        ;
                    }
                    circularLayout();
                });
        }

        function circularLayout() {
            var frame  = $("#neighbors")[0];
            var center = $("#center")[0];
            var width  = frame.offsetWidth;
            var height = frame.offsetHeight;
            var rW =  width/2 - center.offsetWidth /2;
            var rH = height/2 - center.offsetHeight/2;
            center.style.left = rW +'px';
            center.style.top  = rH +'px';
            var objects = $("#neighbors > li");
            var n = objects.length;
            var i = 0;
            $(objects).each(function(i) {
                var t = i * 2*Math.PI / n - Math.PI/2;
                var w = this.info.weight;
                var x = parseInt(rW + rW * (1-0.4*w) * Math.cos(t));
                var y = parseInt(rH + rH * (1-0.4*w) * Math.sin(t));
                this.style.left = x +'px';
                this.style.top  = y +'px';
                console.log(this.innerText, x, y);
            });

            // lines btwn objects
            function lineColor(w) {
                var lineColorMin = 64;
                var lineColorMax = 255;
                return "rgb({0},{0},{1})".format(parseInt((lineColorMax-lineColorMin)*(1-w)+lineColorMin), lineColorMax, lineColorMin);
            }
            var canvas = $("#background")[0];
            canvas.width = width;
            canvas.height = height;
            if (canvas.getContext) {
                var c = canvas.getContext("2d");
                function updateLines() {
                    canvas.width = width; // reset canvas
                    c.lineCap = c.lineJoin = "round";
                    c.lineWidth = 3;
                    $(objects).each(function(i) {
                        c.beginPath();
                        c.moveTo(center.offsetLeft+center.offsetWidth/2, center.offsetTop+center.offsetHeight/2);
                        c.lineTo(  this.offsetLeft+  this.offsetWidth/2,   this.offsetTop+  this.offsetHeight/2);
                        c.closePath();
                        c.strokeStyle = lineColor(this.info.weight);
                        c.lineWidth = parseInt(1 + 5 * this.info.weight);
                        c.stroke();
                    });
                }
                updateLines();
            }

            // let user drag objects and customize layout
            var dragInfo = null;
            var dragOldE = null;
            var dragUpdateDelay = 50; //ms
            $("#frame")
                .mousemove(function(e) {
                    if (dragInfo && e.timeStamp - dragInfo.e.timeStamp > dragUpdateDelay) {
                        dragInfo.e = e;
                        dragInfo.o.style.left = e.pageX - dragInfo.x +'px';
                        dragInfo.o.style.top  = e.pageY - dragInfo.y +'px';
                        updateLines();
                    }
                });
            $(".object")
                .mousedown(function(e) {
                    dragInfo = {
                        x: e.pageX - this.offsetLeft,
                    y: e.pageY - this.offsetTop,
                    e: e,
                    o: this
                    }
                    this.style.zIndex = 2;
                    $(this).toggleClass("dragging");
                    return false;
                })
                .mouseup(function() {
                    $(this).toggleClass("dragging");
                    this.style.zIndex = null;
                    dragInfo = null;
                });
            }
    });
};
