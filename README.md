# retrowave-player

Native Android Hi-Fi music player with cassette-style real-time DSP and a liquid-acrylic AGSL interface.

## Source bundle

The complete Android Studio project is packaged in **[`retrowave-player-source.tar.xz`](./retrowave-player-source.tar.xz)**. It includes the Kotlin sources, Gradle configuration, Android resources, the adapted AGSL shader, the original supplied `liquid.txt`, documentation, tests, and GitHub Actions workflow.

Extract it with 7-Zip (Windows / Android) or:

```sh
tar -xJf retrowave-player-source.tar.xz
```

Then open the extracted `retrowave-player` folder in Android Studio.

## Features

- Kotlin + Jetpack Compose UI
- Media3 ExoPlayer and background MediaSession playback
- Local audio import through Android's system picker
- Live tape-color DSP: saturation/drive, wow, flutter, hiss, crackle, tone roll-off, stereo width, bit reduction, dry/wet and bypass
- AGSL liquid-glass shader on Android 13+ with a Compose fallback on older versions
- GitHub Actions workflow for Android CI

## Build requirements

- Android Studio with Android SDK Platform 36
- JDK 17+
- Gradle 8.13-compatible Android Gradle Plugin setup

The source bundle currently contains the Gradle project but not a Gradle wrapper JAR. Open it in Android Studio, or generate a wrapper with an installed Gradle 8.13:

```sh
gradle wrapper --gradle-version 8.13
gradle assembleDebug
```

## Status

Early project foundation. The included code is intended for Android-device validation; audio coloration and shader performance may vary by Android version, output route and device.

## License

See [LICENSE](./LICENSE) inside the extracted source folder.
