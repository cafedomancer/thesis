file=`gshuf -n 1 data/targets.txt`
jq ".body" < $file
echo "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
python3 markdown.py $file
echo "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
ruby markdown.rb $file
