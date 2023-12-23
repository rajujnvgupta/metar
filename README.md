dependency

developed in ubuntu 20.04 environment

python  v=3.8
django  v=4.2.5
Redis server v=5.0.7
REDIS_IP = 127.0.0.1
REDIS_PORT = 6379


django is running on port 8000

# curl request pong pong test
curl --location --request GET 'http://127.0.0.1:8000/metar/ping'
# curl request without nocache
curl --location --request GET 'http://127.0.0.1:8000/metar/info?scode=AAXX'
payload = { scode : AAXX } 
# curl request with nocache
curl --location --request GET 'http://127.0.0.1:8000/metar/info?scode=AAXX&nocache=1'
payload = { scode : "AAXX", nocache : 1 } 




