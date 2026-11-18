# retrowave-player

Native Android Hi-Fi music player with real-time cassette DSP and the **actual PMMA acrylic GLSL shader supplied for this project**.

## Download and assemble the Android project

1. Open **Code → Download ZIP** and extract the repository.
2. Run `assemble.bat` on Windows or `sh assemble.sh` on Android/Termux/Linux/macOS.
3. Open the generated `retrowave-player` folder in Android Studio.

The assembly script reconstructs the Android Studio source archive and applies `android-overlay.zip`. The overlay replaces the older AGSL approximation with the supplied GLSL 300 es vertex and fragment shaders and wires them into the player UI.

## The shader is actually executed

The original full shader document remains preserved at `retrowave-player/assets/reference/liquid.txt` inside the reconstructed project.

These two shader stages are extracted verbatim from its `vsSource` and `fsSource` template literals:

- `app/src/main/assets/shaders/liquid_vertex.glsl`
- `app/src/main/assets/shaders/liquid_fragment.glsl`

`PmmaShaderView` loads them as Android assets and compiles/links them at runtime with `GLES30.glCompileShader` and `GLES30.glLinkProgram` inside a native `GLSurfaceView`. This is the supplied shader running through OpenGL ES 3.0 on the GPU, not an image, CSS effect or simplified AGSL copy.

The player configures the shader for **Pure PMMA + Studio N8** by default. The original shader's PMMA refraction, chamfered bevel, chromatic dispersion, six-slot ripple ring, finger dent lens, spring-smoothed tilt and procedural metallic/amber background are active on the deck and tape-profile glass panels. Seven visual display modes and five procedural backgrounds remain in the fragment source for future UI controls.

The old `liquid_glass.agsl` file is kept only as a historical reference; the active player panels use the original GLSL through GLES 3.0. Devices must support OpenGL ES 3.0.

## Audio DSP

The visual shader is separate from the audio engine. Audio processing runs on decoded PCM in the Media3 playback path:

- Drive / tape saturation
- Wow and flutter speed instability
- Hiss and crackle
- Tone roll-off
- Stereo width
- Bit reduction
- Dry/Wet mix and bypass

These effects alter audio; the visual shader does not.

## Build requirements

- Android Studio with Android SDK Platform 36
- JDK 17+
- Gradle 8.13
- An OpenGL ES 3.0-capable Android device for the shader renderer

Build from the extracted project folder:

```sh
gradle testDebugUnitTest assembleDebug
```

The debug APK is created at `app/build/outputs/apk/debug/app-debug.apk`. GitHub Actions also builds a debug APK and uploads it as the `retrowave-player-debug-apk` artifact.

## Status

The CI build verifies Kotlin compilation, unit tests, APK packaging and artifact upload. The GLES shader is compiled at runtime on the Android device, so visual performance and driver compatibility still need hands-on device validation.
