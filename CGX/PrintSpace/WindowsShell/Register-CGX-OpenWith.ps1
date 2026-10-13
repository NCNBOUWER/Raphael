[CmdletBinding()]
param([switch]$Install, [switch]$Remove, [switch]$Probe)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
if($Install -and $Remove){throw 'Install and Remove are mutually exclusive.'}
$script='C:\Cognigrex\Interfaces\Open-CGX.ps1'
$hostExe=Join-Path $env:WINDIR 'System32\WindowsPowerShell\v1.0\powershell.exe'
$prog='Cognigrex.LightSpeedOpen'
$base='HKCU:\Software\Classes'
$menu=Join-Path $base 'SystemFileAssociations\.cgx\shell\CGXOpenLightSpeed'
$progKey=Join-Path $base $prog
$with=Join-Path $base '.cgx\OpenWithProgids'
$command=('"'+$hostExe+'" -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "'+$script+'" -CarrierPath "%1"')
$defaultKey=Join-Path $base '.cgx'
$originalDefault=if(Test-Path $defaultKey){(Get-Item $defaultKey).GetValue('')}else{$null}
if($Install){
    if(-not (Test-Path -LiteralPath $script -PathType Leaf)){throw 'Missing reviewed CGX operator launcher.'}
    foreach($key in @($menu,$progKey)){
        if(Test-Path -LiteralPath $key){
            $child=Join-Path $key 'shell\open\command'
            if($key -eq $menu){$child=Join-Path $key 'command'}
            if(-not (Test-Path $child) -or (Get-Item $child).GetValue('') -cne $command){
                throw ('Existing association collision at '+$key)
            }
        }
    }
    New-Item -Path $menu -Force | Out-Null
    Set-Item -Path $menu -Value 'Open in Cognigrex (LightSpeed)'
    New-Item -Path (Join-Path $menu 'command') -Force | Out-Null
    Set-Item -Path (Join-Path $menu 'command') -Value $command
    New-Item -Path $progKey -Force | Out-Null
    Set-Item -Path $progKey -Value 'Cognigrex user-level LS GO viewer (no import)'
    New-Item -Path (Join-Path $progKey 'shell\open\command') -Force | Out-Null
    Set-Item -Path (Join-Path $progKey 'shell\open\command') -Value $command
    New-Item -Path $with -Force | Out-Null
    New-ItemProperty -Path $with -Name $prog -Value '' -PropertyType String -Force | Out-Null
}
if($Remove){
    foreach($key in @($menu,$progKey)){
        $child=if($key -eq $menu){Join-Path $key 'command'}else{Join-Path $key 'shell\open\command'}
        if(Test-Path $key){
            if(-not(Test-Path $child) -or (Get-Item $child).GetValue('') -cne $command){throw ('Refusing to remove modified key: '+$key)}
            Remove-Item -LiteralPath $key -Recurse -Force
        }
    }
    if(Test-Path $with){Remove-ItemProperty -Path $with -Name $prog -ErrorAction SilentlyContinue}
}
$now=if(Test-Path $defaultKey){(Get-Item $defaultKey).GetValue('')}else{$null}
if($now -cne $originalDefault){throw 'Unexpected Windows .cgx default association mutation!'}
$menuCmd=Join-Path $menu 'command'
[pscustomobject]@{
    schema='CGX-WINDOWS-OPENWITH-REG/0.1'
    installed=$(if(Test-Path $menuCmd){(Get-Item $menuCmd).GetValue('') -ceq $command}else{$false})
    operation=$(if($Install){'install'}elseif($Remove){'remove'}else{'probe'})
    default_class=$now
    changed_default=$false
    user_scope='HKCU_ONLY'
    reversible=$true
    new_file_parser=$false
    source_script=$script
} | ConvertTo-Json
