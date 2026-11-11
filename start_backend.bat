@echo off
title Tomato Leaf Disease Identification - Spring Boot & Spring AI Backend
echo ====================================================================
echo Starting Spring Boot 3 Backend with Spring AI & MySQL Database
echo URL: http://localhost:8080
echo ====================================================================

set MAVEN_CMD=C:\Users\kovvu\.maven\maven-3.9.15\bin\mvn.cmd
if not exist "%MAVEN_CMD%" set MAVEN_CMD=mvn

cd /d "%~dp0backend"
call "%MAVEN_CMD%" spring-boot:run
pause
