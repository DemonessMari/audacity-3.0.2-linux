Unofficial historical Audacity 3.0.2 build for **x86_64 Linux**.

Download `Audacity-3.0.2-linux-x86_64.AppImage`, make it executable, and open it. No root access or replacement of installed Audacity/Tenacity is required.

```sh
chmod +x Audacity-3.0.2-linux-x86_64.AppImage
./Audacity-3.0.2-linux-x86_64.AppImage
```

If FUSE is unavailable:

```sh
./Audacity-3.0.2-linux-x86_64.AppImage --appimage-extract
./squashfs-root/AppRun
```

Built on Ubuntu 22.04, targeting compatible newer x86_64 Linux desktops with glibc 2.35 or later. This is not a Windows, macOS, ARM, or universally compatible Linux binary. The package bundles customized wxWidgets and compatible FFmpeg 4.4 libraries. Existing system libraries are not downgraded.

Settings: `~/.config/audacity-3.0.2` (or the corresponding XDG_CONFIG_HOME path). Temporary projects use a separate cache directory. Existing Audacity/Tenacity preferences are not migrated or modified.

`SHA256SUMS` verifies the release assets. The corresponding-source archive includes patched Audacity and wxWidgets, build scripts, and exact Ubuntu source packages for bundled libraries. Bundled copyright notices and a dependency manifest are included in the AppImage.

This is a community build, not an official Audacity release. Audacity and library authors retain their copyrights; see the included licenses.
