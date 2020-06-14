for file in *.py
do
	#echo $file out-$fil
echo $file
cyclus $file --flat-schema -o out-$file-.sqlite
done

