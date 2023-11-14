# What's this?

This tool generates language history data for every commit in your repository.
It uses `github-linguist` to generate the language stats.

# How to use

## Generate statistics history

```
usage: main.py [-h] [-s SKIP_INTERVAL] [-o OUTPUT_FILE] REPO

Generate the history of the number of lines of code for each language in a given repository.

positional arguments:
  REPO                  path to the repository

options:
  -h, --help            show this help message and exit
  -s SKIP_INTERVAL, --skip-interval SKIP_INTERVAL
                        interval of commits to skip (default: 5)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        File to append CSV output to
```

Build the Docker image:

```bash
docker build -t langhisto .
```

Run the program:

```bash
docker run -t \
    -v "/mnt/dev/path/to/repo:/repo" \
    -v "/mnt/dev/scripts/langhisto/out:/out" \
    langhisto \
    -o /out/langstats.csv \
    /repo
```

## Show graph from history

```
usage: main.py [-h] filename

Plot language statistics from a CSV file

positional arguments:
  filename    Input CSV file name

options:
  -h, --help  show this help message and exit
```

```
./display-stats/main.py out/langstats.csv
```
