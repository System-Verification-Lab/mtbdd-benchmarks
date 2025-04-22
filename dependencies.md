## 1. Install dependencies + compile (when not using the Docker image)

1. Clone this repository including its submodules.
```shell
$ git clone --recurse-submodules <this repo's url>
```

2. Install basic build tools.
```shell
$ sudo apt install build-essential cmake autoconf
```

3. Install dependencies.
```shell
$ sudo apt install libpopt-dev libgmp-dev libmpfr-dev libmpc-dev
```

4. Install Python libraries (creating a virtual environment is optional but recommended).
```shell
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

5. After installing the dependencies above, Q-Sylvan can be compiled with the following (adding `-r` will recompile everything, i.e. first remove previously compiled files).
```shell
$ ./compile_all.sh -q
```
