curl -XPUT -H 'Content-Type:application/json;charset=utf-8' --data-binary @./mappings.txt http://192.168.16.69:9200/tripitaka

for file in `ls data`; do
curl -XPUT -H 'Content-Type:application/json;charset=utf-8' --data-binary @./data/$file http://192.168.16.69:9200/_bulk;
done


while read line; do 
curl -XPOST -H 'Content-Type:application/json;charset=utf-8' http://192.168.16.69:9200/tripitaka/suggest -d "
{
\"candidate\": \"$line\",
\"search_count\": 0
}"; 
done < terms-with-english.txt