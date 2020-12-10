python3 rec.py -f pruebasDraco/pp.txt
echo
echo
echo Prueba 
echo begin{verbatim}
echo ---------------------------------
echo ---------- codigo ---------------
echo ---------------------------------
cat pruebasDraco/pp.txt
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
