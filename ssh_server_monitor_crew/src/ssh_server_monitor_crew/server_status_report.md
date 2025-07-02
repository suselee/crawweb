```markdown
# Server Health Report
Processed 5 server(s).

## Server: dtp
**Status:** Error
  **Details:** An unexpected error occurred in ServerMonitorTool: [Errno None] Unable to connect to port 22708 on 192.168.71.121

## Server: mtp
**Status:** Metrics Collected
- **CPU Usage:** 1
- **Memory:** total: 3954MB, used: 3832MB, free: 121MB, available: 1262MB
- **Disk (Root):** size: 38G, used: 789M, avail: 37G, use_percentage: 3%
- **Network Summary:** N/A
- **Network Error:** bash: ss: command not found
- **Top Processes:**
  ```text
  root 2514 0.5 0.0 /topapp/mtp/c/topwalk/hwinfo_alarm
  root 22557 0.3 45.9 java
  root 1896 0.2 9.5 /usr/local/mysql/bin/mysqld
  root 3312 0.1 0.0 ./redis-server
  root 1 0.0 0.0 /sbin/init
  ```

## Server: pas
**Status:** Metrics Collected
- **CPU Usage:** 4
- **Memory:** total: 15995MB, used: 5453MB, free: 7018MB, available: 10044MB
- **Disk (Root):** size: 9.4G, used: 2.0G, avail: 7.4G, use_percentage: 22%
- **Network Summary:** Total: 271 (kernel 2145)
TCP:   136 (estab 88, closed 14, orphaned 0, synrecv 0, timewait 13/0), ports 0

Transport Total     IP        IPv6
*	  2145      -         -        
RAW	  0         0         0        
UDP	  23        9         14       
TCP	  122       24        98       
INET	  145       33        112      
FRAG	  0         0         0
- **Top Processes:**
  ```text
  root 2567 11.2 0.0 /topwalk/topapp/app_proxy/udp_proxy
  root 20661 4.0 0.0 sshd:
  root 5452 2.7 6.6 java
  root 2673 0.7 0.9 ./fgap-backend
  mysql 17249 0.5 3.4 /opt/mysql/bin/mysqld
  ```

## Server: ias
**Status:** Metrics Collected
- **CPU Usage:** 2
- **Memory:** total: 15995MB, used: 4992MB, free: 7756MB, available: 10385MB
- **Disk (Root):** size: 9.4G, used: 2.0G, avail: 7.4G, use_percentage: 22%
- **Network Summary:** Total: 255 (kernel 1248)
TCP:   117 (estab 76, closed 6, orphaned 0, synrecv 0, timewait 3/0), ports 0

Transport Total     IP        IPv6
*	  1248      -         -        
RAW	  0         0         0        
UDP	  21        7         14       
TCP	  111       21        90       
INET	  132       28        104      
FRAG	  0         0         0
- **Top Processes:**
  ```text
  root 2579 11.0 0.0 /topwalk/topapp/app_proxy/udp_proxy
  root 4751 4.0 0.0 sshd:
  root 5409 2.7 6.5 java
  root 2675 0.6 0.9 ./fgap-backend
  mysql 17926 0.4 3.3 /opt/mysql/bin/mysqld
  ```

## Server: irs
**Status:** Metrics Collected
- **CPU Usage:** 1
- **Memory:** total: 7997MB, used: 3351MB, free: 4646MB, available: 472MB
- **Disk (Root):** size: 29G, used: 2.3G, avail: 26G, use_percentage: 8%
- **Network Summary:** N/A
- **Network Error:** bash: ss: command not found
- **Top Processes:**
  ```text
  root 22851 2.5 0.0 sshd:
  root 2254 2.1 0.1 /topwalk/topapp/rss/app/service/db_server
  mysql 2151 0.5 5.7 /topwalk/baseapp/mysql/bin/mysqld
  root 2340 0.2 4.3 java
  root 1 0.0 0.0 /sbin/init
  ```
```