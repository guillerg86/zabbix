#######################################################################################
# @author: Guille Rodriguez https://github.com/guillerg86
#
# Obtiene el número de días que han pasado desde que se instaló una actualización
# en el equipo Windows. Permite por lo tanto saber si ese equipo tiene algún problema
# con las actualizaciones, ya que cada més Microsoft saca actualizaciones acumulativas
#
#######################################################################################

$fecha_instalacion = ([WMI]'').ConvertToDateTime((Get-WmiObject Win32_OperatingSystem).InstallDate)
$last_update_datetime = $fecha_instalacion.Date

$date = Get-Date
$Session = New-Object -ComObject "Microsoft.Update.Session"
$Searcher = $Session.CreateUpdateSearcher()
$historyCount = $Searcher.GetTotalHistoryCount()
if ($historyCount -gt 1) {
	# Tiene actualizaciones instaladas, entonces obtenemos la fecha de la actualizacion mas reciente
	$hotfixes = $Searcher.QueryHistory(0, $historyCount) | Select-Object Date
	$last_update_datetime = $hotfixes[0].Date
} elseif ($historyCount -eq 1) {
    $hotfixes = $Searcher.QueryHistory(0, $historyCount) | Select-Object Date
    $last_update_datetime = $hotfixes.Date
}
$diff3 = New-TimeSpan -Start $last_update_datetime -end $date
write-host $diff3.days