#!/usr/bin/env python3
"""Collect installation metadata only. Never read config contents or credentials."""
import datetime, json, os, pathlib, platform, shutil, subprocess
from zoneinfo import ZoneInfo
ROOT = pathlib.Path(__file__).resolve().parents[1]
HOME = pathlib.Path.home()
def run(args):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=60, env={**os.environ, 'HOMEBREW_NO_AUTO_UPDATE':'1'})
        return p.stdout.strip() if p.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None
def names(path):
    try: return sorted(p.name for p in path.iterdir() if not p.name.startswith('.'))
    except OSError: return []
def display(p): return str(p).replace(str(HOME), '~', 1)
apps = []
for base in [pathlib.Path('/Applications'), HOME/'Applications']:
    if not base.exists(): continue
    for current, dirs, files in os.walk(base):
        depth = len(pathlib.Path(current).relative_to(base).parts)
        for name in list(dirs):
            if name.endswith('.app'):
                apps.append(display(pathlib.Path(current)/name)); dirs.remove(name)
        if depth >= 2: dirs[:] = []
brew = shutil.which('brew')
brew_data = run([brew, 'info', '--json=v2', '--installed']) if brew else None
try: brew_data = json.loads(brew_data or '{}')
except ValueError: brew_data = {}
formulae = [{k:f.get(k) for k in ['name','full_name','installed_on_request']} for f in brew_data.get('formulae',[])]
casks = [{'token':c['token'], 'name':c.get('name',[]), 'version':c.get('version')} for c in brew_data.get('casks',[])]
npm = run(['npm','list','-g','--depth=0','--json'])
try: npm = {k:v.get('version') for k,v in json.loads(npm or '{}').get('dependencies',{}).items()}
except ValueError: npm = {}
configs = ['.zshrc','.zprofile','.bash_profile','.profile','.gitconfig','.tmux.conf','.simplebarrc','.config/git','.config/aerospace','.config/ghostty','.config/karabiner','.config/nvim','.config/raycast','.config/btop','.config/iterm2','.config/mac-dev-setup','.agents/skills','.codex/skills','.claude/skills','Library/Application Support/Code/User/settings.json','Library/Application Support/Code/User/keybindings.json','Library/Application Support/Code/User/snippets']
extensions = []
for p in (HOME/'.vscode/extensions').glob('*/package.json'):
    try:
        d=json.loads(p.read_text()); extensions.append({'id':d['publisher']+'.'+d['name'],'version':d.get('version')})
    except (OSError,ValueError,KeyError): pass
prefs = {}
for domain,key in [('NSGlobalDomain','AppleInterfaceStyle'),('NSGlobalDomain','AppleShowAllExtensions'),('NSGlobalDomain','KeyRepeat'),('NSGlobalDomain','InitialKeyRepeat'),('com.apple.dock','autohide'),('com.apple.dock','orientation'),('com.apple.dock','tilesize'),('com.apple.finder','AppleShowAllFiles'),('com.apple.finder','ShowPathbar'),('com.apple.finder','ShowStatusBar')]:
    value=run(['defaults','read',domain,key]); prefs[domain+'.'+key]=value if value is not None else 'unset / default'
data={'scanned_at':datetime.datetime.now(ZoneInfo('America/Los_Angeles')).isoformat(),'macos':run(['sw_vers','-productVersion']),'architecture':platform.machine(),'applications':sorted(set(apps)),'homebrew_formulae':formulae,'homebrew_casks':casks,'homebrew_leaves':(run([brew,'leaves']) or '').splitlines() if brew else [],'global_npm_packages':npm,'config_candidates':[p for p in configs if (HOME/p).exists()], 'config_directory_names':names(HOME/'.config'),'vscode_extensions':sorted(extensions,key=lambda x:x['id']),'user_fonts':names(HOME/'Library/Fonts'),'user_launch_agents':names(HOME/'Library/LaunchAgents'),'runtime_managers_present':[p for p in ['.nvm','.pyenv','.rustup','.cargo','.bun','.gem','.cocoapods'] if (HOME/p).exists()],'xcode_developer_directory':run(['xcode-select','-p']),'macos_preferences':prefs,'scope':'Installation metadata and allowlisted preference values only. No credentials, config contents, browser profiles, personal documents, histories, or system-wide exhaustive inventory.'}
(ROOT/'inventory/machine.json').write_text(json.dumps(data,indent=2)+'\n')
print('Wrote inventory/machine.json')
