
cmd `iptables` 
```
# Enable access on IP ranges from 172.16.1.1 to 172.16.1.10 for Port 11211 ##
iptables -A INPUT -p tcp --destination-port 11211 -m state --state NEW  -m iprange --src-range 172.16.1.1-172.16.1.10 -j ACCEPT
iptables -A INPUT -p udp --destination-port 11211 -m state --state NEW  -m iprange --src-range 172.16.1.1-172.16.1.10 -j ACCEPT

service iptables restart
```
