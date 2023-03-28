#######################################################################################
# @author: Guille Rodriguez https://github.com/guillerg86
#
# Obtiene las actualizaciones obligatorias que están disponibles
# para instalar en un equipo Windows. Funciona tanto si es gestionado
# por un sistema WSUS local, como si esta configurado para descargar
# directamente desde Microsoft.
#
# Genera un output en formato Json para una mejor integración con otros
# sistemas como: Zabbix, Web APIs, programas CLI
#######################################################################################

$updateObject = New-Object -ComObject Microsoft.Update.Session
$updateObject.ClientApplicationID = "WinUpdateCheck"
$updateSearcher = $updateObject.CreateUpdateSearcher()
$searchResults = $updateSearcher.Search("IsHidden=0 and IsInstalled=0 and Type !='Driver'")
$mandatoryUpdates = $searchResults.Updates | Where-Object {$_.Title -notlike "*Microsoft Defender*"}

$updates = [System.Collections.ArrayList]::new()
$totalsize = 0; 
foreach($update in $mandatoryUpdates) { 
	$totalsize = $totalsize + $update.MaxDownloadSize; 
	
	$newUpdate = New-Object -TypeName psobject	
	$newUpdate | Add-Member -NotePropertyName title -NotePropertyValue $update.Title
	$newUpdate | Add-Member -NotePropertyName size -NotePropertyValue $update.MaxDownloadSize
	
	[void]$updates.add($newUpdate);
}
 
$new_obj = New-Object -TypeName psobject
$new_obj | Add-Member -NotePropertyName count -NotePropertyValue $mandatoryUpdates.Count
$new_obj | Add-Member -NotePropertyName updates -NotePropertyValue $updates
$new_obj | Add-Member -NotePropertyName totalsize -NotePropertyValue $totalsize

Write-Host ($new_obj | ConvertTo-Json)