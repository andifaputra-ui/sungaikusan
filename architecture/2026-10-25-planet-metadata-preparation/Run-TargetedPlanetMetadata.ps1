$ErrorActionPreference = 'Stop'
$taskSecret = Read-Host 'Existing Planet API key (hidden; not saved; never send it in chat)' -AsSecureString
$taskPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($taskSecret)
$taskPriorKey = $env:PL_API_KEY
try {
    $env:PL_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($taskPointer)
    & 'E:/Bendungan_Kusan/Miniforge/envs/kusan-c1/python.exe' -X utf8 "$PSScriptRoot/query_targeted_metadata.py"
    if ($LASTEXITCODE -ne 0) { throw 'Metadata worker stopped. Inspect its sanitized STATUS.json; no automatic retry.' }
} finally {
    $env:PL_API_KEY = $taskPriorKey
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($taskPointer)
    $taskSecret.Dispose()
    Remove-Variable taskPriorKey, taskSecret, taskPointer -ErrorAction SilentlyContinue
}
