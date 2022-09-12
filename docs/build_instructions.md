# Build the documentation

To build the documentation, you need to:

- clone the repository `git clone https://github.com/twiinit/pyturbo.git` (or SSH variant)
- go to the `docs` directory `cd pyturbo/docs`
- create a `conda` environment with required dependencies `micromamba create -f ../environment-dev.yml` or activate existing one `micromamba activate pyturbo`
- run the `sphinx` command `sphinx-build -b html -d _build/doctrees ./source _build`
