#!/usr/bin/env python3
"""Collect Ubuntu source packages and copyright notices for deployed libraries."""
import json, pathlib, shutil, subprocess, sys
appdir, dest = map(pathlib.Path, sys.argv[1:])
lookup = {}
for line in subprocess.check_output(['ldconfig', '-p'], text=True).splitlines():
    if ' => ' in line:
        path = line.split(' => ')[1].strip()
        lookup.setdefault(pathlib.Path(path).name, path)
packages = set()
manifest = []
for lib in sorted((appdir / 'usr/lib').rglob('*.so*')):
    if lib.name.startswith('libwx'):
        manifest.append({'library': lib.name, 'source': 'wxWidgets source included in archive'})
        continue
    host = lookup.get(lib.name)
    if not host:
        raise RuntimeError(f'Cannot identify source package for {lib}')
    owned = None
    for candidate in [host, str(pathlib.Path(host).resolve())]:
        query = subprocess.run(['dpkg-query', '-S', candidate], text=True, capture_output=True)
        if query.returncode == 0:
            owned = query.stdout.split(': ')[0]
            break
    if not owned:
        raise RuntimeError(f'Cannot identify owner of {host}')
    source = subprocess.check_output(['dpkg-query', '-W', '-f=${source:Package}=${source:Version}', owned], text=True)
    packages.add(source)
    manifest.append({'library': lib.name, 'binary_package': owned, 'source_package': source})
    notice = pathlib.Path('/usr/share/doc') / owned.split(':')[0] / 'copyright'
    if notice.exists():
        target = appdir / 'usr/share/doc/bundled-libraries' / (owned.split(':')[0] + '-copyright')
        shutil.copyfile(notice, target)
for source in sorted(packages):
    subprocess.run(['apt-get', 'source', '--download-only', source], cwd=dest, check=True)
(appdir / 'usr/share/doc/bundled-libraries/manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
(dest / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
