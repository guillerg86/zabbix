#######################################################################################
# @author: Guille Rodriguez https://github.com/guillerg86
#
# Permite saber el número de licencias RDP totales que tiene configurado el sistema.
#
#######################################################################################

# Obtenemos el tipo de equipo que és
$tipo_sistema = (Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion' | Select InstallationType).InstallationType

# Obtenemos el maximo de conexiones configuradas en el registro
$path = 'HKLM:\SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services\'
$obj = Get-ItemProperty -Path $path | Select MaxInstanceCount

if ($obj.MaxInstanceCount -eq $null) {
    # No ha encontrado la clave del registro
    if ( $tipo_sistema -eq "Server" ) {
        Write-Host 2
    } else {
        Write-Host 1 
    }
} else {
    Write-Host $obj.MaxInstanceCount 
}