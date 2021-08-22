#!/bin/bash

function insert_db()
{
d_m=700
random_f="$((RANDOM% 21+690))"
random_r="$((RANDOM% 21+690))"
echo "front $random_f rear $random_r Press [CTRL+C] to stop.."

####
#curl -X POST 'http://localhost:8086/write?db=telegraf' --data-binary "telegraf,host=drone default_m=$d_m
#curl -X POST 'http://192.168.35.245:8086/write?db=telegraf' --data-binary "telegraf,host=drone default_m=$d_m
#curl -X POST 'http://localhost:8086/write?db=telegraf' --data-urlencode "-password 9AvamVRQ5Wfi9vKvpzynZT1WDXrCJL" --data-urlencode "-username monitor" --data-binary "gasdb,host=drone default_m=$d_m
#curl -X POST 'http://localhost:8086/write?db=gasdb' --data-binary 'gasdb,host=drone default_m=700
#gasdb,host=drone front_m=734
#gasdb,host=drone rear_m=731'
####

curl -X POST 'http://127.0.0.1:8086/write?db=gasdb&u=gasadmin&p=gasadmin' --data-binary "gasdb,host=drone default_m=$d_m
gasdb,host=drone front_m=$random_f
gasdb,host=drone rear_m=$random_r"

}


while :
do
insert_db
sleep 1
done

