#########################################################################
# File Name: script.sh
# Author: ma6174
# mail: ma6174@163.com
# Created Time: 2019年12月12日 星期四 13时26分30秒
#########################################################################
#!/bin/bash

for file in $(ls ./oracle/*.mv)
do
	echo $file
	python3 ./parse_code.py ./oracle_data $file
done

for file in $(ls ./stdlib/*.mv)
do
	echo $file
	python3 ./parse_code.py ./oracle_data $file
done

for file in $(ls ./currencies/*.mv)
do
	echo $file
	python3 ./parse_code.py ./oracle_data $file
done
