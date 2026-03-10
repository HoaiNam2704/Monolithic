$base = "c:\namProj1\bookstore-microservice"
$svcs = @(
    @("staff-service", "staff_service"),
    @("manager-service", "manager_service"),
    @("catalog-service", "catalog_service"),
    @("order-service", "order_service"),
    @("ship-service", "ship_service"),
    @("pay-service", "pay_service"),
    @("comment-rate-service", "comment_rate_service"),
    @("recommender-ai-service", "recommender_ai_service")
)
foreach ($s in $svcs) {
    $svc = $s[0]; $dj = $s[1]
    $py = "$base\$svc\venv\Scripts\python.exe"
    $manage = "$base\$svc\$dj\manage.py"
    Write-Host "=== $svc ===" -ForegroundColor Cyan
    & $py $manage makemigrations app
    & $py $manage migrate
    $db = Test-Path "$base\$svc\$dj\db.sqlite3"
    Write-Host "DB created: $db" -ForegroundColor $(if ($db) {"Green"} else {"Red"})
}
Write-Host "ALL MIGRATIONS DONE" -ForegroundColor Green
