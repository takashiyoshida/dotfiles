#!/usr/bin/env bash

NELDATA="../../../../src/nel/pkg/neldata"
ECSDATA="../../../../src/mcs/ecs/dat"
MXDDATA="../../../../src/mcs/pow/mxd/dat"

(
    cd Database
    cp -v classlist_*.txt "${NELDATA}/eqplists"
    cp -v dbmuserconst_class*.cfg "${NELDATA}/dbuserdata"
)

(
    # C755B-1396: When ECST_ECS.cfg file is updated, we need to update
    # ECST_ECS.cfg file at mcs/ecs/dat.
    # This is because NELdbs environment uses this file for "something".
    cd Archives

    cp -v CMST_POWMXD.cfg "${MXDDATA}/CMST_POWMXD.cfg"
    cp -v ECST_ECS.cfg "${ECSDATA}/ECST_ECS.cfg"
)
