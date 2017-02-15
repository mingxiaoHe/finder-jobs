    var map = new AMap.Map("mapContainer", {
        resizeEnable: true,
        zoom: 13
    });

        $.getJSON('/api/jobs',function(data){ 
            var i, len, job, ref;
                ref = data["items"];

            var infoWindow = new AMap.InfoWindow({offset:new AMap.Pixel(0,-30)});
            for(var i=0,marker,len=ref.length;i<len;i++){
                    job=ref[i];
                    var marker=new AMap.Marker({
                        position:[job["longitude"], job["latitude"]],
                        map:map
                    });
                marker.content='<p>职位：' + job["positionName"] + '<br/> 公司：' + job["companyShortName"] + '<br/> 资金: ' + job["financeStage"] + '<br/> 地址: ' + job["address"] + '<br/> 待遇: ' + job["salary"] + " <br/> 来源：<a href='http://www.lagou.com/jobs/" + job["positionId"] + ".html'>拉勾网</a> </p>";
                marker.on('click',markerClick);
                marker.emit('click',{target:marker});
            }
            function markerClick(e){
                infoWindow.setContent(e.target.content);
                infoWindow.open(map, e.target.getPosition());
            }
            map.setFitView();

        }); 
