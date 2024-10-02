$username = "volin.d@nt351.a1tis.ru"
$pass_string = "dima8968!"

$pass = ConvertTo-SecureString $pass_string -AsPlainText -force
$cred = New-Object System.Management.Automation.PsCredential($username, $pass)

try {
	$username = $args[0]

	$res = Invoke-Command -ConfigurationName Microsoft.Exchange -ConnectionUri http://eserv1/PowerShell/ -Credential $cred -ScriptBlock {
		 Get-MailboxAutoReplyConfiguration $Using:username | Select-Object AutoReplyState
	}

	$state = $res.AutoReplyState.Value
	echo "AutoReplyState: $state"
}
catch {
	Write-Output "WAS ERROR NEED CHANGE THIS!..."
	throw "Not valid data!";
} 
