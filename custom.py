# Size-optimized Godot 4.3-stable macOS arm64 release export template.
# Project facts (grep of .gd/.tscn/.tres on seymour/size, ed5a441):
#   renderer = gl_compatibility (OpenGL3) -> Vulkan/MoltenVK not needed
#   RegEx used in scripts/Unit.gd -> keep module_regex
#   no RigidBody/CharacterBody/Area3D/RayCast/Navigation/GLTFDocument/XR/multiplayer/video use
#
# production=yes overwrites lto with the command-line value (default "auto").
# platform/macos/detect.py turns lto=auto into none, so the workflow also
# passes lto=full on the scons command line.
platform = "macos"
arch = "arm64"
target = "template_release"
optimize = "size"
lto = "full"
production = "yes"
debug_symbols = "no"

vulkan = "no"            # GL compatibility renderer only
opengl3 = "yes"
openxr = "no"
disable_advanced_gui = "no"   # keep: HUD uses standard Controls
# 3D stays enabled. In 4.3 the physics servers live in servers/physics_2d
# and servers/physics_3d, not in modules. The module_godot_physics_* keys
# below are not SCons options; Variables() ignores them.

modules_enabled_by_default = "yes"
module_gdscript_enabled = "yes"
module_text_server_adv_enabled = "yes"   # .ttf/.otf via HarfBuzz + FreeType
module_freetype_enabled = "yes"
module_text_server_fb_enabled = "no"
module_regex_enabled = "yes"
# Lossless .ctex is PNG (drivers/png, always built) or WebP. Lossy .ctex is WebP.
module_webp_enabled = "yes"

module_navigation_enabled = "no"
module_csg_enabled = "no"
module_gridmap_enabled = "no"
module_multiplayer_enabled = "no"
module_enet_enabled = "no"
module_webrtc_enabled = "no"
module_websocket_enabled = "no"
module_upnp_enabled = "no"
module_mbedtls_enabled = "no"   # no networking/crypto use
module_openxr_enabled = "no"
module_mobile_vr_enabled = "no"
module_webxr_enabled = "no"
module_theora_enabled = "no"
module_ogg_enabled = "no"        # re-enable if .ogg audio is added
module_vorbis_enabled = "no"
module_minimp3_enabled = "no"
module_camera_enabled = "no"
module_gltf_enabled = "no"       # runtime GLTF loading unused (.glb is pre-imported to .scn)
module_fbx_enabled = "no"
module_jsonrpc_enabled = "no"
module_lightmapper_rd_enabled = "no"
module_raycast_enabled = "no"    # Embree occlusion culling (editor/bake only)
module_xatlas_unwrap_enabled = "no"
module_meshoptimizer_enabled = "no"
# squish registers Image::_image_decompress_bc for template builds.
# Desktop GL (including macOS) samples S3TC directly when it can, and
# decompresses non-power-of-two textures that need mipmaps or repeat.
module_squish_enabled = "yes"
# cvtt and etcpak implement can_build() as editor_build only, so a
# template_release build skips them even if these are "yes". BPTC upload
# uses GL_ARB_texture_compression_bptc at runtime, same as official 4.3 templates.
module_cvtt_enabled = "no"
module_etcpak_enabled = "no"
module_basis_universal_enabled = "no"
module_tga_enabled = "no"
module_hdr_enabled = "no"
module_dds_enabled = "no"
module_ktx_enabled = "no"
# basis_universal hard-depends on jpg. With jpg off, SCons disables Basis
# (pre-imported lossless/lossy .ctex does not use Basis).
module_jpg_enabled = "no"
module_bmp_enabled = "no"
module_svg_enabled = "no"   # only icon.svg (pre-imported); set yes if any runtime SVG load
module_godot_physics_2d_enabled = "yes"
module_godot_physics_3d_enabled = "yes"
