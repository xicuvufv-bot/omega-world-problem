# Build the production engine stack on Windows (NVIDIA CUDA).
#
# Prereqs: Git for Windows, Visual Studio 2019+ (Desktop C++), CUDA Toolkit
# (10.1 = BitCrack baseline; 10.2 = Kangaroo; any newer 11.x/12.x works for
# both with the modern .sln/.vcxproj). Run from the lab root as:
#
#   powershell -ExecutionPolicy Bypass -File build\build_windows.ps1
#
# Outputs land in production\bin\ as cuBitCrack.exe and kangaroo.exe, which
# production.manager resolves automatically.

$ErrorActionPreference = "Continue"
$root = Split-Path -Parent $PSScriptRoot
$src  = Join-Path $root "build\src"
$bin  = Join-Path $root "production\bin"
# Native DLLs are found by hash160_ffi / secp256k1_ffi / kangaroo_ffi at the
# LAB ROOT bin/ (dirname(dirname(package_dir))), NOT production\bin -- see
# hash160_ffi.py.
$labRoot = Split-Path -Parent $root
$dllBin  = Join-Path $labRoot "bin"
New-Item -ItemType Directory -Force -Path $src | Out-Null
New-Item -ItemType Directory -Force -Path $bin | Out-Null

function Invoke-GitClone([string]$url, [string]$dir) {
    if (Test-Path (Join-Path $dir ".git")) {
        Write-Host "[skip] $dir already cloned"
        return
    }
    Write-Host "[clone] $url"
    git clone --recursive $url $dir
}

# ---- 0. Beast-Mode native DLLs (no CUDA, self-contained C) -----------------
# hash160.dll + secp256k1.dll. Skips cleanly if either already exists or if
# no MSVC toolchain is present (the GPU engines below need it anyway).
$vcvars = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat"
if (-not (Test-Path $vcvars)) {
    $vcvars = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build\vcvarsall.bat"
}
$nativePairs = @(
    @{ src = "hash160.c";            dll = "hash160.dll" }
    @{ src = "secp256k1_engine.c";   dll = "secp256k1.dll" }
    @{ src = "kangaroo_engine.c";    dll = "kangaroo.dll" }
)
if (Test-Path $vcvars) {
    foreach ($pair in $nativePairs) {
        $srcFile = Join-Path $root "native\$($pair.src)"
        $dllFile = Join-Path $dllBin $pair.dll
        if (Test-Path $dllFile) {
            Write-Host "[skip] $($pair.dll) present"
            continue
        }
        Write-Host "[build] $($pair.dll)  ($($pair.src))"
        cmd /c "call `"$vcvars`" x64 >nul && cl /nologo /O2 /LD `"$srcFile`" /Fe:`"$dllFile`""
        if (Test-Path $dllFile) { Write-Host "[ok]   $($pair.dll)" }
        else { Write-Host "[FAIL] $($pair.dll)" }
    }
} else {
    Write-Host "[warn] MSVC BuildTools not found at $vcvars"
    Write-Host "       Beast Mode DLLs (hash160.dll, secp256k1.dll,"
    Write-Host "       kangaroo.dll) NOT built."
    Write-Host "       The production.manager needs them for the native paths."
}
Write-Host ""

# ---- 1. BitCrack (brichard19) -------------------------------------------
Invoke-GitClone "https://github.com/brichard19/BitCrack.git" (Join-Path $src "BitCrack")

# ---- 2. Kangaroo (JeanLucPons) ------------------------------------------
Invoke-GitClone "https://github.com/JeanLucPons/Kangaroo.git" (Join-Path $src "Kangaroo")

Write-Host ""
Write-Host "Sources ready under build\src\."
Write-Host ""
Write-Host "=== BitCrack build ==="
Write-Host "  1) Open build\src\BitCrack\BitCrack.sln in Visual Studio"
Write-Host "     (if the CUDA version differs, retarget the project:"
Write-Host "      Project -> Properties -> CUDA C/C++ -> Device -> change to your"
Write-Host "      installed toolkit; or edit the .vcxproj CUDA version tags)."
Write-Host "  2) Build 'cuKeyFinder' Release, x64."
Write-Host "  3) Copy cuKeyFinder.exe (or BitCrack.exe / cuBitCrack.exe) to:"
Write-Host "     $bin"
Write-Host ""
Write-Host "=== Kangaroo build ==="
Write-Host "  1) Open build\src\Kangaroo\VC_CUDA102\Kangaroo.sln in VS"
Write-Host "     (retarget CUDA to your installed toolkit if needed)."
Write-Host "  2) Build Release, x64."
Write-Host "  3) Copy kangaroo.exe to:"
Write-Host "     $bin"
Write-Host ""
Write-Host "Alternative: use the sp-hash/Bitcrack fork (sm_80/sm_86 PTX) for"
Write-Host "RTX 30xx/40xx GPUs - build the same way from that repo."
Write-Host ""
Write-Host "Alternative engines (see README): RCKangaroo (RetiredCoder) for"
Write-Host "125-bit+-class kangaroo work, theCollider for pool scanning."