#!/bin/sh

outputdir="/Users/fisha/srv/dialang/"

scala -classpath build/libs/dialang-site-builder.jar \
org.dialang.exporter.DialangExporter ${outputdir}
