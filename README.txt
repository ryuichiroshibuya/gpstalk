1.execTalk.sh:shell ver open_jtalk wapper
2.getGPS.py:open_jtalk wapper module
3.getGPSTalk.py:python ver open_jtalk wapper
4.jsay:open_jtalk wapper
5.setGPS.sh: create sql shell

example1:
pi@rasp01:~/work/bin/gpstalk$ ./execTalk.sh
+ . /home/pi/.bash_profile
++ date +%Y%m%d%H%M
+ DATE=201403180116
+++ dirname ./execTalk.sh
++ cd .
++ pwd
+ BASE=/home/pi/work/bin/gpstalk
+ SQLFILE=logs/sample_201403180116.sql
+ cd /home/pi/work/bin/gpstalk
++ python getGPS.py
+ ./setGPS.sh 139.xxxxx 35.xxxxxx
++ psql -At pgis
++ cat logs/sample_201403180116.sql
+ ./jsay $'\347\217\276\345\234\250\343\201\'

example2:
pi@rasp01:~/work/bin/gpstalk$ ./getGPSTalk.py
139.xxxxx 35.xxxx

Killing Thread...
現在の住所は東京都足立区xxxxxxxx地付近です
