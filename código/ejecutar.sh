python3 rec.py -f tests/test.js > tests/debug.txt
echo ---------- tokens ---------------
cat output/tokens.txt
echo ---------------------------------
echo
echo ---------- errors ---------------
cat output/errors.txt
echo ---------------------------------
echo
echo ------------ ts -----------------
cat output/ts.txt
echo ---------------------------------
echo