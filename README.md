###
# inventedAttack.py - A POC attack combining IP SPoofing, SYN Flood and IP Fragmentation
##
I only made this to feed my own curiosity (and for a classroom homework too tbh) since it's not very effective nowadays, but feel free to use it!

To use it run

pip install -r requirements.txt 

to install the required dependencies

./inventedAttack.py <Target IP> <Target port> 

tun run the attack


David Carracedo Martinez - dcarracedom@uoc.edu 2019

I actually tried it on some machines and it had 0 impact, probably because
the base of the attack (SYN Flood) was effective when resources were scarcer 
and the was no SYN Flood protection builtin in the kernel.
If you want to play around the idea anyways take a look at

/proc/sys/net/ipv4/tcp_syncookies

/proc/sys/net/ipv4/tcp_max_syn_backlog

/proc/sys/net/ipv4/tcp_synack_retries

If you want to monitor the half-open connections on the server you can try

netstat -tuna | grep :443 | grep SYN_RECV

Change 443 for whatever port you are using, also you can pipe again | wc -l to count the number of connections made, in my tests they stay in the range of 50-100.

The fragmentation part makes no difference either.

About the source IP spoofing I found it was the most effective part since 
the web server was making DNS PTR requests for each random source IP, so it
kind flooded the DNS with them. 

Lessons learned : turn off reverse DNS resolution in your services. 

