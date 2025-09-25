# === setup-quant.ps1 ===
Write-Host "=== Quant Project Setup & Verification ===`n"

$projectPath = "$PWD"
$envPath = "$projectPath\quant\Scripts\python.exe"

# === 1️⃣ Check Python virtual environment ===
if (Test-Path $envPath) {
    Write-Host "Python environment found ✅"
    $pythonVersion = & $envPath --version 2>&1
    Write-Host "Python version:" $pythonVersion
} else {
    Write-Host "No Python environment found ❌"
    Write-Host "Creating virtual environment..."
    python -m venv "$projectPath\quant"
    Write-Host "✅ Environment created"
}

# === 2️⃣ Activate virtual environment ===
Write-Host "`nActivating virtual environment..."
& "$projectPath\quant\Scripts\Activate.ps1"

# === 3️⃣ Install missing packages from requirements.txt ===
$reqFile = "$projectPath\requirements.txt"
if (Test-Path $reqFile) {
    Write-Host "`nInstalling packages from requirements.txt..."
    & $envPath -m pip install --upgrade pip
    & $envPath -m pip install -r $reqFile
    Write-Host "✅ Packages installed/upgraded"
} else {
    Write-Host "No requirements.txt found ❌"
}

# === 4️⃣ Verify VS Code interpreter ===
$settingsFile = "$projectPath\.vscode\settings.json"
if (Test-Path $settingsFile) {
    $settings = Get-Content $settingsFile -Raw
    if ($settings -match "quant") {
        Write-Host "`nVS Code interpreter already set to 'quant' ✅"
    } else {
        Write-Host "`nVS Code interpreter not set to 'quant', updating..."
        if (-not (Test-Path "$projectPath\.vscode")) { New-Item -ItemType Directory "$projectPath\.vscode" }
        $json = @{ "python.pythonPath" = "$projectPath\quant\Scripts\python.exe" } | ConvertTo-Json
        Set-Content -Path $settingsFile -Value $json
        Write-Host "✅ VS Code interpreter updated"
    }
} else {
    Write-Host "`nVS Code settings.json not found, creating..."
    if (-not (Test-Path "$projectPath\.vscode")) { New-Item -ItemType Directory "$projectPath\.vscode" }
    $json = @{ "python.pythonPath" = "$projectPath\quant\Scripts\python.exe" } | ConvertTo-Json
    Set-Content -Path $settingsFile -Value $json
    Write-Host "✅ VS Code interpreter created"
}

Write-Host "`n✅ Quant environment is active, all packages installed, VS Code linked!"
Write-Host "(quant) should appear in your terminal if activation succeeded"
