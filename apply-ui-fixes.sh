#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${1:-retrowave-player}"
PLAYER="$PROJECT_DIR/app/src/main/java/com/retrowave/player/ui/PlayerScreen.kt"
if [[ ! -f "$PLAYER" ]]; then
  echo "PlayerScreen.kt not found: $PLAYER" >&2
  exit 1
fi

# PaddingValues exposes these as member functions, not importable symbols.
sed -i \
  -e '/^import androidx\.compose\.foundation\.layout\.calculateTopPadding$/d' \
  -e '/^import androidx\.compose\.foundation\.layout\.calculateBottomPadding$/d' \
  "$PLAYER"

# Keep Brush and Color in separate background overloads.
sed -i \
  's#\.background(if (large) Brush\.linearGradient(listOf(Color(0xFFFFC879), AmberDim)) else Color(0xFF252D34))#.then(if (large) Modifier.background(Brush.linearGradient(listOf(Color(0xFFFFC879), AmberDim))) else Modifier.background(Color(0xFF252D34)))#' \
  "$PLAYER"

grep -q 'Modifier.background(Color(0xFF252D34))' "$PLAYER"
echo "Applied Android UI compile fixes to $PLAYER"
