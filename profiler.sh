#!/bin/bash

script=hulltester.py
kernprof -l ${script}
python -m line_profiler ${script}.lprof
