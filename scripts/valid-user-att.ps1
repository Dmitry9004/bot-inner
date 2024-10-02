$id = $args[0]
$attr = $args[1] 

$username = "nt351.a1tis.ru\volin.d"
$pass_string = "dima8968!"

$pass = ConvertTo-SecureString $pass_string -AsPlainText -force
$cred = New-Object System.Management.Automation.PsCredential($username, $pass)

Enter-PSSession -ComputerName pdc2012 -Credential $cred -Authentication Negotiate -Verbose
$login = Get-ADuser -Filter "$attr -eq '$id'" | Select SamAccountName

if ($login.SamAccountName -eq "") {
	echo "Not found username"
	exit 100
}

$name = $login.SamAccountName

echo "login: $name" 
