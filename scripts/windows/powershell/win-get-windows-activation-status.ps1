#######################################################################################
# @author: Guille Rodriguez https://github.com/guillerg86
#
# Permite saber si un sistema Windows está pendiente de activar o está activado correctamente
# tiene en cuenta si el servidor de activación es un KMS
#
#######################################################################################

$WinVerAct=[string](cscript.exe /NoLogo c:\Windows\system32\slmgr.vbs /xpr); 
# Versión en ingles
$Res1=$WinVerAct.Contains('The machine is permanently activated.'); 
# Versión en castellano
$Res2=$WinVerAct.Contains('activado de forma permanente'); 
# Licenciado con KMS server
$Res3=$WinVerAct.Contains('de volumen expirar'); 
if ($Res1 -or $Res2 -or $Res3) {
    Write-Host 1
} else {
    Write-Host 0
}
