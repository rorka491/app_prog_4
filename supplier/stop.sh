#!/bin/bash

for port in 8001 8002 8003; do
    pid=$(lsof -ti :"$port")

    if [ -n "$pid" ]; then
        kill $pid
        echo "Stopped supplier on port $port"
    fi
done