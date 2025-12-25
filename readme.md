# Измерения:

nginx.conf:

В /etc/nginx/nginx.conf для кэша:

```
http {

        ##
        # Basic Settings
        ##
        proxy_cache_path /home/alex/Education/VK/WEB/QuestionProject/nginx_cache levels=1  keys_zone=question_zone:10m inactive=24h max_size=50m;
        sendfile on;
```

# Отдача статического документа напрямую через nginx

```
(.venv) alex@alex-Redmi-Book-14-2024:~/Education/VK/WEB/QuestionProject$ ab -c 200 -n 2000 http://ogloblina.localhost/static/admin/css/base.css

Server Software:        nginx/1.18.0
Server Hostname:        ogloblina.localhost
Server Port:            80

Document Path:          /static/admin/css/base.css
Document Length:        22120 bytes

Concurrency Level:      200
Time taken for tests:   0.156 seconds
Complete requests:      2000
Failed requests:        0
Total transferred:      44728000 bytes
HTML transferred:       44240000 bytes
Requests per second:    12840.51 [#/sec] (mean)
Time per request:       15.576 [ms] (mean)
Time per request:       0.078 [ms] (mean, across all concurrent requests)
Transfer rate:          280434.83 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    4   1.6      4      12
Processing:     3   10   3.1     10      20
Waiting:        1    4   1.7      4      12
Total:          6   15   3.1     14      24

Percentage of the requests served within a certain time (ms)
  50%     14
  66%     15
  75%     15
  80%     16
  90%     20
  95%     21
  98%     23
  99%     23
 100%     24 (longest request)
```

# Отдача статического документа напрямую через gunicorn

```
(.venv) alex@alex-Redmi-Book-14-2024:~/Education/VK/WEB/QuestionProject$ ab -c 200 -n 2000 http://127.0.0.1:8000/static/admin/css/base.css

Server Software:        gunicorn
Server Hostname:        127.0.0.1
Server Port:            8000

Document Path:          /static/admin/css/base.css
Document Length:        24 bytes

Concurrency Level:      200
Time taken for tests:   1.353 seconds
Complete requests:      2000
Failed requests:        0
Non-2xx responses:      2000
Total transferred:      622000 bytes
HTML transferred:       48000 bytes
Requests per second:    1477.81 [#/sec] (mean)
Time per request:       135.335 [ms] (mean)
Time per request:       0.677 [ms] (mean, across all concurrent requests)
Transfer rate:          448.83 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   1.0      0       5
Processing:     2  111  21.1    108     193
Waiting:        2  111  21.1    107     188
Total:          7  111  20.7    108     193

Percentage of the requests served within a certain time (ms)
  50%    108
  66%    118
  75%    121
  80%    122
  90%    129
  95%    150
  98%    166
  99%    170
 100%    193 (longest request)
```

# Отдача динамического документа напрямую через gunicorn

```
(.venv) alex@alex-Redmi-Book-14-2024:~/Education/VK/WEB/QuestionProject$ ab -c 200 -n 2000 http://127.0.0.1:8000/questions/

Server Software:        gunicorn
Server Hostname:        127.0.0.1
Server Port:            8000

Document Path:          /questions/
Document Length:        22871 bytes

Concurrency Level:      200
Time taken for tests:   52.785 seconds
Complete requests:      2000
Failed requests:        0
Total transferred:      46336000 bytes
HTML transferred:       45742000 bytes
Requests per second:    37.89 [#/sec] (mean)
Time per request:       5278.461 [ms] (mean)
Time per request:       26.392 [ms] (mean, across all concurrent requests)
Transfer rate:          857.26 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   1.2      0       5
Processing:    50 4988 929.1   5171    5734
Waiting:       49 4988 929.1   5170    5734
Total:         55 4989 928.0   5171    5734

Percentage of the requests served within a certain time (ms)
  50%   5171
  66%   5310
  75%   5397
  80%   5423
  90%   5588
  95%   5673
  98%   5705
  99%   5720
 100%   5734 (longest request)
```

# Отдача динамического документа через проксирование запроса с nginx на gunicorn

```
(.venv) alex@alex-Redmi-Book-14-2024:~/Education/VK/WEB/QuestionProject$ ab -c 200 -n 2000 http://ogloblina.localhost/questions/ 

Server Software:        nginx/1.18.0
Server Hostname:        ogloblina.localhost
Server Port:            80

Document Path:          /questions/
Document Length:        22871 bytes

Concurrency Level:      200
Time taken for tests:   51.564 seconds
Complete requests:      2000
Failed requests:        1
   (Connect: 0, Receive: 0, Length: 1, Exceptions: 0)
Non-2xx responses:      1
Total transferred:      46339146 bytes
HTML transferred:       45719295 bytes
Requests per second:    38.79 [#/sec] (mean)
Time per request:       5156.352 [ms] (mean)
Time per request:       25.782 [ms] (mean, across all concurrent requests)
Transfer rate:          877.62 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   1.6      0      10
Processing:     0 4898 925.8   5047    5844
Waiting:        0 4898 925.9   5047    5844
Total:          0 4899 924.3   5047    5844

Percentage of the requests served within a certain time (ms)
  50%   5047
  66%   5137
  75%   5227
  80%   5273
  90%   5432
  95%   5639
  98%   5732
  99%   5825
 100%   5844 (longest request)
```

# Отдача динамического документа через проксирование запроса с nginx на gunicorn, при кэшировние ответа на nginx (proxy cache)

До этого были проведены измерения с кэшом. Теперь результаты для проксирования nginx на gunicorn без кэша.

```
(.venv) alex@alex-Redmi-Book-14-2024:~/Education/VK/WEB/QuestionProject$ ab -c 200 -n 2000 http://ogloblina.localhost/questions/ 

Server Software:        nginx/1.18.0
Server Hostname:        ogloblina.localhost
Server Port:            80

Document Path:          /questions/
Document Length:        22871 bytes

Concurrency Level:      200
Time taken for tests:   56.394 seconds
Complete requests:      2000
Failed requests:        0
Total transferred:      46362000 bytes
HTML transferred:       45742000 bytes
Requests per second:    35.46 [#/sec] (mean)
Time per request:       5639.447 [ms] (mean)
Time per request:       28.197 [ms] (mean, across all concurrent requests)
Transfer rate:          802.83 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   1.3      0       6
Processing:    59 5359 1040.2   5617    6180
Waiting:       59 5359 1040.3   5617    6180
Total:         64 5359 1039.1   5617    6180

Percentage of the requests served within a certain time (ms)
  50%   5617
  66%   5760
  75%   5839
  80%   5908
  90%   5985
  95%   6052
  98%   6129
  99%   6139
 100%   6180 (longest request)
```