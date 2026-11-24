import os, pathlib, subprocess, sys, time
launcher = pathlib.Path(sys.argv[1]).resolve()
env = dict(os.environ, XDG_CONFIG_HOME=str(pathlib.Path('test-config').resolve()), XDG_CACHE_HOME=str(pathlib.Path('test-cache').resolve()))
with open('launch-test.log', 'w') as log:
    app = subprocess.Popen([str(launcher)], env=env, stdout=log, stderr=log)
    try:
        for _ in range(60):
            if app.poll() is not None:
                raise RuntimeError(f'Audacity exited with {app.returncode}')
            windows = subprocess.run(['xdotool', 'search', '--onlyvisible', '--pid', str(app.pid)], text=True, capture_output=True)
            if windows.returncode == 0:
                titles = [subprocess.check_output(['xdotool', 'getwindowname', window], text=True).strip() for window in windows.stdout.split()]
                if any('Audacity' in title for title in titles):
                    print('Visible Audacity window:', titles)
                    time.sleep(5)
                    subprocess.run(['import', '-window', 'root', 'launch-test.png'], check=True)
                    break
            time.sleep(1)
        else:
            raise RuntimeError('No visible Audacity window within 60 seconds')
    finally:
        app.terminate()
        app.wait(timeout=15)
assert pathlib.Path('test-config/audacity-3.0.2/audacity.cfg').exists(), 'Isolated settings not created'
