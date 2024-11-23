$TaskName = "Trends24 Scraper"
$ScriptPath = "C:\AI_Content_App\Datavbase_conf\trends24_scraper.py"
$PythonPath = "C:\Users\darre\AppData\Local\Programs\Python\Python313\python.exe"

# Validate paths
if (!(Test-Path -Path $ScriptPath)) {
    Write-Host "Error: Script file not found at $ScriptPath. Please verify the path." -ForegroundColor Red
    exit 1
}
if (!(Test-Path -Path $PythonPath)) {
    Write-Host "Error: Python executable not found at $PythonPath. Please verify the installation." -ForegroundColor Red
    exit 1
}

# Define the action to run the Python script
$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument "`"$ScriptPath`"" -WorkingDirectory "C:\AI_Content_App\Datavbase_conf"

# Define the trigger to run every hour, starting at the next full hour
$NextHour = (Get-Date).AddHours(1).Date.AddHours((Get-Date).Hour + 1 - (Get-Date).Hour)
$Trigger = New-ScheduledTaskTrigger -Once -At $NextHour -RepetitionInterval (New-TimeSpan -Hours 1) -RepetitionDuration (New-TimeSpan -Days 1)

# Define settings for the task
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries `
                                          -DontStopIfGoingOnBatteries `
                                          -StartWhenAvailable `
                                          -RestartCount 3 `
                                          -RestartInterval (New-TimeSpan -Minutes 5)

# Define registration options to ensure task runs even after restarts
$Principal = New-ScheduledTaskPrincipal -UserId "NT AUTHORITY\SYSTEM" -LogonType ServiceAccount

# Register the scheduled task
try {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Description "Runs the Trends24 scraper script every hour"
    Write-Host "Scheduled task '$TaskName' created successfully!" -ForegroundColor Green
} catch {
    Write-Host "Failed to create the scheduled task. Error: $_" -ForegroundColor Red
    exit 1
}

# Test the task by running it immediately
try {
    Start-ScheduledTask -TaskName $TaskName
    Write-Host "Scheduled task has been started for immediate execution." -ForegroundColor Green
} catch {
    Write-Host "Failed to start the scheduled task. Verify the configuration in Task Scheduler." -ForegroundColor Red
}
