[CmdletBinding()]
param([string]$CarrierPath, [switch]$Probe, [switch]$NoBrowser)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$root='C:\Cognigrex'
$selection='NO_CARRIER_SELECTED'
$uri=$null
if($CarrierPath){
    $full=[IO.Path]::GetFullPath($CarrierPath)
    if([IO.Path]::GetExtension($full) -ine '.cgx'){throw 'Only .cgx carrier selections accepted.'}
    if(-not(Test-Path -LiteralPath $full -PathType Leaf)){throw 'CGX carrier file not found.'}
    $known=@{
      'C:\Cognigrex\Cognigrex.cgx'='cgx://cognigrex/'
      'C:\Cognigrex\Domains\Romer.cgx'='cgx://cognigrex/romer'
      'C:\Cognigrex\Domains\Eco.cgx'='cgx://cognigrex/eco'
      'C:\Cognigrex\Domains\EMASSC.cgx'='cgx://cognigrex/emassc'
      'C:\Cognigrex\Domains\LS.cgx'='cgx://cognigrex/emassc/lightspeed'
    }
    foreach($item in $known.GetEnumerator()){
        if([string]::Equals($full,$item.Key,[StringComparison]::OrdinalIgnoreCase)){
            $uri=$item.Value
            break
        }
    }
    if($uri){
        $resolved= & (Join-Path $root 'Tools\resolve-cgx.ps1') $uri | ConvertFrom-Json
        if(-not $resolved.carrier_exists){throw 'CGX domain carrier missing.'}
        $selection='KNOWN_CGX_LOCAL_REFERENCE'
    }else{
        # Do not open, read, import or forward the bytes of unknown carriers.
        $selection='EXTERNAL_CGX_REVIEW_REQUIRED_NO_IMPORT'
    }
}
$url=$null
foreach($candidate in @('http://127.0.0.1:4173/','http://127.0.0.1:8080/')){
    try{
        $response=Invoke-WebRequest -Uri $candidate -UseBasicParsing -TimeoutSec 2
        if($response.StatusCode -eq 200){$url=$candidate;break}
    }catch{}
}
if(-not $Probe -and -not $NoBrowser -and $url){
    $chrome=Join-Path $env:ProgramFiles 'Google\Chrome\Application\chrome.exe'
    if(Test-Path -LiteralPath $chrome){
        Start-Process -FilePath $chrome -ArgumentList @('--new-window',('--app='+$url)) | Out-Null
    }else{Start-Process -FilePath $url | Out-Null}
}
[pscustomobject]@{
    schema='CGX-WINDOWS-LIGHT-SHELL-OPEN/0.1'
    state=$(if($url){'LOCAL_OPERATOR_AVAILABLE'}else{'LOCAL_OPERATOR_OFFLINE'})
    selection=$selection
    cgx_uri=$uri
    operator_url=$url
    root_path=$root
    provider_mode='existing_lightspeed_only'
    file_import=$false
    canonical_mutation=$false
    windows_default_changed=$false
} | ConvertTo-Json -Depth 3
