#!/bin/bash
#&>/dev/null

#создаём каталоги, если их нет
image_folder='image'
if [ ! -d "$image_folder" ]
then
        mkdir $image_folder
fi
gif_folder='image/gif'
if [ ! -d "$gif_folder" ]
then
        mkdir $gif_folder
fi
last_file_folder='image/last'
if [ ! -d "$last_file_folder" ]
then
        mkdir $last_file_folder
fi
pre_image_folder='pre_image'
if [ ! -d "$pre_image_folder" ]
then
        mkdir $pre_image_folder
fi
pre_image_gif_folder='pre_image/gif'
if [ ! -d "$pre_image_gif_folder" ]
then
        mkdir $pre_image_gif_folder
fi
as_doc_folder='image/doc'
if [ ! -d "$as_doc_folder" ]
then
        mkdir $as_doc_folder
fi


#удаляем картинки с прошлого запроса
rm ./image/*
rm ./image/gif/*
rm ./image/last/*
rm ./image/doc/*
rm ./pre_image/*
rm ./pre_image/gif/*

#функция отрезающая вотермарк реактора (нижние 15 пикселей)
function cut15 () {
	#size=$(identify $1 | awk '{print $7}' | sed -e 's/B//g s/K//g s/M//g' )
	size=$(wc -c $1 | awk '{print $1}')
	x=$(identify $1 | awk '{print $4}' | awk -Fx '{print $2}' | awk -F+ '{print $1}')
	z=$(identify $1 | awk '{print $4}' | awk -Fx '{print $1}')
	y=$(( $x - 15 ))
	filename=$(echo $1 | awk -F/ '{print $3}')
	if [ $size -gt 5242880 ]
	then
		convert $1 -crop ${z}x${y}+0+0 image/doc/$filename
		#mv ./pre_image/$filename ./pre_image/to_big$filename
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


#тут делаем проверку на наличие переадресации на поддомен
joy_domain='joyreactor.cc'

request_tag_domain=$(curl joyreactor.cc/tag/$1/new | grep -o "http-equiv=\"refresh\"")
tag_domain='joyreactor.cc'

if [ "$request_tag_domain" ]
then
        tag_domain=$(curl $joy_domain/tag/$1/new | grep -Po "http:.*?(?=\")" | awk -F/ '{print $3}')
	joy_domain='reactor.cc'
fi

last_page=$(curl $tag_domain/tag/$1/new | grep -Po "current'>\d+" | sed "s/current'>//")

page=1
if [ $last_page -gt 0 ]
then
	page=$(shuf -i 1-$last_page -n 1)
fi

if [ "$request_tag_domain" ]
then
	curl $tag_domain/tag/$1/new/$page | grep -oP 'http:\/\/img\d+.reactor.cc\/pics\/post\/full\/\S+?(?=")' | sed -e 's/<//g; s/\/>//g; s/img src=//g; s/"//g' > url_list.temp
else
	curl $tag_domain/tag/$1/new/$page | grep -oP '<img\ssrc="http:\/\/img\d+.joyreactor.cc\/pics\/post\/\S+?(?=")' | sed -e 's/<//g; s/\/>//g; s/img src=//g; s/"//g' > url_list.temp
fi

count=0
gif_count=0
prefix=A
for var in $(cat url_list.temp)
	do
	ifgif=$(echo ${var:$((${#var}-3)):3})
	gif='gif'
	if [ $ifgif = $gif ]
	then
		gif_count=$(( $gif_count + 1 ))
		curl $var > pre_image/gif/$prefix-$gif_count.gif
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
if [ "file_list" ]
then
	for row in $file_list
	do
	cut15 $row
	done
fi

gif_list=$(find ./pre_image/gif -maxdepth 1 -type f)
if [ "$gif_list" ]
then
	for row in $gif_list
	do
	cut15gif $row 
	done
fi

echo $count
