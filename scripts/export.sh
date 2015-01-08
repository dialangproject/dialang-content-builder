#!/bin/sh

outputdir="/srv/dialang/"

scala -classpath build/libs/dialang-site-builder-test.jar \
org.dialang.exporter.DialangExporter ${outputdir}
