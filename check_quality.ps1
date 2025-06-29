# CraftX.py Code Quality Report Generator
# Usage: .\check_quality.ps1

Write-Host ""
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "   CraftX.py Code Quality Report" -ForegroundColor Yellow
Write-Host "   Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "📊 OVERALL PROJECT SCORE:" -ForegroundColor Yellow
Write-Host "----------------------------" -ForegroundColor Gray
$scoreOutput = pylint scripts\migrate_storage.py craftxpy\memory\storage.py craftxpy\plugins\tools\large_storage_manager.py craftxpy\plugins\tools\file_hydration.py examples\large_storage_demo.py examples\storage_demo.py --score=yes --output-format=text 2>&1 | Select-String "Your code has been rated"
Write-Host $scoreOutput -ForegroundColor Green
Write-Host ""

Write-Host "🚨 REMAINING ISSUES BY FILE:" -ForegroundColor Red
Write-Host "-----------------------------" -ForegroundColor Gray

$files = @(
    @{Name = "scripts\migrate_storage.py"; Display = "📄 scripts\migrate_storage.py:" },
    @{Name = "craftxpy\memory\storage.py"; Display = "📄 craftxpy\memory\storage.py:" },
    @{Name = "craftxpy\plugins\tools\large_storage_manager.py"; Display = "📄 craftxpy\plugins\tools\large_storage_manager.py:" },
    @{Name = "craftxpy\plugins\tools\file_hydration.py"; Display = "📄 craftxpy\plugins\tools\file_hydration.py:" },
    @{Name = "examples\large_storage_demo.py"; Display = "📄 examples\large_storage_demo.py:" },
    @{Name = "examples\storage_demo.py"; Display = "📄 examples\storage_demo.py:" }
)

foreach ($file in $files) {
    Write-Host ""
    Write-Host $file.Display -ForegroundColor Magenta
    $issues = pylint $file.Name --output-format=text 2>&1 | Where-Object { $_ -match ":\d+:\d+:" }
    if ($issues) {
        foreach ($issue in $issues) {
            Write-Host "  $issue" -ForegroundColor White
        }
    }
    else {
        Write-Host "  ✅ No issues found!" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "📈 SUMMARY BY ISSUE TYPE:" -ForegroundColor Yellow
Write-Host "-------------------------" -ForegroundColor Gray

# Count issues by type
$allIssues = pylint scripts\migrate_storage.py craftxpy\memory\storage.py craftxpy\plugins\tools\large_storage_manager.py craftxpy\plugins\tools\file_hydration.py examples\large_storage_demo.py examples\storage_demo.py --output-format=text 2>&1 | Where-Object { $_ -match ":\d+:\d+:" }

$criticalCount = ($allIssues | Where-Object { $_ -match "C0\d{3}" }).Count
$refactorCount = ($allIssues | Where-Object { $_ -match "R0\d{3}" }).Count
$warningCount = ($allIssues | Where-Object { $_ -match "W0\d{3}" }).Count
$errorCount = ($allIssues | Where-Object { $_ -match "E0\d{3}" }).Count

Write-Host "  🔴 Critical Issues (C0xxx): $criticalCount" -ForegroundColor Red
Write-Host "  🟡 Refactor Issues (R0xxx): $refactorCount" -ForegroundColor Yellow  
Write-Host "  🟠 Warning Issues (W0xxx): $warningCount" -ForegroundColor DarkYellow
Write-Host "  ⚫ Error Issues (E0xxx): $errorCount" -ForegroundColor DarkRed

Write-Host ""
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "   Report Complete - Total Issues: $($allIssues.Count)" -ForegroundColor Yellow
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""
