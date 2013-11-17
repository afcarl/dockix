# Dockix = Docker + Napix

```
docker build -t napix .
docker run -p 8002:8002 -v $(pwd):/napix/auto -v /var/run:/hvr -t -i napix
```
