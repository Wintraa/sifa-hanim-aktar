# Ürün fotoğraflarını 4:5 kadraja oturt:
# - dikey şişe: tamamı görünsün, zemin rengi kenarı doldursun
# - yatay baharat: kadrajı doldur (hafif yan kırpma)
Add-Type -AssemblyName System.Drawing

$ErrorActionPreference = "Stop"
$dir = Join-Path (Split-Path $PSScriptRoot -Parent) "assets\products"
$targetW = 900
$targetH = 1125
$pad = 0.055
$targetRatio = $targetW / $targetH

function Get-AvgCornerColor([System.Drawing.Bitmap]$bmp) {
  $maxX = [Math]::Max(0, $bmp.Width - 3)
  $maxY = [Math]::Max(0, $bmp.Height - 3)
  $r = 0; $g = 0; $b = 0
  foreach ($c in @(
      $bmp.GetPixel(2, 2),
      $bmp.GetPixel($maxX, 2),
      $bmp.GetPixel(2, $maxY),
      $bmp.GetPixel($maxX, $maxY)
    )) {
    $r += $c.R; $g += $c.G; $b += $c.B
  }
  [System.Drawing.Color]::FromArgb([int]($r / 4), [int]($g / 4), [int]($b / 4))
}

$jpegCodec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() |
  Where-Object { $_.MimeType -eq "image/jpeg" }
$encoder = [System.Drawing.Imaging.Encoder]::Quality
$encParams = New-Object System.Drawing.Imaging.EncoderParameters 1
$encParams.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter $encoder, ([long]90)

$files = Get-ChildItem $dir -File | Where-Object { $_.Extension -match '\.(jpe?g|png|webp)$' }
foreach ($file in $files) {
  $srcImg = [System.Drawing.Image]::FromFile($file.FullName)
  $src = New-Object System.Drawing.Bitmap $srcImg
  $srcImg.Dispose()

  $canvas = New-Object System.Drawing.Bitmap $targetW, $targetH
  $g = [System.Drawing.Graphics]::FromImage($canvas)
  $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
  $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
  $g.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality

  $bg = Get-AvgCornerColor $src
  $g.Clear($bg)

  $ratio = $src.Width / $src.Height
  if ($ratio -lt $targetRatio) {
    $availW = $targetW * (1 - 2 * $pad)
    $availH = $targetH * (1 - 2 * $pad)
    $scale = [Math]::Min($availW / $src.Width, $availH / $src.Height)
    $dw = [int][Math]::Max(1, $src.Width * $scale)
    $dh = [int][Math]::Max(1, $src.Height * $scale)
    $dx = [int](($targetW - $dw) / 2)
    $dy = [int](($targetH - $dh) / 2)
    $g.DrawImage($src, $dx, $dy, $dw, $dh)
  } else {
    $scale = [Math]::Max($targetW / $src.Width, $targetH / $src.Height)
    $dw = [int]($src.Width * $scale)
    $dh = [int]($src.Height * $scale)
    $dx = [int](($targetW - $dw) / 2)
    $dy = [int](($targetH - $dh) / 2)
    $g.DrawImage($src, $dx, $dy, $dw, $dh)
  }

  $g.Dispose()
  $src.Dispose()

  $tmp = Join-Path $dir ("tmp-" + $file.Name)
  $canvas.Save($tmp, $jpegCodec, $encParams)
  $canvas.Dispose()
  Move-Item -LiteralPath $tmp -Destination $file.FullName -Force
  [GC]::Collect()
  Write-Host ("fitted " + $file.Name)
}

Write-Host "done $($files.Count) files"
