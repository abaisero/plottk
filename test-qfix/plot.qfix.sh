#!/bin/bash

./plot.qfix.smacv2.return-mean.py
./plot.qfix.smacv2.return-mean.aggregate.py
./plot.qfix.smacv2.return-iqm.aggregate.py

./plot.qfix.smacv2.winrate-mean.py
./plot.qfix.smacv2.winrate-mean.aggregate.py
./plot.qfix.smacv2.winrate-iqm.aggregate.py

./plot.qfix.smacv2-ablation.return-mean.py
./plot.qfix.smacv2-ablation.return-mean.aggregate.py
./plot.qfix.smacv2-ablation.return-iqm.aggregate.py

./plot.qfix.smacv2.poi.py

./plot.qfix.overcooked.py
./plot.qfix.overcooked-3.py
