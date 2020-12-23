# Quick Cmd


### 导入
`
# 编码转换
iconv -f UTF16LE -t UTF8 -o file_utf.csv file.csv
# 去掉boom
sed -i '1s/^\xEF\xBB\xBF//'  file_utf.csv

# 导入tab分割、无指定quote的文件
copy test_table from program 'sed ''s/\\/\\\\/g'' < /var/lib/pgsql/file_utf.csv' with (format csv, delimiter E'\t', quote '\');
`