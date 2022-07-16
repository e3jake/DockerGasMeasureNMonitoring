이 프로젝트는 라즈베리파이에 공기질 센서를 연결시켜 프로그래밍을 통하여 실시간 차트를 보여준다.
도커환경에 telegraf-influxdb-grafana를 구성한다

#
# 1. 도커로 필요한 소프트웨어를 설치한다
#

### 1.1 사전 설치 패키지(이미 설치된 패키지는 skip) 
```
> sudo apt-get update
> sudo apt-get upgrade
> sudo apt-get install libffi-dev libssl-dev
> sudo apt-get install python3-dev
> sudo apt-get install -y python3 python-pip
```

### 1.2 도커등 설치
```
> sudo apt-get install docker.io docker-compose
> sudo usermod -aG docker userid
> sudo systemctl enabler docker
> docker version          # 설치확인
> docker-compose version  # 설치확인
```

### 1.3 도커 이미지 다운로드 및 설치
```
> git clone https://github.com/elafargue/rpi-tig.git
> cd rpi-tig
  docker-compose.yml 파일에 influx-telegraf 연동을 위한 port를 모두 열어준다. 
  rpi-docker/docker-compose.yml 참조
  ----------------------------------------------------------------------------
  ports:
    - "8086:8086"
    - "8083:8083"
    - "8090:8090"
  ----------------------------------------------------------------------------
```

### 1.4 rpi-tig 설치 및 확인
```
> cd ~/rpi-tig
> ./start.sh

> docker ps -a      # 이미지설치확인
> docker ps 도커    # 패키지 실행여부
   pi@raspberrypi:~/gasProject/rpi-docker $ docker ps 시 결과 참조
  ----------------------------------------------------------------------------
   CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS              PORTS                                                                    NAMES
   8acadd12fbe9        telegraf:latest          "/entrypoint.sh tele…"   17 hours ago        Up 6 hours          8092/udp, 8094/tcp, 0.0.0.0:8125->8125/udp                               telegraf
   5b23cafbfa06        grafana/grafana:latest   "/run.sh"                17 hours ago        Up 6 hours          0.0.0.0:3000->3000/tcp                                                   grafana
   71dfea3b0ce4        influxdb:1.8.4           "/entrypoint.sh infl…"   17 hours ago        Up 6 hours          0.0.0.0:8083->8083/tcp, 0.0.0.0:8086->8086/tcp, 0.0.0.0:8090->8090/tcp   influxdb
  ----------------------------------------------------------------------------
> docker logs influxdb   # 로그확인
> docker logs telegraf
> docker logs grafana
```


#
# 2. Influxdb 설정
#

### 2.1 DB구성하기
```
influxdb 접속하기, admin password는 rpi-tig내 env.influxdb 파일에 있음(랜덤생성됨)
> docker exec -it influxdb influx -username admin -password <admin>
> use telegraf
> create database gasdb                     # 데이터베이스 gasdb 생성하기
> create user <username> with password <password> with all privileges     # 사용자 생성 및 권한주기
> grant all on <database> to <username>     # 예시 create user gasadmin with password gasadmin with all privileges
                                            # 예시 grant all on gasadmin to gasadmin
> show databases    # 데이터 베이스 확인하기
> show users        # 생성된 사용자 확인하기
하위에 생성된 데이터베이스 gasdb와 생성된 사용자계정 gasadmin이 보이면 정상
```

### 2.2 telegraf 데이터 확인
```
> docker exec -it influxdb influx -username admin -password <admin>   # influxdb 접속하기
> use telegraf
> select * from cpu limit 10            # 하위에 데이터가 나오면 정상적으로 쌓이고 있음
```

### 2.3 gasdb 데이터 입력하기
```
curl이 없다면 설치
> sudo apt-get install -y curl
> curl --version

DB접속 통신이상유무 확인
> curl -I http://127.0.0.1:8086
정상일 경우 통신결과나 나오고 접속에 이상이 생기면 curl: (7) Failed to connect to localhost port 8086: Connection refused

접속 오류일경우
localhost가 아닌 네트웍 I/F의 IP주소를 입력
> curl -I http://192.168.**.**:8086

샘플 데이터 write 테스트
> curl -X POST 'http://127.0.0.1:8086/write?db=gasdb&u=gasadmin&p=gasadmin' --data-binary "gasdb,host=drone default_m=700 
gasdb,host=drone front_m=1234 
gasdb,host=drone rear_m=5678"

데이터 확인
> docker exec -it influxdb influx -username gasadmin -password gasadmin
> use gasdb
> select * from gasdb 
입력한 데이터가 나오면 정상 write 확인
```

### 2.4 gasdb 데이터 추출 및 입력 프로그램
```
https://github.com/e3jake/GasMeasurementProject/tree/main/gasMeasure/gasMeasure.sh 파일을 참조하여 사용한다

라즈베리파이 구동시 자동으로 해당 파일이 실행토록 설정방법
/etc/rc.local 파일을 수정
....
~~~program pull path/gasMeasure.sh &
exit 0
```

#
# 3. Grafana 셋팅
#

### 3.1 grafana 접속 
```
http://ipaddress:3000 초기  ID/비번   admin/admin -> 비번변경
```

### 3.2 데이터소스 추가
```
        1. *->Configuration -> Data source 선택
        2. Add data source 클릭
        3. Name : GASMeasurement(자유롭게 명명)
        4. Default check
        5. Type : InfluxDB
        6. Url : http://localhost:8086 --대신--> http://192.168.*.*:8006 으로 해야 통신이 가능할 수 있음
        7. Database : gasdb (생성한 데이터베이스 명)
        8. User/Passwd : gasadmin/9AvamVRQ5Wfi9vKvpzynZT1WDXrCJL (사용자계정 접속정보)
        9. Save&test
        테스트시 정상적으로 나오지 않을때는 대부분 url접속이 안되는 경우가 많기 때문에 해당 정보를 정확히 입력하여 테스트할것
        snapshot에 해당 이미지를 참조할것 (https://github.com/e3jake/GasMeasurementProject/tree/main/snapshot)
```

### 3.3 대시보드 추가
```
> Create -> Import -> GasMeasureMentatDrone1st.json  선택후 저장하면 기본 화면 
Json파일 https://github.com/e3jake/GasMeasurementProject/tree/main/grafanaJson 참조
정상적이지 않을경우
Create -> Import -> https://grafana.com/grafana/dashboards/11912 선택후 저장후

판넬을 추가 아래 순서를 추가로 반복설정
        1. Data source : GASMeasurement
        2. Default : gasds
        3. Where host = drone
        4. field(default_m)
        5. Time series
        6. Alias : User
        snapshot에 해당 이미지를 참조할것 (https://github.com/e3jake/GasMeasurementProject/tree/main/snapshot)
```

#
# 4. GPIO 쉘상에서 확인 GPIO값을 쉘스크립트로 활용하기 위한 패키지 설치
#

### 4.1 GPIO 패키지 설치
```
> sudo apt-get update
> sudo apt-get upgrade
> cd ~/
> git clone https://github.com/WiringPi/WiringPi.git
> cd ~/WiringPi
> git pull origin
> ./build
> gpio -v   # 설치확인
> gpio readall
해당 프로그램도 https://github.com/e3jake/GasMeasurementProject/tree/main/gasMeasure/gasMeasure.sh 파일을 참조하여 사용한다
```


