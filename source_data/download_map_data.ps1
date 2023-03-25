$urls = @(
    [uri]'https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lad_000a21a_f.zip',
    [uri]'https://www150.statcan.gc.ca/n1/tbl/csv/98100015-fra.zip',
    [uri]'https://data.montreal.ca/dataset/b628f1da-9dc3-4bb1-9875-1470f891afb1/resource/92cb062a-11be-4222-9ea5-867e7e64c5ff/download/limites-terrestres.geojson'
)

New-Item -Path "$PSScriptRoot\map" -ItemType Directory -ErrorAction Ignore
foreach ($url in $urls) {
    $dest = "$PSScriptRoot\map\$($url.Segments[-1])"
    if (!(Test-Path -Path $dest -PathType Leaf)) {
        Invoke-WebRequest -Uri $url -OutFile $dest
    }
}