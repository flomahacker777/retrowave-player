#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$ROOT"
cat source-bundle/part-00.bin source-bundle/part-01.bin source-bundle/part-02.bin source-bundle/part-03.bin source-bundle/part-04.bin > retrowave-player.tar.xz
tar -xJf retrowave-player.tar.xz
python3 "$ROOT/apply-project-overlay.py" "$ROOT/retrowave-player"
printf '\nProject extracted and supplied GLSL overlay applied to ./retrowave-player\n'
