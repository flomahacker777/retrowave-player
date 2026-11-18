# retrowave-player

Native Android Hi-Fi music player with cassette-style real-time DSP and a liquid-acrylic AGSL interface.

## Get the Android Studio project

The Android Studio project is bundled as a compressed archive split into five binary pieces under `source-bundle/`. Download this repository using **Code → Download ZIP**, extract it, and run the assembly script:

- **Windows:** double-click `assemble.bat`
- **Android / Termux / Linux / macOS:** run `sh assemble.sh`

The scripts join the five pieces into `retrowave-player.tar.xz`, extract the Android project and apply the small Kotlin compatibility patch used by CI.

## Source archive

- [Part 00](source-bundle/part-00.bin)
- [Part 01](source-bundle/part-01.bin)
- [Part 02](source-bundle/part-02.bin)
- [Part 03](source-bundle/part-03.bin)
- [Part 04](source-bundle/part-04.bin)

## Features in the source

- Kotlin + Jetpack Compose UI
- Media3 ExoPlayer and background MediaSession playback
- Local audio import through Android's system picker
- Live tape-color DSP: saturation/drive, wow, flutter, hiss, crackle, tone roll-off, stereo width, bit reduction, dry/wet and bypass
- AGSL liquid-glass shader on Android 13+ with a Compose fallback on older versions
- VU meters, animated transport details and tactile controls
- Original supplied WebGL2 shader preserved at `retrowave-player/assets/reference/liquid.txt`

## Build requirements

- Android Studio with Android SDK Platform 36
- JDK 17+
- Gradle 8.13-compatible Android Gradle Plugin setup

The source bundle does not include the Gradle wrapper JAR. Open the extracted `retrowave-player` folder in Android Studio, or generate a wrapper with an installed Gradle 8.13:

```sh
gradle wrapper --gradle-version 8.13
gradle testDebugUnitTest assembleDebug
```

The debug APK is produced at `app/build/outputs/apk/debug/app-debug.apk`.

## Status

Early project foundation. The project has a GitHub Actions build workflow that runs unit tests and assembles a debug APK. Audio coloration and shader performance still require validation on real Android devices.

## License

See `LICENSE` inside the extracted source folder.
