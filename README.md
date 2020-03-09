# GOEASY Platform

GOEASY project is aimed at developing a platfom with integrated physical, internet-connected devices so that applications and services running on-board devices can access the Trusted GOEASY platform via the open GOEASY APIs, which allow access to core GOEASY services such as the end-to-end authentication of position information, the trusted measurement and exchange of position information, dependable LBS or privacy-aware Data Base Management systems (DBMS).

In order to provide its services, the core GOEASY enabled devices and platform depends naturally on GNSS services. Moreover, GOEASY is externally supported by third-party services federated with the platform, Cloud-based applications, beyond interacting directly with devices with GOEASY components on-board, can also access GOEASY services via the open GOEASY application API. Major barrier to the diffusion of such services is associated with privacy and e-security concerns of users, who are (or at least, should be) rightfully worried in sharing their precise location with unknown service providers, which may make unknown uses of such information. For this reason, the main component of the platform is the GOEASY e-security infrastructure which guarantees end-to-end position authentication, and is tightly integrated with identity and privacy services such as the privacy aware DBMS, which stores the data provided by the users in a secure way, also providing selective, controlled access and anonymization services.

Implementation was done using microservice architecture using Python programming language, NGINX, and PostgreSQL.


## Prerequisites

In order to run GOEASY platform, you need to have the modules listed in [`requirements.txt`](https://github.com/sisayie/goeasy-platform/blob/master/application/requirements.txt) installed or build docker image or simply pull the docker image from dockerHub.

## Installing

### Building Image using Docker
GOEASY Platform is easy to install and deploy in a Docker container. By default, the Docker will expose port 5003, so change this within the docker-compose if necessary. When ready, simply use the docker-compose to build the image.

```
cd goeasy-platform
docker-compose up --build
```
This will create the goeasy-platform image and pull in the necessary dependencies. 

Once done, run the Docker image and map the port to whatever you wish on your host. In this example, we simply map port 5003 of the host to port 5003 of the Docker (or whatever port was exposed in the Dockerfile):

```
docker run -d -p 5003:5003 --restart="always" goeasy/gep_anonengine
```

Verify the deployment by navigating to your server address in your preferred browser.

```
127.0.0.1:5003
```

### Pulling Image from Docker Registry

You can also directly pull (and run) goeasy-platform from image registry using 

```
docker pull goeasy/gep_web:latest && docker pull goeasy/gep_anonengine:latest
```

## Running the tests

You can run CRUD operations on the database as follows:

#### GET

```
curl -X GET "https://localhost:5003/GEP/paib/publicstorage" -H "accept: application/json"
```

#### POST
curl -X POST "https://localhost:5003/GEP/paib/publicstorage" -H "accept: application/json" -H "Content-Type: application/json" -d '
     ```{
        "deviceId": 123445,
        "sessionID": 456789,
        "sourceApp": "ApesMobility",  
        "positions": [
            {"lat":43.4541819, 
		"lon":11.8679015, 
		"time":1570390750300, 
		"authenticity": 1
		},
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
    }``` '

#### PUT

https://localhost:5003/GEP/paib/publicstorage/{id}

## Authors

See the list of [contributors](https://github.com/sisayie/goeasy-platform/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details

## More on the GOEASY Project

### Project Website

https://goeasyproject.eu/

### Project Youtube Channel
https://www.youtube.com/channel/UCZHD8RBdWRYcEYckCx7mVBw

### Project LinkedIn Page
https://www.linkedin.com/company/goeasyproject/