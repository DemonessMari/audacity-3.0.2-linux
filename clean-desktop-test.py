#!/usr/bin/env python3
"""Verify the no-FUSE launcher in the unmodified Ubuntu base container."""
from pathlib import Path
import os,subprocess,time,wave,struct,math
root=Path.cwd();test=root/'work/clean-test';test.mkdir(parents=True,exist_ok=True)
settings=test/'config/audacity-3.0.2';settings.mkdir(parents=True,exist_ok=True)
(settings/'audacity.cfg').write_text('[GUI]\nShowSplashScreen=0\n')
with wave.open(str(test/'clean-runtime-test.wav'),'wb') as audio:
 audio.setparams((1,2,44100,0,'NONE','not compressed'))
 audio.writeframes(b''.join(struct.pack('<h',round(5000*math.sin(2*math.pi*440*i/44100))) for i in range(44100)))
# No apt install or other changes are made inside this image.
subprocess.run(['docker','pull','ubuntu:22.04'],check=True)
audit=['docker','run','--rm','-v',str(root/'work/AppDir')+':/app:ro','ubuntu:22.04','sh','-c','test ! -e /dev/fuse; LD_LIBRARY_PATH=/app/usr/lib ldd /app/usr/bin/audacity > /tmp/dependencies; cat /tmp/dependencies; ! grep -q "not found" /tmp/dependencies']
subprocess.run(audit,check=True)
server=subprocess.Popen(['Xvfb',':98','-ac','-screen','0','1280x800x24'])
try:
 time.sleep(2)
 command=['docker','run','--rm','--name','audacity-clean-runtime','--user',f'{os.getuid()}:{os.getgid()}','-e','HOME=/tmp','-e','DISPLAY=:98','-e','XDG_CONFIG_HOME=/test/config','-e','XDG_CACHE_HOME=/test/cache','-v','/tmp/.X11-unix:/tmp/.X11-unix:ro','-v',str(root/'dist')+':/release:ro','-v',str(test)+':/test','ubuntu:22.04','/release/Audacity-3.0.2-linux-x86_64.run','/test/clean-runtime-test.wav']
 with (root/'work/clean-runtime.log').open('w') as log:
  app=subprocess.Popen(command,stdout=log,stderr=log)
  try:
   env=dict(os.environ,DISPLAY=':98')
   for _ in range(90):
    if app.poll() is not None:raise RuntimeError(f'Clean container exited {app.returncode}; see clean-runtime.log')
    found=subprocess.run(['xdotool','search','--onlyvisible','--name','clean-runtime-test'],env=env,capture_output=True,text=True)
    if found.returncode==0:
     time.sleep(5)
     if app.poll() is not None:raise RuntimeError('Exited after import')
     subprocess.run(['import','-window','root',str(root/'work/clean-runtime.png')],env=env,check=True)
     print('PASS: WAV imported in unmodified Ubuntu 22.04 base container without FUSE, GTK, FFmpeg, or extra packages installed.')
     break
    time.sleep(1)
   else:raise RuntimeError('No imported waveform within 90 seconds')
  finally:
   subprocess.run(['docker','stop','-t','3','audacity-clean-runtime'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   app.wait(timeout=15)
finally:
 server.terminate();server.wait(timeout=10)
