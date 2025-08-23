path="benyehuda_epub"
# count all *.epub files recursively and do it every 0.5 seconds
while true; do find $path -type f -name "*.epub" | wc -l; sleep 0.5; done