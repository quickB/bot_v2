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
#надо потом переделать чтоб чистил после ответа пользователю. но для дебага пусть остаются
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
		convert $1 -crop ${z}x${y}+0+0 image/doc/$filename
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

#берём рандомную страницу. пока руками написана последняя. надо дописать чтоб сам номер доставал
page=$(shuf -i 10-66960 -n 1)

#запросы тут просто сохраняют в временный файл ссылки на контент из постов (пока это фото и гиф)
curl joyreactor.cc/all/$page | grep -oP '<img\ssrc="http:\/\/img\d+.joyreactor.cc\/pics\/post\/\S+?(?=")' | sed -e 's/<//g; s/\/>//g; s/img src=//g; s/"//g' > url_list.temp

#счетчики картинок и гифок для нумерации файлов
count=0
gif_count=0

#картинки в итоге распихиваются по альбомам. в один альбом влезает только 10 изображений
#тут у меня сохранённые картинки именуются по правилу:
#префикс-счетчик
#не помню почему такую схему выбрал
#файлы с префиксом А пойдут в перый альбом, с префиксом В во второй, с С в третий и так далее
#соответственно с каждым десятком файлов префикс меняется
#вообще мне не нравится и очень громоздко, надо переделать на числа и циклом, а не вот это вот всё
#пока поддерживается только 70 картинок, хотя попадались страницы где было больше 120. переделаю позже
prefix=A
for var in $(cat url_list.temp)
	do
	#тут гифки сохраняются в отделюную папку и в альбомы не попадают
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

#срезаем 15 пикселей со скаченных картинок, если они есть
file_list=$(find ./pre_image -maxdepth 1 -type f)
for row in $file_list
	do
	cut15 $row
done

#срезаем 15 пикселей с гифок, если они есть
gif_list=$(find ./pre_image/gif -maxdepth 1 -type f)
if [ "$gif_list" ]
then
	for row in $gif_list
	do
	cut15gif $row 
	done
fi

#возвращаем счетчик картинок
echo $count
