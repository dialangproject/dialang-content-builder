#!/bin/sh

rm -rf website/dialang/content/*

scala -classpath target/scala-2.10/classes\
:lib_managed/bundles/org.fusesource.scalate/scalate-core_2.10/*\
:lib_managed/bundles/org.fusesource.scalate/scalate-util_2.10/*\
:lib_managed/jars/org.slf4j/slf4j-api/*\
:lib/postgresql-9.1-901.jdbc4.jar \
org.dialang.exporter.DialangExporter

cd website/dialang

tar -czf ../../target/content.tar.gz *
