sudo cp homecam-client.service /lib/systemd/system/
sudo mkdir /usr/bin/homecam-client
sudo cp homecam-client.sh /usr/bin/homecam-client/

sudo systemctl start homecam-client

sudo systemctl enable homecam-client
