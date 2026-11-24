#!/usr/bin/env python3
"""Wrap the static AppImage runtime to automatically launch without FUSE."""
from pathlib import Path
import hashlib,sys
image=Path(sys.argv[1]);output=Path(sys.argv[2]);digest=hashlib.sha256(image.read_bytes()).hexdigest()
header='''#!/bin/sh
set -eu
umask 077
case "$0" in */*) self=$0;; *) self=$(command -v "$0");; esac
cache="${XDG_CACHE_HOME:-$HOME/.cache}/audacity-3.0.2/launcher/@HASH@"
mkdir -p "$cache"
payload="$cache/Audacity.AppImage"
if [ ! -x "$payload" ]; then
 temporary=$(mktemp "$cache/payload.XXXXXX")
 trap 'rm -f "$temporary"' EXIT HUP INT TERM
 tail -c +@OFFSET@ "$self" > "$temporary"
 actual=$(sha256sum "$temporary")
 case "$actual" in '@HASH@ '*) ;; *) echo 'Audacity payload checksum failed' >&2; exit 1;; esac
 chmod 700 "$temporary"
 mv "$temporary" "$payload"
 trap - EXIT HUP INT TERM
fi
exec "$payload" --appimage-extract-and-run "$@"
exit 1
'''.replace('@HASH@',digest)
offset=1
while True:
 data=header.replace('@OFFSET@',str(offset)).encode()
 new=len(data)+1
 if new==offset:break
 offset=new
with output.open('wb') as stream:
 stream.write(data)
 with image.open('rb') as source:
  import shutil;shutil.copyfileobj(source,stream)
output.chmod(0o755)
