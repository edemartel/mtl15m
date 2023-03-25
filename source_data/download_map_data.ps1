$urls = @(
    [uri]'https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lad_000a21a_f.zip',
    [uri]'https://www150.statcan.gc.ca/n1/tbl/csv/98100015-fra.zip'
)

New-Item -Path "$PSScriptRoot\map" -ItemType Directory -ErrorAction Ignore
foreach ($url in $urls) {
    $dest = "$PSScriptRoot\map\$($url.Segments[-1])"
    if (!(Test-Path -Path $dest -PathType Leaf)) {
        Invoke-WebRequest -Uri $url -OutFile $dest
    }
}