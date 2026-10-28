#!/bin/bash

ENV_FILE=.env.supplier1 uv run uvicorn main:app --port 8001 &
ENV_FILE=.env.supplier2 uv run uvicorn main:app --port 8002 &
ENV_FILE=.env.supplier3 uv run uvicorn main:app --port 8003 &

wait