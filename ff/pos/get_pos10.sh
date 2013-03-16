#/bin/bash
python writepomdp.py;
cp ff_pos10.pomdpx ../../src
cd ../../src
./pomdpsol  --output pos10.policy ff_pos10.pomdpx 
