# mini-rag

This is a minimal implementation of the RAG model for question answering.

## Requirements

- Python 3.8 or later

#### Install Python using MiniConda

1) Download and install MiniConda from [here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install)
2) Create a new environment using the following command:
```bash
$ conda create -n mini-rag python=3.8
```
3) Activate the environment:
```bash
$ conda activate mini-rag
```

### (Optional) Setup you command line interface for better readability

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## Installation

### Install the required packages

```bash
$ pip install -r requirements.txt
```

### Setup the environment variables

```bash
$ cp src/.env.example src/.env
```

Set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value.

## Run Docker Compose Services

```bash
$ cd docker
$ cp .env.example .env
```

- update `.env` with your credentials



```bash
$ cd docker
$ sudo docker compose up -d
```

## Run the FastAPI server

```bash
$ cd src
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

Set your environment variables in the `src/.env` file. Like `OPENAI_API_KEY` value.

### Ollama on Windows with the API running in WSL

When WSL uses its default NAT networking, find the Windows host address from WSL:

```bash
ip route show default
```

Use the address after `via` in `src/.env`, for example:

```dotenv
GENERATION_BACKEND=OLLAMA
EMBEDDING_BACKEND=OLLAMA
OLLAMA_API_URL="http://172.31.0.1:11434"
```

That address can change after WSL restarts. Ollama on Windows normally listens only on `127.0.0.1`. To accept connections from WSL, set the **Windows Ollama server** environment variable `OLLAMA_HOST` to `0.0.0.0:11434`, then quit Ollama from the Windows system tray and start it again. This listens on all Windows interfaces, so restrict port 11434 with Windows Firewall if the machine is on a network you do not trust. `OLLAMA_API_URL` is the app's client setting; it does not change where the Ollama server listens.

Verify connectivity from WSL before starting the API:

```bash
curl --noproxy '*' "http://$(ip route show default | awk '{print $3}'):11434/api/tags"
```

If the request still times out, check Windows Firewall for inbound connections to Ollama on port 11434. When Ollama runs inside WSL, or WSL is configured for mirrored networking, use `OLLAMA_API_URL="http://127.0.0.1:11434"` instead.

