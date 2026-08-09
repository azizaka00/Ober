$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$server = "root@77.42.123.90"
$secureKey = $null
$keyPtr = [IntPtr]::Zero
$plainKey = $null
$payload = $null

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  OBER - OpenAI rasmli qidiruvni xavfsiz yoqish" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "OpenAI API kalitini joylashtiring va Enter bosing."
Write-Host "Kiritayotgan matningiz ekranda ko'rinmaydi." -ForegroundColor DarkGray
Write-Host ""

try {
    $secureKey = Read-Host "API kalit" -AsSecureString
    $keyPtr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureKey)
    $plainKey = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($keyPtr)

    if ([string]::IsNullOrWhiteSpace($plainKey) -or
        -not $plainKey.StartsWith("sk-") -or
        $plainKey.Length -lt 20 -or
        $plainKey -match "\s") {
        throw "Kalit formati noto'g'ri. U sk- bilan boshlanishi va bo'sh joysiz bo'lishi kerak."
    }

    # BOMsiz UTF-8 yuboriladi. Systemd env faylining birinchi kalit nomi oldida
    # yashirin BOM bo'lsa, butun OPENAI_API_KEY qatorini yaroqsiz deb tashlaydi.
    # Birinchi izoh qatori qo'shimcha himoya: kodirovka xatosi takrorlansa ham
    # systemd jurnaliga maxfiy kalit emas, faqat izoh qatori tushadi.
    $payload = "# OBER AI environment`nOPENAI_API_KEY=$plainKey`nOBER_VISION_MODEL=gpt-5.6-luna`nOBER_VISION_DETAIL=low`n"
    $remoteCommand = 'umask 077; cat > /etc/ober-ai.env.new; if [ "$(od -An -tx1 -N3 /etc/ober-ai.env.new | tr -d " \n")" = "efbbbf" ]; then dd if=/etc/ober-ai.env.new of=/etc/ober-ai.env.clean bs=1 skip=3 status=none; mv /etc/ober-ai.env.clean /etc/ober-ai.env.new; fi; chmod 600 /etc/ober-ai.env.new; mv /etc/ober-ai.env.new /etc/ober-ai.env; systemctl restart ober-server; systemctl is-active ober-server'

    $startInfo = [Diagnostics.ProcessStartInfo]::new()
    $startInfo.FileName = "ssh"
    $startInfo.Arguments = "-o BatchMode=yes $server `"$remoteCommand`""
    $startInfo.UseShellExecute = $false
    $startInfo.RedirectStandardInput = $true
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    $startInfo.CreateNoWindow = $true

    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $startInfo
    if (-not $process.Start()) {
        throw "SSH ishga tushmadi."
    }

    $utf8NoBom = [Text.UTF8Encoding]::new($false)
    $payloadBytes = $utf8NoBom.GetBytes($payload)
    $process.StandardInput.BaseStream.Write($payloadBytes, 0, $payloadBytes.Length)
    $process.StandardInput.BaseStream.Flush()
    $process.StandardInput.Close()
    $output = $process.StandardOutput.ReadToEnd()
    $errorOutput = $process.StandardError.ReadToEnd()
    $process.WaitForExit()

    if ($process.ExitCode -ne 0) {
        if ($errorOutput) { Write-Host $errorOutput -ForegroundColor Red }
        throw "Server kalitni qabul qilmadi. SSH ulanishini tekshiring."
    }

    if ($output.Trim() -ne "active") {
        throw "Kalit yozildi, lekin ober-server faol holatga qaytmadi."
    }

    Write-Host ""
    Write-Host "TAYYOR: OpenAI kaliti serverga xavfsiz yozildi." -ForegroundColor Green
    Write-Host "OBER serveri faol. Endi ober.uz da rasm bilan qidirib ko'ring." -ForegroundColor Green
}
catch {
    Write-Host ""
    Write-Host "XATO: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
finally {
    $payload = $null
    $plainKey = $null
    if ($keyPtr -ne [IntPtr]::Zero) {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($keyPtr)
    }
    $secureKey = $null
}
