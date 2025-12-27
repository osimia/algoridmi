# ========================================
# Mass Problem Generation Script
# ========================================
# Generates problems for all grades (1-12)
# and different difficulty levels

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "MASS PROBLEM GENERATION" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check virtual environment activation
if (-not $env:VIRTUAL_ENV) {
    Write-Host "WARNING: Virtual environment not activated!" -ForegroundColor Yellow
    Write-Host "Activating venv..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
}

# Generation parameters
$problemsPerGrade = 10
$delay = 2.0

# Counters
$totalProblems = 0
$successCount = 0
$errorCount = 0

Write-Host "Generation parameters:" -ForegroundColor Cyan
Write-Host "   - Problems per grade: $problemsPerGrade" -ForegroundColor White
Write-Host "   - Delay: $delay sec" -ForegroundColor White
Write-Host ""

# ========================================
# PART 1: Generation for school grades (1-12)
# ========================================

Write-Host "PART 1: Generating problems for school grades (1-12)" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

for ($grade = 1; $grade -le 12; $grade++) {
    Write-Host "Grade $grade..." -ForegroundColor Yellow
    
    try {
        python manage.py generate_problems_bulk --count $problemsPerGrade --grade $grade --delay $delay
        
        if ($LASTEXITCODE -eq 0) {
            $successCount += $problemsPerGrade
            Write-Host "   [OK] Successfully generated: $problemsPerGrade problems" -ForegroundColor Green
        } else {
            $errorCount += $problemsPerGrade
            Write-Host "   [ERROR] Generation failed for grade $grade" -ForegroundColor Red
        }
    } catch {
        $errorCount += $problemsPerGrade
        Write-Host "   [ERROR] Exception: $_" -ForegroundColor Red
    }
    
    $totalProblems += $problemsPerGrade
    Write-Host ""
}

# ========================================
# PART 2: Generation for difficulty levels
# ========================================

Write-Host "PART 2: Generating problems for difficulty levels" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Define difficulty levels
$difficultyLevels = @(
    @{Name="Beginner"; Min=0; Max=300; Count=10},
    @{Name="Easy"; Min=300; Max=600; Count=10},
    @{Name="Medium"; Min=600; Max=900; Count=10},
    @{Name="Above Average"; Min=900; Max=1200; Count=10},
    @{Name="Hard"; Min=1200; Max=1500; Count=10},
    @{Name="Very Hard"; Min=1500; Max=2000; Count=10},
    @{Name="Expert"; Min=2000; Max=3000; Count=10}
)

foreach ($level in $difficultyLevels) {
    Write-Host "Level: $($level.Name) ($($level.Min)-$($level.Max))" -ForegroundColor Yellow
    
    try {
        python manage.py generate_problems_bulk --count $($level.Count) --difficulty-min $($level.Min) --difficulty-max $($level.Max) --delay $delay
        
        if ($LASTEXITCODE -eq 0) {
            $successCount += $level.Count
            Write-Host "   [OK] Successfully generated: $($level.Count) problems" -ForegroundColor Green
        } else {
            $errorCount += $level.Count
            Write-Host "   [ERROR] Generation failed for level $($level.Name)" -ForegroundColor Red
        }
    } catch {
        $errorCount += $level.Count
        Write-Host "   [ERROR] Exception: $_" -ForegroundColor Red
    }
    
    $totalProblems += $level.Count
    Write-Host ""
}

# ========================================
# FINAL STATISTICS
# ========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GENERATION COMPLETED!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Statistics:" -ForegroundColor Cyan
Write-Host "   - Total problems planned: $totalProblems" -ForegroundColor White
Write-Host "   - Successfully generated: $successCount" -ForegroundColor Green
Write-Host "   - Errors: $errorCount" -ForegroundColor Red
Write-Host ""

# Check total problems in DB
Write-Host "Checking database..." -ForegroundColor Cyan
python manage.py shell -c "from problems.models import Problem; print(f'Total problems in DB: {Problem.objects.count()}')"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Done!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
