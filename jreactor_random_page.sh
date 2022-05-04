#!/bin/bash
#&>/dev/null
rm ./image/*
rm ./image/gif/*
rm ./image/last/*
rm ./pre_image/*
rm ./pre_image/gif/*

#функция отрезающая вотермарк реактора (нижние 15 пикселей)
function cut15 () {
	size=$(wc -c $1 | awk '{print $1}')
	x=$(identify $1 | awk '{print $4}' | awk -Fx '{print $2}' | awk -F+ '{print $1}')
	z=$(identify $1 | awk '{print $4}' | awk -Fx '{print $1}')
	y=$(( $x - 15 ))
	filename=$(echo $1 | awk -F/ '{print $3}')
	if [ $size -gt 5242880 ]
	then
		mv ./preimage/$filename ./pre_image/to_big$filename
	else
		convert $1 -crop ${z}x${y}+0+0 image/$filename
	fi
	}

function cut15gif () {
	x=$(identify $1 | head -n1 | awk '{print $4}' | awk -Fx '{print $2}' | awk -F+ '{print $1}')
	z=$(identify $1 | head -n1 | awk '{print $4}' | awk -Fx '{print $1}')
	y=$(( $x - 15 ))
	filename=$(echo $1 | awk -F/ '{print $4}')
	convert $1 -coalesce -repage 0x0 -crop ${z}x${y}+0+0 +repage image/gif/$filename
	}


page=$(shuf -i 10-66695 -n 1)
curl joyreactor.cc/all/$page | grep -oP '<img\ssrc="http:\/\/img\d+.joyreactor.cc\/pics\/post\/\S+?(?=")' | sed -e 's/<//g; s/\/>//g; s/img src=//g; s/"//g' > url_list.temp
count=0
prefix=A
for var in $(cat url_list.temp)
	do
	ifgif=$(echo ${var:$((${#var}-3)):3})
	gif='gif'
	if [ $ifgif = $gif ]
	then
		
		curl $var > pre_image/gif/$prefix-$count.gif
	else
		if [ $count -gt 9 ] && [ $count -lt 20 ]
		then
			prefix=B
		elif [ $count -gt 19 ] && [ $count -lt 30 ]
		then
			prefix=C
		elif [ $count -gt 29 ] && [ $count -lt 40 ]
		then
			prefix=D
		elif [ $count -gt 39 ] && [ $count -lt 50 ]
                then
                        prefix=E
		elif [ $count -gt 49 ] && [ $count -lt 60 ]
		then
			prefix=F
		elif [ $count -gt 59 ] && [ $count -lt 70 ]
		then
			prefix=G
		fi
		count=$(( $count + 1 ))
		curl $var > pre_image/$prefix-$count.jpeg
	fi
done

file_list=$(find ./pre_image -maxdepth 1 -type f)
for row in $file_list
	do
	cut15 $row
done
gif_list=$(find ./pre_image/gif -maxdepth 1 -type f)
if [ "$gif_list" ]
then
	for row in $gif_list
	do
	cut15gif $row 
	done
fi
echo $count
