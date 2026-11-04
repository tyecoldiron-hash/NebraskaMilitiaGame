# Slim Godot 4.3 macOS arm64 export template

This repository builds a size-optimized **Godot 4.3-stable** macOS Apple Silicon release export template. Godot Engine is MIT licensed; this repo contains the build profile and workflow only. The game itself is not stored here. The game uses the GL Compatibility renderer, 3D, and GDScript, and the zipped `.app` needs to stay under 25 MB, so the stock template binary (about 24 MB zipped) leaves no room for art.

## Workflow

[`.github/workflows/slim-macos-template.yml`](.github/workflows/slim-macos-template.yml) runs on a GitHub-hosted **`macos-15-intel`** runner and cross-compiles the arm64 template (`arch=arm64`). GitHub Actions retired the macOS 14 images on November 2, 2026. A `macos-15` Apple Silicon job was then cancelled before any step ran: the hosted arm64 pool never assigned a runner. The Intel macOS 15 image is a separate pool, and Xcode on it can emit an arm64 binary.

It runs on `workflow_dispatch`, on pushes to `main`, and on pull requests. README-only pushes are ignored so a size note does not rebuild the engine.

The job:

1. Checks out this repo and `godotengine/godot` at tag **`4.3-stable`**.
2. Installs SCons 4.8.1 under Python 3.12 and restores an SCons cache (`SCONS_CACHE`).
3. Builds with Xcode's `clang`:

   ```sh
   scons profile="$GITHUB_WORKSPACE/custom.py" platform=macos arch=arm64 target=template_release lto=full -j3
   ```

4. Runs `strip -x` on `bin/godot.macos.template_release.arm64`.
5. Packs `macos.zip` from `misc/dist/macos_template.app`, with the arm64 binary at `macos_template.app/Contents/MacOS/godot_macos_release.universal`. An arm64-only file under that name is valid: Godot's `thin.py` only slices fat binaries.
6. Uploads the raw binary and `macos.zip` as a workflow artifact, and attaches both to a public GitHub Release tagged `slim-template-4.3-<run number>`. The workflow has `contents: write`.

`production=yes` in [`custom.py`](custom.py) replaces `lto` with the command-line value, and macOS turns `lto=auto` into `none`. The workflow passes `lto=full` on the command line so link-time optimization stays on.

## Download

Release assets on this public repo can be downloaded without authentication:

The green run is `slim-template-4.3-3`:

```text
https://github.com/tyecoldiron-hash/NebraskaMilitiaGame/releases/download/slim-template-4.3-3/macos.zip
https://github.com/tyecoldiron-hash/NebraskaMilitiaGame/releases/download/slim-template-4.3-3/godot.macos.template_release.arm64
```

Later runs use the same path with their own run number:

```text
https://github.com/tyecoldiron-hash/NebraskaMilitiaGame/releases/download/slim-template-4.3-<run>/macos.zip
```

Point the macOS export preset at the zip:

```ini
custom_template/release="<path>/macos.zip"
```

The debug slot can keep using the stock 4.3 template.

## Size

Stock Godot 4.3 arm64 release template binary: **73,112,736 bytes**.

This build (`slim-template-4.3-3`, `lto=full`, stripped): **32,724,800 bytes** (about 55% smaller). `macos.zip` is **10,934,131 bytes**.

| file | bytes |
| --- | ---: |
| stock 4.3 arm64 release binary | 73,112,736 |
| `godot.macos.template_release.arm64` | 32,724,800 |
| `macos.zip` | 10,934,131 |

## Profile

[`custom.py`](custom.py) is the SCons profile: `template_release`, `optimize=size`, `lto=full`, `production=yes`, Vulkan off, OpenGL 3 on.

Kept for this game:

- `text_server_adv` and `freetype` so `.ttf` / `.otf` fonts load
- `regex`
- 3D (there is no `disable_3d`)
- GodotPhysics, which in 4.3 is part of `servers/physics_2d` and `servers/physics_3d`. `module_godot_physics_2d_enabled` and `module_godot_physics_3d_enabled` are not real options; SCons ignores them
- PNG (always compiled, `drivers/png`) and `webp` for lossless and lossy `.ctex`
- `squish`, which supplies S3TC/RGTC CPU decompression in export templates

`squish` is the module this profile turns back on. The original profile disabled it. Desktop GL, including macOS, reports S3TC as supported and uploads compressed textures directly. When a compressed texture is not a power of two and needs mipmaps or repeat, the GL Compatibility renderer decompresses it, and that path calls `Image::_image_decompress_bc` from `squish`.

`cvtt` (BPTC) and `etcpak` implement `can_build()` as editor-only, so a `template_release` build skips them even if the flags are enabled. Official 4.3 export templates are the same: BPTC `.ctex` data is uploaded when the driver advertises `GL_ARB_texture_compression_bptc`.

`jpg` stays off, and `basis_universal` is off with it because Basis hard-depends on `jpg`. Pre-imported lossless and lossy `.ctex` files use PNG and WebP, not Basis Universal.

GDScript's dependency on `jsonrpc` and `websocket` is optional and only pulls in the language server for editor builds. Those modules stay disabled.
