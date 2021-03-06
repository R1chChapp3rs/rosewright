python config_watch.py -sa -S || exit
./waf build || exit
mv build/rosewright.pbw build/rosewright_a.pbw

python config_watch.py -sa || exit
./waf build || exit
mv build/rosewright.pbw build/rosewright_as.pbw

python config_watch.py -sb -S || exit
./waf build || exit
mv build/rosewright.pbw build/rosewright_b.pbw

python config_watch.py -sb || exit
./waf build || exit
mv build/rosewright.pbw build/rosewright_bs.pbw

python config_watch.py -sb -b || exit
./waf build || exit
mv build/rosewright.pbw build/rosewright_bsb.pbw

python config_watch.py -sc || exit
./waf build || exit
mv build/rosewright.pbw build/rosewright_c1.pbw

python config_watch.py -sc -c || exit
./waf build || exit
mv build/rosewright.pbw build/rosewright_c2.pbw
