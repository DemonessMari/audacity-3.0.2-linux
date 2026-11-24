#!/usr/bin/env bash
set -euo pipefail
root=$(cd -- "$(dirname -- "$0")" && pwd)
work=${BUILD_WORK_DIR:-"$root/work"}
mkdir -p "$work" "$root/dist"
cd "$work"
source_url=https://github.com/audacity/audacity/releases/download/Audacity-3.0.2/audacity-minsrc-3.0.2.tar.xz
if [[ ! -f audacity-minsrc-3.0.2.tar.xz ]]; then curl -fL --retry 3 "$source_url" -o audacity-minsrc-3.0.2.tar.xz; fi
echo '728d6459931da006ed45a31e63b7fe6ca47a2547459a2aff3bf0880cef85c296  audacity-minsrc-3.0.2.tar.xz' | sha256sum -c -
if [[ ! -d src ]]; then
 mkdir src
 tar -xf audacity-minsrc-3.0.2.tar.xz -C src --strip-components=1
 for patch_file in "$root"/patches/modern-compiler.patch "$root"/patches/isolated-settings.patch; do patch -d src -p1 < "$patch_file"; done
 git clone --depth 1 --branch audacity-fixes-3.1.3 --recurse-submodules --shallow-submodules https://github.com/audacity/wxWidgets.git wxWidgets
 test "$(git -C wxWidgets rev-parse HEAD)" = 837669d3fa63febf0fca8cdd532abaf38a22c82a
 patch -d wxWidgets -p1 < "$root/patches/wx-cmake4.patch"
fi
cmake -S src -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr \
 -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DCMAKE_C_STANDARD=11 -Daudacity_use_wxwidgets=local \
 -DWXWIN="$work/wxWidgets" -DwxBUILD_TOOLKIT=gtk3 -DwxUSE_WEBVIEW=OFF \
 -DwxUSE_LIBTIFF=sys -DwxUSE_LIBPNG=sys -DwxUSE_LIBJPEG=sys -DwxUSE_ZLIB=sys -DwxUSE_EXPAT=sys \
 -Daudacity_use_ffmpeg=loaded -Daudacity_use_pch=yes
cmake --build build -j"${BUILD_JOBS:-3}"
DESTDIR="$work/AppDir" cmake --install build
# Audacity's wxWidgets proxy stages its private libraries in the build output.
mkdir -p AppDir/usr/lib
cp -a build/lib/libwx*.so* AppDir/usr/lib/
cp "$root/AppRun" AppDir/AppRun
chmod +x AppDir/AppRun
curl -fL --retry 3 https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage -o linuxdeploy.AppImage
chmod +x linuxdeploy.AppImage
# FFmpeg is loaded with dlopen, so explicitly deploy the compatible major versions.
APPIMAGE_EXTRACT_AND_RUN=1 ./linuxdeploy.AppImage --appdir AppDir \
 --desktop-file "$root/audacity-3.0.2.desktop" --icon-file src/images/audacity.png \
 --library /usr/lib/x86_64-linux-gnu/libavcodec.so.58 \
 --library /usr/lib/x86_64-linux-gnu/libavformat.so.58 \
 --library /usr/lib/x86_64-linux-gnu/libavutil.so.56
cp "$root/AppRun" AppDir/AppRun
chmod +x AppDir/AppRun
# Preserve licensing notices and collect exact distro source archives for bundled libraries.
mkdir -p AppDir/usr/share/doc/bundled-libraries source-dependencies
python3 "$root/collect-library-sources.py" AppDir source-dependencies
cp "$root/LICENSE.txt" AppDir/usr/share/doc/audacity/COPYING
ARCH=x86_64 VERSION=3.0.2 OUTPUT="$root/dist/Audacity-3.0.2-linux-x86_64.AppImage" \
 APPIMAGE_EXTRACT_AND_RUN=1 ./linuxdeploy.AppImage --appdir AppDir --output appimage
# Complete build inputs: patched Audacity/wxWidgets, packaging, exact distro sources.
tar --exclude=.git --exclude=build --exclude=libs --exclude=dist --exclude=work \
 -czf "$root/dist/Audacity-3.0.2-corresponding-source.tar.gz" \
 src wxWidgets source-dependencies -C "$root" build-appimage.sh collect-library-sources.py AppRun patches audacity-3.0.2.desktop LICENSE.txt
cd "$root/dist"
sha256sum ./*.AppImage ./*.tar.gz > SHA256SUMS
