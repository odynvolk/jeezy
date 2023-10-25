# jeezy

A LLaMA 2 powered summariser

## Prerequisites:

### LLaMA 2 model

You need a LLaMA 2 model in GGML format. You can find quite a few through [TheBloke on HuggingFace](https://huggingface.co/TheBloke)
who has done an enormous service to the community by converting different models to GGML and quantized them. Pick one that suits your
needs and hardware requirements.

### Python

You need Python 3 on your machine.

- Miniconda (optional)

For handling the packages needed for different enivronments.

```bash
$ curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -o Miniconda3-latest-MacOSX-arm64.sh
$ chmod +x Miniconda3-latest-MacOSX-arm64.sh
$ ./Miniconda3-latest-MacOSX-arm64.sh -b -p $HOME/miniconda
$ source ~/miniconda/bin/activate
```

- LLaMA 2 etc

For using LLaMA 2 models etc

```bash
$ pip install -r requirements.txt
```

## Configuration

Create a `.env` file with the following properties.
