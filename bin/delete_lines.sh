#!/bin/bash

# Search for patterns like "[3] RadComServer", "[4] RadComServer", and "[5] RadComServer" and remove the line and the next line
sed -e '/\[3\] RadComServer/{N;d;}' -e '/\[4\] RadComServer/{N;d;}' -e '/\[5\] RadComServer/{N;d;}' "$@"

# Path: bin/delete_lines.sh
