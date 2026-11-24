#!/usr/bin/env python3
"""Bundle the complete ELF dependency closure except the platform C runtime."""
from pathlib import Path
import os,re,shutil,subprocess,sys
app=Path(sys.argv[1]).resolve();libdir=app/'usr/lib'
base={'libc.so.6','libm.so.6','libdl.so.2','libpthread.so.0','librt.so.1','libresolv.so.2','libutil.so.1','libanl.so.1','ld-linux-x86-64.so.2'}
env=dict(os.environ,LD_LIBRARY_PATH=str(libdir)+':'+str(libdir/'audacity'))
# ALSA loads configuration and PulseAudio integration dynamically, not via ELF dependencies.
alsa_config=app/'usr/share/alsa'
shutil.copytree('/usr/share/alsa',alsa_config,dirs_exist_ok=True)
alsa_plugins=libdir/'alsa-lib';alsa_plugins.mkdir(parents=True,exist_ok=True)
for name in ['libasound_module_pcm_pulse.so','libasound_module_ctl_pulse.so']:
 shutil.copyfile(Path('/usr/lib/x86_64-linux-gnu/alsa-lib')/name,alsa_plugins/name)
seen=set();queue=[app/'usr/bin/audacity']+list(libdir.rglob('*.so*'))+list((app/'usr/share/audacity/modules').glob('*.so'))
while queue:
 file=queue.pop()
 if not file.is_file() or str(file) in seen:continue
 seen.add(str(file))
 result=subprocess.run(['ldd',str(file)],env=env,text=True,capture_output=True)
 if 'not found' in result.stdout:raise RuntimeError(result.stdout)
 for name,path in re.findall(r'^\s*(\S+) => (/\S+)',result.stdout,re.M):
  if name in base or name.startswith('libnss_'):continue
  target=libdir/name
  if not target.exists():
   shutil.copyfile(Path(path).resolve(),target)
   print('Bundled',name)
  queue.append(target)
fontdir=app/'usr/share/fonts';fontdir.mkdir(parents=True,exist_ok=True)
for name in ['DejaVuSans.ttf','DejaVuSans-Bold.ttf','DejaVuSansMono.ttf']:
 shutil.copyfile(Path('/usr/share/fonts/truetype/dejavu')/name,fontdir/name)
config=app/'usr/share/fontconfig/fonts.conf';config.parent.mkdir(parents=True,exist_ok=True)
config.write_text('''<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig><dir prefix="relative">../fonts</dir><cachedir prefix="xdg">audacity-3.0.2/fontconfig</cachedir><alias><family>sans-serif</family><prefer><family>DejaVu Sans</family></prefer></alias><alias><family>monospace</family><prefer><family>DejaVu Sans Mono</family></prefer></alias></fontconfig>
''')
