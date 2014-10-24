#!/bin/bash

# Lets start with the network interfaces
sudo mv interfaces /etc/network/interfaces

# Then the DHCP server
sudo apt-get install isc-dhcp-server
sudo mv dhcpd.conf /etc/dhcp/dhcpd.conf
sudo mv isc-dhcp-server /etc/default/isc-dhcp-server
sudo service isc-dhcp-server restart

# Now the WiFi broadcast stuff
sudo apt-get install hostapd
# Replace default binary to allow the rtl871xdrv driver for the Edimax USB dongle
wget http://www.adafruit.com/downloads/adafruit_hostapd.zip
unzip adafruit_hostapd.zip
sudo mv /usr/sbin/hostapd /usr/sbin/hostapd.ORIG
sudo mv hostapd /usr/sbin
sudo chmod 755 /usr/sbin/hostapd
sudo chown root:root /usr/sbin/hostapd

sudo mv hostapd.conf /etc/hostapd/hostapd.conf
sudo mv hostapd /etc/default/hostapd

# Finally, reboot
sudo reboot
