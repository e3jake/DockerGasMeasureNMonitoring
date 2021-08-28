#!/bin/bash

PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

function check_sensor()
{
	d_m=700

	if [ $f_g1 -eq 0 ] && [ $f_g2 -eq 0 ] ; then
		f_m="$((RANDOM% 10))"
	elif [ $f_g1 -eq 0 ] && [ $f_g2 -eq 1 ] ; then
		f_m="$((RANDOM% 11+700))"
	elif [ $f_g1 -eq 1 ] && [ $f_g2 -eq 0 ] ; then
		f_m="$((RANDOM% 100+1500))"
	elif [ $f_g1 -eq 1 ] && [ $f_g2 -eq 1 ] ; then
		f_m="$((RANDOM% 100+2000))"
	else
		return 1
	fi

	if [ $r_g1 -eq 0 ] && [ $r_g2 -eq 0 ] ; then
		r_m="$((RANDOM% 10))"
	elif [ $r_g1 -eq 0 ] && [ $r_g2 -eq 1 ] ; then
		r_m="$((RANDOM% 11+700))"
	elif [ $r_g1 -eq 1 ] && [ $r_g2 -eq 0 ] ; then
		r_m="$((RANDOM% 100+1500))"
	elif [ $r_g1 -eq 1 ] && [ $r_g2 -eq 1 ] ; then
		r_m="$((RANDOM% 100+2000))"
	else
		return 1
	fi
}



function insert_db()
{

	##@echo "$d_m $f_m $r_m"

curl -X POST 'http://127.0.0.1:8086/write?db=gasdb&u=gasadmin&p=gasadmin' --data-binary "gasdb,host=drone default_m=$d_m
gasdb,host=drone front_m=$f_m
gasdb,host=drone rear_m=$r_m"

}


while :
do

# gpio 를 이용한 센서값 읽기
f_g1=`gpio -g read 27`
f_g2=`gpio -g read 22`
r_g1=`gpio -g read 23`
r_g2=`gpio -g read 24`

check_sensor
insert_db
sleep 2

done

