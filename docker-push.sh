#! /usr/bin/env bash
docker build -t base -f Dockerfile.base .
docker tag base isaccchoi/base
docker push isacchoi/base
