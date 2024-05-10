Kartei is a simple, CLI-based vocabulary trainer.

## CLI

Currently only one argument (a path to a kartei file) is available.

```
$ kartei -h
usage: kartei [-h] file

Kartei Vocabulary Trainer

positional arguments:
  file        path to file

options:
  -h, --help  show this help message and exit
```

## File format

The plaintext file which is read by kartei must consist of one word pair per line and must be separated by two equal signs.

`<shown word> == <translation>`

The left hand is the shown word and the right hand will be revealed after your guess.

You can add some metadata by adding key=value pairs after a hash sign. Currently this isn't used anywhere, but it might be useful to indicate or filter difficult words. 

`<shown word> == <translation>  # key=value`
