for i in ./tests/??; do
  echo "============== Start Test ${i} ========================="
  cat $i
  echo "========================================================"
  python match.py < $i > temp
  diff temp ${i}.out
  echo "============== Test ${i} done =========================="
done;
