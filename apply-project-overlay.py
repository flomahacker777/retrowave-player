#!/usr/bin/env python3
"""Apply the native GLES 3.0 port of the supplied PMMA shader to the Android project."""
from __future__ import annotations
import re
import zipfile
import sys
from pathlib import Path

project = Path(sys.argv[1] if len(sys.argv) > 1 else "retrowave-player").resolve()
repo = Path(__file__).resolve().parent
overlay_zip = repo / "android-overlay.zip"
app_main = project / "app" / "src" / "main"

if not (project / "app" / "build.gradle.kts").is_file():
    raise SystemExit(f"Android project not found: {project}")
if not overlay_zip.is_file():
    raise SystemExit(f"Shader overlay archive not found: {overlay_zip}")

with zipfile.ZipFile(overlay_zip) as archive:
    archive.extractall(app_main)

player_file = app_main / "java/com/retrowave/player/ui/PlayerScreen.kt"
source = player_file.read_text(encoding="utf-8")

# Remove imports used only by the old AGSL approximation.
obsolete_imports = (
    "import android.graphics.RuntimeShader",
    "import android.os.Build",
    "import androidx.compose.foundation.gestures.detectTapGestures",
    "import androidx.compose.runtime.withFrameNanos",
    "import androidx.compose.ui.graphics.asComposeRenderEffect",
    "import androidx.compose.ui.graphics.graphicsLayer",
    "import androidx.compose.ui.input.pointer.pointerInput",
)
for item in obsolete_imports:
    source = source.replace(item + "\n", "")

android_view_imports = (
    "import androidx.compose.ui.viewinterop.AndroidView",
    "import androidx.lifecycle.Lifecycle",
    "import androidx.lifecycle.LifecycleEventObserver",
    "import androidx.lifecycle.compose.LocalLifecycleOwner",
)
anchor = "import androidx.compose.ui.platform.LocalContext\n"
if anchor not in source:
    raise SystemExit("Could not find Compose LocalContext import anchor")
for item in android_view_imports:
    if item not in source:
        source = source.replace(anchor, anchor + item + "\n")
        anchor = item + "\n"

source = re.sub(
    r'InfoTile\("GLASS ENGINE",\s*if\s*\(Build\.VERSION\.SDK_INT\s*>=\s*33\)\s*"AGSL / PMMA"\s*else\s*"COMPOSE FALLBACK",\s*Modifier\.weight\(1f\)\)',
    'InfoTile("GLASS ENGINE", "GLES 3.0 / PMMA GLSL", Modifier.weight(1f))',
    source,
)

start_marker = "@Composable\nprivate fun LiquidGlassPanel"
end_marker = "\n@Composable\nprivate fun TransportButton"
if start_marker not in source or end_marker not in source:
    raise SystemExit("Could not locate LiquidGlassPanel function boundaries")
start = source.index(start_marker)
end = source.index(end_marker, start)

new_function = r'''@Composable
private fun LiquidGlassPanel(modifier: Modifier = Modifier, content: @Composable () -> Unit) {
    val shape = RoundedCornerShape(25.dp)
    val lifecycleOwner = LocalLifecycleOwner.current
    var shaderView by remember { mutableStateOf<PmmaShaderView?>(null) }

    DisposableEffect(lifecycleOwner, shaderView) {
        val view = shaderView
        if (view == null) return@DisposableEffect onDispose { }
        val observer = LifecycleEventObserver { _, event ->
            when (event) {
                Lifecycle.Event.ON_RESUME -> view.onResume()
                Lifecycle.Event.ON_PAUSE -> view.onPause()
                else -> Unit
            }
        }
        lifecycleOwner.lifecycle.addObserver(observer)
        if (lifecycleOwner.lifecycle.currentState.isAtLeast(Lifecycle.State.RESUMED)) {
            view.onResume()
        }
        onDispose {
            lifecycleOwner.lifecycle.removeObserver(observer)
            view.onPause()
        }
    }

    Box(
        modifier = modifier
            .clip(shape)
            .border(
                1.dp,
                Brush.linearGradient(
                    listOf(
                        Color.White.copy(alpha = 0.34f),
                        Amber.copy(alpha = 0.42f),
                        Color.White.copy(alpha = 0.08f)
                    )
                ),
                shape
            )
    ) {
        // The supplied #version 300 es PMMA fragment shader is executed directly via GLES 3.0.
        AndroidView(
            factory = { context -> PmmaShaderView(context).also { shaderView = it } },
            modifier = Modifier.fillMaxSize(),
            onRelease = { view ->
                view.onPause()
                if (shaderView === view) shaderView = null
            }
        )
        Box(
            Modifier
                .fillMaxSize()
                .background(
                    Brush.linearGradient(
                        listOf(
                            Color(0xFF101923).copy(alpha = 0.16f),
                            Color(0xFF161E26).copy(alpha = 0.10f),
                            Color(0xFF080C10).copy(alpha = 0.24f)
                        )
                    )
                )
        ) {
            content()
        }
    }
}
'''
source = source[:start] + new_function + source[end:]

# Fix the archived source's invalid mixed Brush/Color background overload.
source = source.replace(
    ".background(if (large) Brush.linearGradient(listOf(Color(0xFFFFC879), AmberDim)) else Color(0xFF252D34))",
    ".then(if (large) Modifier.background(Brush.linearGradient(listOf(Color(0xFFFFC879), AmberDim))) else Modifier.background(Color(0xFF252D34)))",
)
source = source.replace(
    "import androidx.compose.foundation.layout.calculateTopPadding\n", ""
).replace(
    "import androidx.compose.foundation.layout.calculateBottomPadding\n", ""
)
player_file.write_text(source, encoding="utf-8")

