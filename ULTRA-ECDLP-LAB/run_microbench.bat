@echo off
setlocal
rem Portable microbench runner: uses g++ from PATH (override with GXX).
rem   run_microbench.bat            -> rebuild + rerun all 4 flag sets
rem   GXX=C:\path\to\g++.exe run_microbench.bat
if not defined GXX set GXX=g++
"%GXX%" -O2    -std=c++17 -I. -o micro_O2.exe      src\micro_main.cpp
if errorlevel 1 exit /b 1
micro_O2.exe      > MICROBENCH_O2.csv
"%GXX%" -O3    -std=c++17 -I. -o micro_O3.exe      src\micro_main.cpp
if errorlevel 1 exit /b 1
micro_O3.exe      > MICROBENCH_O3.csv
"%GXX%" -Ofast -std=c++17 -I. -o micro_Ofast.exe   src\micro_main.cpp
if errorlevel 1 exit /b 1
micro_Ofast.exe   > MICROBENCH_Ofast.csv
"%GXX%" -O3 -march=native -std=c++17 -I. -o micro_native.exe src\micro_main.cpp
if errorlevel 1 exit /b 1
micro_native.exe  > MICROBENCH_native.csv
echo done