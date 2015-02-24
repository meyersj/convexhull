#!/bin/bash
set -e

stops=tm_stops
park=tm_parkride
tc=tm_tran_cen
url=http://developer.trimet.org/gis/data

function fetch() {
    name=$1
    wget ${url}/${name}.zip
    unzip ${name}.zip
    ogr2ogr -f "GeoJSON" ${name}.json ${name}.shp ${name}
    mv ${name}.json ../ && rm ./*
}

mkdir tmp
cd tmp

fetch ${stops}
fetch ${park}
fetch ${tc}

cd ..
rm -r tmp

