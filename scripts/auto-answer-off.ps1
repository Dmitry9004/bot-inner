$username = "volin.d@nt351.a1tis.ru"
$pass_string = "dima8968!"

$pass = ConvertTo-SecureString $pass_string -AsPlainText -force
$cred = New-Object System.Management.Automation.PsCredential($username, $pass)

try {
	$username = $args[0]

	Invoke-Command -ConfigurationName Microsoft.Exchange -ConnectionUri http://eserv1/PowerShell/ -Credential $cred -ScriptBlock {
		Set-MailboxAutoReplyConfiguration -Identity $Using:username -AutoReplyState Disabled
	}
}
catch {
	Write-Output "WAS ERROR NEED CHANGE THIS!..."
	throw "Not valid data!";
} 
