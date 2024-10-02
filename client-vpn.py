import subprocess
from os import chmod
from os import remove
from sys import argv

server = "?srv?"
vpnUsername = "?vpn-usr?"
username = "?usr?"
password = "?psw?"
IPAddress = "?ip?"
key = "?key?"
pcName = "?pcName?"

setVpn = f"""Add-VpnConnection  -Name "work-vpn" -ServerAddress "{server}" -TunnelType "L2tp" -L2tpPsk "{key}" -AuthenticationMethod Chap, MSChapv2 -Force
	Install-PackageProvider -Name NuGet -Force
	Install-Module -Name VPNCredentialsHelper -Force
	Set-ExecutionPolicy RemoteSigned -Force
	Import-Module VPNCredentialsHelper
	Set-VpnConnectionUsernamePassword -connectionName "work-vpn" -username "{vpnUsername}" -password "{password}"
    route /p add 192.168.2.0 mask 255.255.255.0 {IPAddress}
	route /p add 192.168.3.0 mask 255.255.255.0 {IPAddress}
	route /p add 192.168.4.0 mask 255.255.255.0 {IPAddress}
	route /p add 192.168.5.0 mask 255.255.255.0 {IPAddress}
	route /p add 192.168.40.0 mask 255.255.255.0 {IPAddress}
	route /p add 192.168.99.0 mask 255.255.255.0 {IPAddress}
    
    rasdial "work-vpn"
"""

out = subprocess.Popen(["powershell", setVpn], stdout=subprocess.PIPE).communicate() 

desktopPath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

f = open(f"{desktopPath}\\work-pc.rdp", "w")
f.write(f""" screen mode id:i:2
use multimon:i:0
desktopwidth:i:1920
desktopheight:i:1080
session bpp:i:32
winposstr:s:0,1,64,46,1680,960
compression:i:1
keyboardhook:i:2
audiocapturemode:i:0
videoplaybackmode:i:1
connection type:i:7
networkautodetect:i:1
bandwidthautodetect:i:1
displayconnectionbar:i:1
enableworkspacereconnect:i:0
disable wallpaper:i:0
allow font smoothing:i:0
allow desktop composition:i:0
disable full window drag:i:1
disable menu anims:i:1
disable themes:i:0
disable cursor setting:i:0
bitmapcachepersistenable:i:1
full address:s:{pcName}.nt351.a1tis.ru
audiomode:i:0
redirectprinters:i:0
redirectcomports:i:0
redirectsmartcards:i:0
redirectclipboard:i:0
redirectposdevices:i:0
autoreconnection enabled:i:1
authentication level:i:0
prompt for credentials:i:1
negotiate security layer:i:1
remoteapplicationmode:i:0
alternate shell:s:
shell working directory:s:
gatewayhostname:s:
gatewayusagemethod:i:4
gatewaycredentialssource:i:4
gatewayprofileusagemethod:i:1
promptcredentialonce:i:0
gatewaybrokeringtype:i:0
use redirection server name:i:0
rdgiskdcproxy:i:0
kdcproxyname:s:
smart sizing:i:1
drivestoredirect:s:
username:s:nt351\\{username}
""")
f.close()

