# bot_v2
(aiogram) telegram bot for joyreactor (aiogram)<br>
<br>
(ru)<br>
парсит реактор и кидает картинки в телеграм<br>
сейчас функций всего две<br>
-) по команде /Random парсит рандомную страницу сайта и возвращает картинки и гифки из постов<br>
-) текст сообщения пользователя берётся как тэг и также парсит картинки и гифки<br>
<br>
всё в стадии альфа-версии и нестабильно<br>
все файлы предварительно скачиваются<br>
<br>
тут будет что-то вроде чендж лога)<br>
17.05.22<br>
авторизацию я пока не победил. но позже к ней вернусь. нужна она для формирования ленты. до сих пор сомневаюсь что нужна<br>
этот проект тестовый и никому не нужен кроме меня. сейчас я изучаю докер, так что позже запихну это творение в контейнер<br>
<br>
только для личного пользования (потому что иначе он не работает)<br>
код самый простой. много что переделать надо<br>
-------------требования-------------<br>
для работы нужен Linux (часть скриптов на bash) <br>
файл в корне config.py в котором прописан токен бота, полученный от @BotFather строкой вида:<br>
TOKEN = '1122334455:XXYYZZxxxyyyyzzz-yourToken'<br>
<br>
ImageMagick.x86_64   (у меня версия 6.9.10.68-6.el7_9)<br>
python не ниже 3.7 <br>
библиотеки<br>
aiogram==2.20<br>
aiohttp==3.8.1<br>
aiosignal==1.2.0<br>
async-timeout==4.0.2<br>
attrs==21.4.0<br>
Babel==2.9.1<br>
certifi==2021.10.8<br>
charset-normalizer==2.0.12<br>
emoji==1.7.0<br>
frozenlist==1.3.0<br>
idna==3.3<br>
multidict==6.0.2<br>
natsort==8.1.0<br>
pytz==2022.1<br>
yarl==1.7.2<br>
