# Server Health Report
Processed 5 server(s).

## Server: dtp
**Status:** Error
  **Details:** SSH Authentication Failed. Check credentials or SSH server configuration.

## Server: mtp
**Status:** Metrics Collected
- **CPU Usage:** 1
- **Memory:** total: 3954MB, used: 3561MB, free: 393MB, available: 985MB
- **Disk (Root):** size: 38G, used: 778M, avail: 37G, use_percentage: 3%
- **Network Summary:** N/A
- **Network Error:** bash: ss: command not found
- **Top Processes:**
  ```text
  root 2514 0.5 0.1 /topapp/mtp/c/topwalk/hwinfo_alarm
  root 22557 0.4 45.2 java
  root 1896 0.2 13.2 /usr/local/mysql/bin/mysqld
  root 3312 0.1 0.1 ./redis-server
  root 1 0.0 0.0 /sbin/init
  ```

## Server: pas
**Status:** Metrics Collected
- **CPU Usage:** 1
- **Memory:** total: 15995MB, used: 5383MB, free: 7519MB, available: 10235MB
- **Disk (Root):** size: 9.4G, used: 2.0G, avail: 7.4G, use_percentage: 22%
- **Network Summary:** Total: 262 (kernel 1742)
TCP:   128 (estab 79, closed 15, orphaned 0, synrecv 0, timewait 14/0), ports 0

Transport Total     IP        IPv6
*	  1742      -         -        
RAW	  0         0         0        
UDP	  23        9         14       
TCP	  113       23        90       
INET	  136       32        104      
FRAG	  0         0         0
- **Top Processes:**
  ```text
  root 2567 6.3 0.0 /topwalk/topapp/app_proxy/udp_proxy
  root 20511 2.0 0.0 sshd:
  root 5452 1.5 6.6 java
  root 2673 0.6 0.9 ./fgap-backend
  mysql 17249 0.3 3.3 /opt/mysql/bin/mysqld
  ```

## Server: ias
**Status:** Metrics Collected
- **CPU Usage:** 2
- **Memory:** total: 15995MB, used: 4962MB, free: 8361MB, available: 10583MB
- **Disk (Root):** size: 9.4G, used: 2.0G, avail: 7.4G, use_percentage: 22%
- **Network Summary:** Total: 256 (kernel 1092)
TCP:   119 (estab 77, closed 7, orphaned 0, synrecv 0, timewait 4/0), ports 0

Transport Total     IP        IPv6
*	  1092      -         -        
RAW	  0         0         0        
UDP	  21        7         14       
TCP	  112       22        90       
INET	  133       29        104      
FRAG	  0         0         0
- **Top Processes:**
  ```text
  root 2579 6.2 0.0 /topwalk/topapp/app_proxy/udp_proxy
  root 5409 1.5 6.5 java
  root 6090 1.5 0.0 sshd:
  root 2675 0.5 0.9 ./fgap-backend
  mysql 17926 0.3 3.3 /opt/mysql/bin/mysqld
  ```

## Server: irs
**Status:** Metrics Collected
- **CPU Usage:** 1
- **Memory:** total: 7997MB, used: 3285MB, free: 4711MB, available: 478MB
- **Disk (Root):** size: 29G, used: 2.3G, avail: 26G, use_percentage: 8%
- **Network Summary:** N/A
- **Network Error:** bash: ss: command not found
- **Top Processes:**
  ```text
  root 2254 2.1 0.1 /topwalk/topapp/rss/app/service/db_server
  root 31376 2.0 0.0 sshd:
  mysql 2151 0.5 5.5 /topwalk/baseapp/mysql/bin/mysqld
  root 2340 0.2 4.3 java
  root 2265 0.1 2.0 java
  ```
