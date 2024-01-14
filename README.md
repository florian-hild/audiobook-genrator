# Audiobook generator
Change layout of audiobook files structure and set ID3 tags.

## Setup:
```bash
git clone https://github.com/florian-hild/audiobook-genrator
cd audiobook-genrator
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

##### Offline installation
```bash
# On local system
source .venv/bin/activate
mkdir pip_local
python3 -m pip wheel --wheel-dir=pip_local/ -r requirements.txt
rsync -rv pip_local nas:audiobook-genrator/

# On remote system
git clone https://github.com/florian-hild/audiobook-genrator
cd audiobook-genrator
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --no-index --find-links=pip_local/ -r requirements.txt
```

## Example:
```bash
source ~/audiobook-genrator/.venv/bin/activate
alias audiobook-genrator='/root/audiobook-genrator/audiobook-generator.py'
cd /data/audiobooks/work/Niffenegger_Audrey_Die_Zwillinge_von_Highgate
mkdir -p '/data/audiobooks/library/Audrey Niffenegger/2009 - Die Zwillinge von Highgate'
audiobook-genrator -i . -o '/data/audiobooks/library/Audrey Niffenegger/2009 - Die Zwillinge von Highgate' -p Niffenegger_Die_Zwillinge_von_Highgate --author 'Audrey Niffenegger' --album 'Die Zwillinge von Highgate' -y 2009 -v
```

## License
See repository license file.