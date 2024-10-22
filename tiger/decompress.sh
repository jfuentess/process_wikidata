i=0
for file in *.zip
do
    i=$(( i + 1 ))
    
    echo "decompressing $file ($i)"
    
    len=${#file}
    len=$(( len - 4)) ## avoiding '.zip'

    file_name=${file:0:$len}

    echo $tmp

    unzip $file $file_name.shp
    unzip $file $file_name.dbf
done

echo $i
