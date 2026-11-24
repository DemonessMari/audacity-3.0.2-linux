Unofficial Audacity 3.0.2 for x86_64 Linux.

**Recommended download: `Audacity-3.0.2-linux-x86_64.run`.** Make it executable and open it. It unpacks and runs automatically; users do not need to install FUSE, GTK, wxWidgets, FFmpeg, fonts, or additional application packages. No administrator access is needed.

```sh
chmod +x Audacity-3.0.2-linux-x86_64.run
./Audacity-3.0.2-linux-x86_64.run
```

This update bundles libraries that AppImage tooling normally expects the host to provide. It includes fonts and a complete linked-library dependency closure, apart from the Linux platform C runtime. The AppImage remains available as an alternative format.

Supported base: an existing x86_64 Linux desktop with glibc 2.35+ and X11/XWayland. Other operating systems and older Linux bases need different builds; installing or upgrading system libraries is not part of this package's instructions.

Settings and temporary projects are isolated from existing Audacity and Tenacity installations. `SHA256SUMS`, corresponding source, bundled copyright notices, and a dependency manifest are provided.

The workflow verifies WAV import in an unmodified Ubuntu 22.04 base container, without installing dependency packages or exposing a FUSE device. See the linked successful build run for the completed checks.

Community build, not an official Audacity release. Original authors retain their copyrights and licenses.

Completed verification: [clean-container build and tests](https://github.com/DemonessMari/audacity-3.0.2-linux/actions/runs/45391874421), plus launch and WAV import on an Arch Linux desktop. The automatic launcher also handles an existing AppImageLauncher installation without an integration prompt for its internal payload.
