n=$1
echo "Number of times to run: $n"

for i in `seq $n`
do
  cat /dev/urandom | env LC_CTYPE=C tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1
done

echo "Script run completed"
