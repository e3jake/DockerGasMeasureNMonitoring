이 프로젝트는 로봇(스파이더, 드론등등)에 라즈베라이를 연동시키고
라즈베리파이에 공기질 센서를 연결시켜 프로그래밍을 통하여 실시간 차트를 보여준다.

##
## 도커로 필요한 소프트웨어를 설치한다
##

라즈베리파이용 도커를 이용하여 grafana, telegraf, influxdb를 설치한다.
1. 사전 설치 패키지(이미 설치된 패키지는 skip)
> sudo apt-get update
> sudo apt-get upgrade
> sudo apt-get install libffi-dev libssl-dev
> sudo apt-get install python3-dev
> sudo apt-get install -y python3 python-pip

2. 도커등 설치
> sudo apt-get install docker.io docker-compose
> sudo usermod -aG docker userid
> sudo systemctl enabler docker
> docker version 설치확인
> docker-compose version 설치확인

3. 도커 이미지 다운로드 및 설치
> git clone https://github.com/elafargue/rpi-tig.git
> cd rpi-tig
> // docker-compose.yml 파일에 influx-telegraf 연동을 위한 port를 모두 열어준다. 
rpi-docker/docker-compose.yml 참조
----------------------------------------------------------------------------
  ports:
    - "8086:8086"
    - "8083:8083"
    - "8090:8090"
----------------------------------------------------------------------------

3) rpi-tig 폴더 하위에 start.sh를 실행하면 모두 설치됨
4) 도커 설치 확인
# docker ps
pi@raspberrypi:~/gasProject/rpi-docker $ docker ps
CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS              PORTS                                                                    NAMES
8acadd12fbe9        telegraf:latest          "/entrypoint.sh tele…"   17 hours ago        Up 6 hours          8092/udp, 8094/tcp, 0.0.0.0:8125->8125/udp                               telegraf
5b23cafbfa06        grafana/grafana:latest   "/run.sh"                17 hours ago        Up 6 hours          0.0.0.0:3000->3000/tcp                                                   grafana
71dfea3b0ce4        influxdb:1.8.4           "/entrypoint.sh infl…"   17 hours ago        Up 6 hours          0.0.0.0:8083->8083/tcp, 0.0.0.0:8086->8086/tcp, 0.0.0.0:8090->8090/tcp   influxdb

# docker logs influxdb
5) influxdb에 사용자 권한과 데이터베이스에 권한을 설정해준다(인터넷찾아볼것)
   기 설치된 telegraf 데이터베이스에 monitor 사용자를 사용해도 무방함


##
## 2. 테스트 데이터 정상 입력 확인
##

1) gasMeasure/dataSampleTest.sh 파일에 해당 db명과 사용자명을 확인후에 터미널에서 테스트후 정상적으로 입력되는지 확인해본다
curl -X POST 'http://127.0.0.1:8086/write?db=gasdb&u=gasadmin&p=gasadmin' --data-binary "gasdb,host=drone default_m=$d_m
gasdb,host=drone front_m=$random_f
gasdb,host=drone rear_m=$random_r"

db : gasdb
username : gasadmin
password : gasadmin

2) confirm
# docker exec -it influxdb influx -username gasadmin -password gasadmin
Connected to http://localhost:8086 version 1.8.4
InfluxDB shell version: 1.8.4
>use gasdb
>select * from gasdb
데이터 나오면 정상


##
## 3. Grafana 셋팅
##

1) grafana 접속 : http://ipaddress:3000
admin/admin -> 비번변경
2) 데이터소스추가
        1. *->Configuration -> Data source 선택
        2. Add data source 클릭
        3. Name : GASMeasurement
        4. Default check
        5. Type : InfluxDB
        6. Url : http://localhost:8086 --대신--> http://192.168.*.*:8006 으로 해야 통신이 가능할 수 있음
        7. Database : gasdb
        8. User/Passwd : gasadmin/gasadmin
        9. Save&test

3) Create -> Import -> GasMeasureMentatDrone1st.json 선택후 저장하면 기본 화면 나옴
정상적이지 않을경우
Create -> Import -> https://grafana.com/grafana/dashboards/11912 선택후 저장후
판넬을 추가 아래 순서를 추가로 반복설정
        1. Data source : GASMeasurement
        2. Default : gasds
        3. Where host = drone
        4. field(default_m)
        5. Time series
        6. Alias : User
grafanaJson/GasMeasureMentatDrone1st.json

** Data source 에서 라즈베리파이 ip address를 localhost(127.0.0.1) 대신 192.168.*.*로 설정해야 통신이 가능할 수 있음
** telegraf.conf 에서 influxdb url = http://localhost:8086 --> http://192.168.*.*:8086 으로 해서 통신테스트 필요

##
## 4. GPIO 쉘상에서 확인
##

# sudo apt-get update
# sudo apt-get upgrade
# git clone https://github.com/WiringPi/WiringPi.git
# cd WiringPi
# git pull origin
# ./build

gpio -v #version
gpio readall


