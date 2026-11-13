# retrowave-player

Native Android Hi-Fi music player with cassette-style real-time DSP and a liquid-acrylic AGSL interface.

## Get the Android Studio project

The complete Android Studio project is bundled as a compressed archive split into five binary pieces under `source-bundle/`. The easiest method is to download the repository using **Code → Download ZIP**, extract it, and run the assembly script for your operating system:

- **Windows:** double-click `assemble.bat`
- **Android / Termux / Linux / macOS:** run `sh assemble.sh`

The scripts join the five binary pieces into `retrowave-player.tar.xz` and extract the project folder.

You can also download the pieces individually:

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
- GitHub Actions workflow for Android CI
- Adapted AGSL implementation based on the supplied liquid acrylic shader

## Build requirements

- Android Studio with Android SDK Platform 36
- JDK 17+
- Gradle 8.13-compatible Android Gradle Plugin setup

The source bundle contains the Gradle project but does not include the Gradle wrapper JAR. Open it in Android Studio, or generate a wrapper with an installed Gradle 8.13:

```sh
gradle wrapper --gradle-version 8.13
gradle assembleDebug
```

## Status

Early project foundation. The source code is ready for Android Studio/device validation; audio coloration and shader performance may vary by Android version, output route and device. An APK has not yet been built or device-tested in this environment.

## License

See `LICENSE` inside the extracted source folder.
