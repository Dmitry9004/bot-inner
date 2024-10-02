$username = "volin.d@nt351.a1tis.ru"
$pass_string = "dima8968!"

$pass = ConvertTo-SecureString $pass_string -AsPlainText -force
$cred = New-Object System.Management.Automation.PsCredential($username, $pass)

try {
	#$Session = New-PSSession -ConfigurationName Microsoft.Exchange -ConnectionUri http://eserv1/PowerShell/ -Credential $cred
	#Import-PSSession $Session -DisableNameChecking

	$msgInt = $args[2]
	$msgExt = $args[3]
	$username = $args[4]

	$startDate = $args[0]
	$endDate = $args[1]

	Invoke-Command -ConfigurationName Microsoft.Exchange -ConnectionUri http://eserv1/PowerShell/ -Credential $cred -ScriptBlock {
		Set-MailboxAutoReplyConfiguration -Identity $Using:username -AutoReplyState Scheduled -StartTime $Using:startDate -EndTime $Using:endDate -ExternalAudience All -InternalMessage $Using:msgInt -ExternalMessage $Using:msgExt
	}
}
catch {
	Write-Output "WAS ERROR NEED CHANGE THIS!..."
	throw "Not valid data!";
} 
