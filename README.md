# What's this?
This tool generates language history data for every commit in your repository.
It uses `github-linguist` to generate the language stats.

# How to use
Build the Docker image:
```bash
docker build -t langhisto .
```

Run the program: 
```bash
docker run -t --rm -v /path/to/your/repository:/repo langhisto
```
