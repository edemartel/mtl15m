$data = Get-Content -Path "$PSScriptRoot/sources.jsonc" -Raw | ConvertFrom-Json -AsHashtable

foreach ($pair in $data.GetEnumerator()) {
    $dir = "$PSScriptRoot/$($pair.Key)"
    New-Item -Path $dir -ItemType Directory -ErrorAction Ignore
    foreach ($str in $pair.Value) {
        $url = [uri]$str
        $dest = "$dir/$($url.Segments[-1])"
        if (!(Test-Path -Path $dest -PathType Leaf)) {
            Invoke-WebRequest -Uri $url -OutFile $dest
        }
    }
}