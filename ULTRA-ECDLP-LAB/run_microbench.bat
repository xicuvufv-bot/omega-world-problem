@echo off
setlocal
set L=c:\ProgramData\mingw64\mingw64\bin
rem runner: build micro_main with several flag sets and save CSV
"%L%\g++.exe" -O2      -std=c++17 -I. -o micro_O2.exe      src\micro_main.cpp
micro_O2.exe      > MICROBENCH_O2.csv
"%L%\g++.exe" -O3      -std=c++17 -I. -o micro_O3.exe      src\micro_main.cpp
micro_O3.exe      > MICROBENCH_O3.csv
"%L%\g++.exe" -Ofast   -std=c++17 -I. -o micro_Ofast.exe   src\micro_main.cpp
micro_Ofast.exe   > MICROBENCH_Ofast.csv
"%L%\g++.exe" -O3 -march=native -std=c++17 -I. -o micro_native.exe src\micro_main.cpp
micro_native.exe  > MICROBENCH_native.csv
echo done