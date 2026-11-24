import os, pathlib, subprocess, sys, time, wave, math, struct
launcher = pathlib.Path(sys.argv[1]).resolve()
env = dict(os.environ, XDG_CONFIG_HOME=str(pathlib.Path('test-config').resolve()), XDG_CACHE_HOME=str(pathlib.Path('test-cache').resolve()))
settings = pathlib.Path(env['XDG_CONFIG_HOME']) / 'audacity-3.0.2'
settings.mkdir(parents=True, exist_ok=True)
(settings / 'audacity.cfg').write_text('[GUI]\nShowSplashScreen=0\n')
test_audio = pathlib.Path('audacity-portable-test.wav').resolve()
with wave.open(str(test_audio), 'wb') as audio:
    audio.setparams((1, 2, 44100, 0, 'NONE', 'not compressed'))
    audio.writeframes(b''.join(struct.pack('<h', round(5000 * math.sin(2 * math.pi * 440 * i / 44100))) for i in range(44100)))
with open('launch-test.log', 'w') as log:
    app = subprocess.Popen([str(launcher), str(test_audio)], env=env, stdout=log, stderr=log)
    try:
        for _ in range(90):
            if app.poll() is not None:
                raise RuntimeError(f'Audacity exited with {app.returncode}')
            windows = subprocess.run(['xdotool', 'search', '--onlyvisible', '--pid', str(app.pid)], text=True, capture_output=True)
            if windows.returncode == 0:
                titles = [subprocess.check_output(['xdotool', 'getwindowname', window], text=True).strip() for window in windows.stdout.split()]
                if any('audacity-portable-test' in title for title in titles):
                    print('Imported WAV in visible Audacity editor:', titles)
                    time.sleep(5)
                    subprocess.run(['import', '-window', 'root', 'launch-test.png'], check=True)
                    break
            time.sleep(1)
        else:
            raise RuntimeError('No imported test waveform window within 90 seconds')
    finally:
        app.terminate()
        app.wait(timeout=15)
assert pathlib.Path('test-config/audacity-3.0.2/audacity.cfg').exists(), 'Isolated settings not created'
