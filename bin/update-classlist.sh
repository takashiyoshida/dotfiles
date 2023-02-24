#!/usr/bin/env bash

NELDATA="../../../../src/nel/pkg/neldata"

cp -v classlist_*.txt "${NELDATA}/eqplists"
cp -v dbmuserconst_class*.cfg "${NELDATA}/dbuserdata"
