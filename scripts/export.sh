#!/bin/sh

outputdir="/Users/fisha/git/dialang/dialang-web/dialang-content/"

scala -classpath build/libs/dialang-site-builder.jar\
:/Users/fisha/.m2/repository/org/fusesource/scalate/scalate-core_2.10/1.6.1/scalate-core_2.10-1.6.1.jar\
:/Users/fisha/.m2/repository/org/fusesource/scalate/scalate-util_2.10/1.6.1/scalate-util_2.10-1.6.1.jar\
:/Users/fisha/.m2/repository/org/slf4j/slf4j-api/1.6.4/slf4j-api-1.6.4.jar\
:/Users/fisha/.m2/repository/postgresql/postgresql/9.1-901.jdbc4/postgresql-9.1-901.jdbc4.jar\
:/Users/fisha/.m2/repository/org/dialang/common/dialang-common/0.1/dialang-common-0.1.jar \
org.dialang.exporter.DialangExporter ${outputdir}
