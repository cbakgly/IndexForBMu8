curl -XPUT -H 'Content-Type:application/json;charset=utf-8' --data-binary @./mapping1.txt http://192.168.16.69:9200/tripitaka

for file in `ls data`; do
curl -XPUT -H 'Content-Type:application/json;charset=utf-8' --data-binary @./data/$file http://192.168.16.69:9200/_bulk;
done