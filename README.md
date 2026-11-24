# Historical Audacity 3.0.2 for Linux

Unofficial community build of Audacity 3.0.2. This repository is not affiliated with or endorsed by the Audacity project.

The downloadable x86_64 AppImage is built on Ubuntu 22.04 (glibc 2.35 baseline). It is intended for compatible newer x86_64 Linux desktops. It does not run on Windows, macOS, ARM, or Linux systems with older glibc. See release notes for actual testing; compatibility with every distribution is not promised.

## Run

Download the AppImage from Releases, make it executable in your file manager, and open it. No root access or package replacement is required.

```sh
chmod +x Audacity-3.0.2-linux-x86_64.AppImage
./Audacity-3.0.2-linux-x86_64.AppImage
```

If FUSE is unavailable, extract and run:

```sh
./Audacity-3.0.2-linux-x86_64.AppImage --appimage-extract
./squashfs-root/AppRun
```

Settings are kept in `$XDG_CONFIG_HOME/audacity-3.0.2` (default `~/.config/audacity-3.0.2`). Existing Audacity and Tenacity settings are not migrated or modified. Temporary projects use a separate cache directory. Existing `.aup3` projects are not opened automatically; use copies when testing historical software.

## Build

The GitHub Actions workflow lists the Ubuntu 22.04 dependencies. Run `./build-appimage.sh` after installing them. The original Audacity source archive is verified by SHA-256, and the customized wxWidgets fork is pinned to commit `837669d3fa63febf0fca8cdd532abaf38a22c82a`.

The small patches add missing standard headers, remove an obsolete integer macro, update an old CMake minimum, and allow a separate settings directory. C11 is selected for older C code. The Ubuntu build uses FFmpeg 4.4, including dynamically loaded libraries in the AppImage. No host libraries are downgraded.

Release assets include checksums and the corresponding source archive: patched Audacity, customized wxWidgets and its vendored sources, packaging scripts, and exact Ubuntu source packages for bundled libraries. Copyright notices and a dependency manifest are included in the AppImage.

Audacity is distributed under GPLv2 or later; bundled libraries retain their own licenses. See `LICENSE.txt` and the included notices.
