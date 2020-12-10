python3 rec.py -f pruebasDraco/a.txt
echo
echo
echo Prueba 
echo begin{verbatim}
echo ---------------------------------
echo ---------- codigo ---------------
echo ---------------------------------
cat pruebasDraco/a.txt
echo ---------------------------------
echo ---------- tokens ---------------
echo ---------------------------------
cat output/tokens.txt
echo ---------------------------------
echo ------------ ts -----------------
echo ---------------------------------
cat output/ts.txt
echo ---------------------------------
echo ----------- parse ---------------
echo ---------------------------------
cat output/parse.txt
echo
echo ---------------------------------
echo ---------- errors ---------------
echo ---------------------------------
cat output/errors.txt
echo end{verbatim}
