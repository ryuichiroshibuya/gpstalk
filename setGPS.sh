#!/bin/bash

cat  << EOF

SELECT '現在の住所は'||pref_name||city_name||street_name||address||'番地付近です' FROM address WHERE ST_DWithin(geom2,ST_GeomFromText('POINT($1 $2)',4326),1000) ORDER BY ST_Distance(geom2,ST_GeomFromText('POINT($1 $2)',4326)) limit 1;
EOF
