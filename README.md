JSON-wrap
=========

Simple tool to wrap it's input into JSON.

This is useful for feeding output of tools that to elasticsearch, e.g. Django's *migrate* command which you might execute as part of your service.

Usage
-----

```bash
# default output
$ uptime
22:17:17 up  1:20,  5 users,  load average: 0,49, 0,67, 0,96

# wrapped output
$ uptime | json-wrap service_name=my-service
{"@timestamp": "2018-09-07T22:17:43.938647", "msg": " 22:17:43 up  1:20,  5 users,  load average: 0,50, 0,65, 0,95", "service_name": "my-service"}

# continuos wrapping (line by line)
$ dmesg -w | json-wrap -l
…
{"@timestamp": "2018-09-07T22:20:51.643386", "msg": "[   42.282042] IPv6: ADDRCONF(NETDEV_CHANGE): wlp4s0: link becomes ready"}
{"@timestamp": "2018-09-07T22:20:51.643412", "msg": "[ 1023.755875] tun: Universal TUN/TAP device driver, 1.6"}
{"@timestamp": "2018-09-07T22:20:51.643435", "msg": "[ 1023.909441] alg: No test for echainiv(authenc(hmac(sha1),cbc(des3_ede))) (echainiv(authenc(hmac(sha1-generic),cbc(des3_ede-generic))))"}
…

# also wrap/capture stderr
# this is utilising a shell-feature, so there's no way to determine for json-wrap what is from stdout or sterr (which would be nice to change the loglevel)
uptime 2>&1 | json-wrap

```


Options
-------

### -l

Read the input line-by-line. For long-running processes. If this is your application, the better way would probably to be to fix the logging of your service.

### additional_fields

To add additional fields to the JSON-objects (e.g. your service-name, loglevel etc.), add a list of key-values pairs (separated by equal-signs).

