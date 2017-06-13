for i in {1..10000}; do
  echo Test$i; 
  python3.5 get_test.py 10 30 $i > sometest$i;
  python3.5 g.py < sometest$i;
done;
