param(
    [string]$ProjectDir = "retrowave-player"
)
$ErrorActionPreference = "Stop"
$player = Join-Path $ProjectDir "app/src/main/java/com/retrowave/player/ui/PlayerScreen.kt"
if (-not (Test-Path $player)) { throw "PlayerScreen.kt not found: $player" }
$content = [System.IO.File]::ReadAllText((Resolve-Path $player))
$content = $content.Replace("import androidx.compose.foundation.layout.calculateTopPadding`n", "")
$content = $content.Replace("import androidx.compose.foundation.layout.calculateBottomPadding`n", "")
$content = $content.Replace(
    ".background(if (large) Brush.linearGradient(listOf(Color(0xFFFFC879), AmberDim)) else Color(0xFF252D34))",
    ".then(if (large) Modifier.background(Brush.linearGradient(listOf(Color(0xFFFFC879), AmberDim))) else Modifier.background(Color(0xFF252D34)))"
)
[System.IO.File]::WriteAllText((Resolve-Path $player), $content, [System.Text.UTF8Encoding]::new($false))
if (-not $content.Contains("Modifier.background(Color(0xFF252D34))")) { throw "UI patch verification failed" }
Write-Host "Applied Android UI compile fixes to $player"