# Lifecycle-aware GLSurfaceView pause/resume support.
gradle_file = project / "app" / "build.gradle.kts"
gradle_text = gradle_file.read_text(encoding="utf-8")
compose_lifecycle = '    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.9.1")'
if "lifecycle-runtime-compose" not in gradle_text:
    anchor = '    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.9.1")'
    if anchor not in gradle_text:
        raise SystemExit("Could not find lifecycle-runtime-ktx dependency anchor")
    gradle_text = gradle_text.replace(anchor, anchor + "\n" + compose_lifecycle)
gradle_file.write_text(gradle_text, encoding="utf-8")

# The supplied shader requires OpenGL ES 3.0.
manifest_file = app_main / "AndroidManifest.xml"
manifest_text = manifest_file.read_text(encoding="utf-8")
feature = '    <uses-feature android:glEsVersion="0x00030000" android:required="true" />\n'
if 'glEsVersion="0x00030000"' not in manifest_text:
    manifest_text = manifest_text.replace(
        '<manifest xmlns:android="http://schemas.android.com/apk/res/android">\n',
        '<manifest xmlns:android="http://schemas.android.com/apk/res/android">\n' + feature
    )
manifest_file.write_text(manifest_text, encoding="utf-8")

# Update project docs to describe the active GLSL renderer, not the retired AGSL approximation.
readme_file = project / "README.md"
readme_text = readme_file.read_text(encoding="utf-8")
readme_text = readme_text.replace(
    "2. **Visual shader** — an Android AGSL port of the supplied Liquid Glass / PMMA shader: chromatic edge refraction, a soft bevel highlight, a touch-reactive lens and slow optical shimmer.",
    "2. **Visual shader** — the supplied WebGL2 PMMA acrylic vertex/fragment shader, compiled directly by Android OpenGL ES 3.0: chromatic edge refraction, chamfered acrylic volume, six-slot ring ripples, touch lens, tilt parallax and procedural Studio N8 background."
)
readme_text = readme_text.replace(
    "- AGSL liquid glass surface on Android 13+; a Compose fallback surface on earlier versions.",
    "- Native OpenGL ES 3.0 PMMA acrylic surface using the supplied GLSL 300 es vertex and fragment shaders."
)
old_shader_section = re.compile(r"## Shader integration\n[\s\S]*?(?=## Build)")
new_shader_section = """## Shader integration

The original supplied shader document is preserved at `assets/reference/liquid.txt`.

The app extracts and runs the original WebGL2 `vsSource` and `fsSource` stages directly through Android OpenGL ES 3.0:

- `app/src/main/assets/shaders/liquid_vertex.glsl`
- `app/src/main/assets/shaders/liquid_fragment.glsl`

`PmmaShaderView` compiles those GLSL 300 es stages with `GLES30.glCompileShader` and links them into a GPU program. The fragment shader includes the original six-slot ripple ring buffer, touch lens, tilt parallax, chromatic bevel refraction, procedural backgrounds and seven display modes. The Hi-Fi player defaults to Pure PMMA + Studio N8. This is the supplied GLSL running on the GPU, not a CSS imitation, screenshot or simplified AGSL rewrite.

The old `liquid_glass.agsl` file remains as a historical reference; the active player panels use the supplied GLSL through OpenGL ES 3.0.

"""
if "## Shader integration" in readme_text:
    readme_text = old_shader_section.sub(new_shader_section, readme_text)
readme_file.write_text(readme_text, encoding="utf-8")

notice_file = project / "assets" / "SHADER_SOURCE_NOTICE.md"
notice_file.parent.mkdir(parents=True, exist_ok=True)
notice_file.write_text(
    "# Shader source notice\n\n"
    "`reference/liquid.txt` is the original full shader document supplied by the project owner. It is preserved verbatim as a reference asset.\n\n"
    "The app extracts and runs the original WebGL2 `vsSource` and `fsSource` GLSL 300 es stages directly through Android OpenGL ES 3.0 (`GLSurfaceView` + `GLES30`). The runtime stages are stored at `app/src/main/assets/shaders/liquid_vertex.glsl` and `app/src/main/assets/shaders/liquid_fragment.glsl`.\n\n"
    "The former AGSL implementation is retained as a historical reference only; current player panels use the supplied GLSL shader.\n",
    encoding="utf-8"
)

project_files = project / "PROJECT_FILES.txt"
if project_files.is_file():
    entries = project_files.read_text(encoding="utf-8")
    for item in (
        "app/src/main/java/com/retrowave/player/ui/PmmaShaderView.kt",
        "app/src/main/assets/shaders/liquid_vertex.glsl",
        "app/src/main/assets/shaders/liquid_fragment.glsl",
    ):
        if item not in entries:
            entries += "\n" + item
    project_files.write_text(entries, encoding="utf-8")

for shader_name in ("liquid_vertex.glsl", "liquid_fragment.glsl"):
    shader_path = app_main / "assets/shaders" / shader_name
    if not shader_path.read_text(encoding="utf-8").startswith("#version 300 es"):
        raise SystemExit(f"Unexpected shader source: {shader_name}")

print("Applied supplied WebGL2 PMMA shader as native GLES 3.0 renderer.")
print(f"Android project: {project}")
