# Historical Audacity 3.0.2 for Linux

Unofficial community build, not affiliated with or endorsed by the Audacity project.

## Download and run

Use **Audacity-3.0.2-linux-x86_64.run** from Releases. Make it executable in your file manager and open it. It automatically unpacks and runs: no FUSE, GTK, wxWidgets, FFmpeg, fonts, or other application packages need to be installed separately. No root access is needed.

```sh
chmod +x Audacity-3.0.2-linux-x86_64.run
./Audacity-3.0.2-linux-x86_64.run
```

The AppImage is also available for users who prefer that format. The `.run` download handles extraction automatically, including on systems without FUSE.

The supported platform is an existing **x86_64 Linux desktop with glibc 2.35 or newer and X11/XWayland**. This is an operating-system compatibility baseline, not a request to install or upgrade libraries. Windows, macOS, ARM, and older Linux bases require different builds. The package includes the full linked-library dependency closure except the Linux platform C runtime, plus fonts and compatible FFmpeg 4.4.

Settings: `$XDG_CONFIG_HOME/audacity-3.0.2` (default `~/.config/audacity-3.0.2`). Existing Audacity and Tenacity settings are not migrated or modified. Temporary projects and launcher cache use a separate cache directory.

## Validation and source

The build workflow checks launch and WAV import, then runs the `.run` file in an **unmodified Ubuntu 22.04 base container**, with no dependency installation and no FUSE device. The clean-container check passed, and the automatic launcher also passed launch/WAV-import testing on Arch Linux. See release notes for the verification run.

`SHA256SUMS` covers the release assets. The corresponding-source archive includes patched Audacity, customized wxWidgets and its vendored sources, packaging scripts, and exact Ubuntu source packages for bundled libraries and fonts. Copyright notices and a dependency manifest are included in the application.

The workflow lists packages needed by developers to compile the application; end users do not need to install those packages. Audacity's source tarball is verified by SHA-256, and wxWidgets is pinned to `837669d3fa63febf0fca8cdd532abaf38a22c82a`. Compatibility patches add standard headers, replace an obsolete integer macro, update an old CMake minimum, bound historical font fitting to valid sizes, and allow isolated preferences. No host libraries are downgraded.

Audacity is distributed under GPLv2 or later; bundled libraries retain their own licenses. See `LICENSE.txt` and included notices.
