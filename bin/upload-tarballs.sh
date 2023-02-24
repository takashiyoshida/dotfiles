#!/usr/bin/env bash

echo "Uploading tarballs to nelarchiver:source..."
scp *.tar.gz nelarchiver:source
echo "Uploading tarballs to nelbuildrhel:source/rpmbuild/SOURCES..."
scp -oKexAlgorithms=diffie-hellman-group1-sha1 *.tar.gz nelbuildrhel:source/rpmbuild/SOURCES
