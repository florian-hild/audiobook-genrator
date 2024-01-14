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

## Usage:
```bash
# ./audiobook-generator.py --help
usage: audiobook-genrator [options]

Order audiobook and add ID3 tags.

options:
  -V, --version         Print version number and exit.
  -h, --help            Print a short help page describing the options available and exit.
  -v, --verbose         Verbose mode. Print debug messages. Multiple -v options increase the verbosity. The maximum is 3.
  -i INPUT, --input INPUT
                        Path to audiobook source
  -o OUTPUT, --output OUTPUT
                        Path to audiobook destination
  -p PREFIX, --prefix PREFIX
                        Filename prefix. (e.g. Kluftinger_12_Affenhitze)
  --author AUTHOR       Author name
  --album ALBUM         Album name
  -y YEAR, --year YEAR  Publishing year
  --series SERIES       Series Name
  --asin ASIN           Amazon / Audible Standard Identification Number (e.g. B09X7FS3ZC)
  --genre GENRE         Genre
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