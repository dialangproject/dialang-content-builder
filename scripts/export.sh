#!/bin/sh

outputdir="/Users/fisha/srv/dialang/"

scala -classpath build/libs/dialang-content-builder.jar \
org.dialang.exporter.DialangExporter ${outputdir}
