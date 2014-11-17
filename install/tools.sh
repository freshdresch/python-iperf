#! /bin/bash
## install iperf (version 2)
echo $1 | sudo -S sudo DEBIAN_FRONTEND=noninteractive apt-get -y install iperf

## install and configure iperf3
tar zxf iperf.tar.gz
cd iperf
./configure
make
echo $1 | sudo -S make install
cd ~
cp .bashrc .backup_bashrc
echo -e "## Adding iperf3 library location\nexport LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib:/usr/local/lib/libiperf.so.0\n" > .bashrc
cat .backup_bashrc >> .bashrc
rm .backup_bashrc
