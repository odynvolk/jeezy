# jeezy

A video viewer

## Prerequisites:

### Python

You need Python 3 on your machine.

- Micromamba (optional)

For handling the packages needed for different enivronments. Easy to install with asdf.

```bash
$ asdf install
$ micromamba create -n jeezy python=3.13
$ micromamba activate jeezy
```

- Nodriver

For using Chrome undetected

```bash
$ pip install -r requirements.txt
```

## Configuration

Create a `.env` file with the following properties.

```
TIMES=5
STAY_ON_PAGE_IN_MINUTES=20
SLEEP_BETWEEN_RUNS_IN_MINUTES=60
USER_AGENTS=<path-to-file-with-user-agents>
URLS=<path-to-file-with-urls>

## Usage

Start the application:

```bash
python ./jeezy/app.py
```
