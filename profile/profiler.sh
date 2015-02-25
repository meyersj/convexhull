#!/bin/bash

script=runner.py
kernprof -l ../src/${script}
python -m line_profiler ${script}.lprof
