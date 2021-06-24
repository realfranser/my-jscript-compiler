python3 src/master.py -f ./tests/test$1.js
echo
echo
echo Prueba 

echo ---------------------------------
echo ---------- codigo ---------------
echo ---------------------------------
cat ./tests/test$1.js
echo ---------------------------------
echo ---------- tokens ---------------
echo ---------------------------------
cat ./tests/output/tokens.txt
echo ---------------------------------
echo ------------ ts -----------------
echo ---------------------------------
cat ./tests/output/ts.txt
echo ---------------------------------
echo ----------- parse ---------------
echo ---------------------------------
cat ./tests/output/parse.txt
echo
echo ---------------------------------
echo ---------- errors ---------------
echo ---------------------------------
cat ./tests/output/errors.txt

