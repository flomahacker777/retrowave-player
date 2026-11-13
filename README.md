# retrowave-player

Native Android Hi-Fi music player with cassette-style real-time DSP and a liquid-acrylic AGSL interface.

## Get the Android Studio project

The compressed source archive is stored as five binary Git blobs under `source-bundle/`. Download all five files:

- [Part 00](source-bundle/part-00.bin)
- [Part 01](source-bundle/part-01.bin)
- [Part 02](source-bundle/part-02.bin)
- [Part 03](source-bundle/part-03.bin)
- [Part 04](source-bundle/part-04.bin)

Join the parts **in numeric order** to reconstruct `retrowave-player.tar.xz`.

### Android (Termux) / Linux / macOS

From the repository root after downloading the files into `source-bundle`:

```sh
cat source-bundle/part-00.bin source-bundle/part-01.bin source-bundle/part-02.bin source-bundle/part-03.bin source-bundle/part-04.bin > retrowave-player.tar.xz
tar -xJf retrowave-player.tar.xz
```

### Windows

From Command Prompt:

```bat
copy /b source-bundle\part-00.bin+source-bundle\part-01.bin+source-bundle\part-02.bin+source-bundle\part-03.bin+source-bundle\part-04.bin retrowave-player.tar.xz
```

Then extract the archive with 7-Zip and open the extracted `retrowave-player` folder in Android Studio.

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

The source bundle currently contains the Gradle project but not a Gradle wrapper JAR. Open it in Android Studio, or generate a wrapper with an installed Gradle 8.13:

```sh
gradle wrapper --gradle-version 8.13
gradle assembleDebug
```

## Status

Early project foundation. The included code is intended for Android-device validation; audio coloration and shader performance may vary by Android version, output route and device.

## License

See `LICENSE` inside the extracted source folder.
