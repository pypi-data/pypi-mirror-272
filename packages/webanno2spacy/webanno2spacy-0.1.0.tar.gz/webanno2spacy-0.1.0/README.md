# WebAnno ⟶ spaCy

A tool that helps you to convert the
[WebAnno TSV 3.2](https://webanno.github.io/webanno/releases/3.4.5/docs/user-guide.html#sect_webannotsv)
files to [spaCy](https://spacy.io)'s `Doc` format.

## Usage

```
$ poetry install
$ webanno2spacy --help
Usage: webanno2spacy [OPTIONS] SPACY_MODEL INPUT_TEXT_FILE INPUT_WEBANNO_FILE

Arguments:
  SPACY_MODEL         [required]
  INPUT_TEXT_FILE     [required]
  INPUT_WEBANNO_FILE  [required]

Options:
  --output-file PATH
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```

## TODO
- Implement batch conversion of multiple files to DocBin 
