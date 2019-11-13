GET:

curl -X GET "https://localhost:5003/anonymizer/publicstorage" -H "accept: application/json"

POST:
curl -X POST "https://localhost:5003/anonymizer/publicstorage" -H "accept: application/json" -H "Content-Type: application/json" -d '{
        "common": { 
            "deviceId": 123445,
            "sessionID": 456789,
            "sourceApp": "ApesMobility"
        },  
        "positions": [
            {"lat":43.4541819, "lon":11.8679015, "time":1570390750300, "authenticity": 1},
            {"lat":43.4541711, "lon":11.8679564, "time":1570390752305, "authenticity": 0},
            {"lat":43.4542047, "lon":11.8679665, "time":1570390757171, "authenticity": 1},
            {"lat":43.4541974, "lon":11.8679352, "time":1570390770173, "authenticity": 1},
            {"lat":43.4541987, "lon":11.8679016, "time":1570390806175, "authenticity": -1},
            {"lat":43.4541867, "lon":11.8679515, "time":1570390812154, "authenticity": -1},
            {"lat":43.4541729, "lon":11.8679809, "time":1570390813172, "authenticity": -1},
            {"lat":43.4541361, "lon":11.8680513, "time":1570390815164, "authenticity": -1},
            {"lat":43.4541128, "lon":11.8680922, "time":1570390816218, "authenticity": -1}
        ],
        "tpv_defined_behaviour":[
            {"start_time":1570390750300, "end_time":1570391081178, "mode": "walk"},
            {"start_time":1570391082220, "end_time":1570391333188, "mode": "drive"}
        ],
        "app_defined_behaviour":[
            {"start_time":1570390750300, "end_time":1570391081178, "mode": "walk"},
            {"start_time":1570391082220, "end_time":1570391333188, "mode": "drive"}
        ],
        "user_defined_behaviour":[
            {"start_time":1570390750300, "end_time":1570391081178, "mode": "walk"},
            {"start_time":1570391082220, "end_time":1570391333188, "mode": "drive"}
        ],
        "sensordata":[
            {"data":5.0,"name":"proximity","time":1570390749231},
            {"data":{"x":-2.0,"y":0.0,"z":8.0},"name":"accellerometer","time":1570390749233},
            {"data":{"x":15.363352,"y":-29.060678,"z":-69.23764},"name":"magnetometer","time":1570390749320},
            {"data":{"x":22.490746,"y":-43.714897,"z":-103.77774},"name":"magnetometer","time":1570390750221},
            {"data":{"x":26.39621,"y":-51.00329,"z":-121.21308},"name":"magnetometer","time":1570390751287},
            {"data":{"x":29.422604,"y":-56.587624,"z":-134.03339},"name":"magnetometer","time":1570390753288},
            {"data":{"x":35.883057,"y":-46.446068,"z":-138.07208},"name":"magnetometer","time":1570390865175},
            {"data":{"x":36.672806,"y":-35.711693,"z":-137.7186},"name":"magnetometer","time":1570390867176},
            {"data":{"x":27.774622,"y":-25.288143,"z":-139.21454},"name":"magnetometer","time":1570390892173}
        ]
    }'
