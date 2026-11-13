#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
cat source-bundle/part-00.bin source-bundle/part-01.bin source-bundle/part-02.bin source-bundle/part-03.bin source-bundle/part-04.bin > retrowave-player.tar.xz
tar -xJf retrowave-player.tar.xz
printf '\nProject extracted to ./retrowave-player\n'
