#!/usr/bin/env bash

# Returns 1 when Time Machine is performing backup,
# otherwise returns 0.

tmutil status | grep "Running" | sed 's/    Running = \([01]\);/\1/'
