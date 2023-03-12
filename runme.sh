#!/bin/bash

# Run the app
uvicorn main:app --reload --port 3001  --log-level debug
