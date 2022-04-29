<h1 align="center">Simple Slurm Command</h1>
<p align="center">A simple Python wrapper for Slurm with flexibility in mind<p>
<p align="center">
<a href="https://github.com/amq92/simple_slurm_command/actions/workflows/python-publish-pypi.yml">
    <img src="https://github.com/takuma-yoneda/simple_slurm_command/actions/workflows/python-publish-pypi.yml/badge.svg" alt="Publish to PyPI" />
</a>
<!-- <a href="https://github.com/amq92/simple_slurm/actions/workflows/python-package-conda.yml"> -->
<!--     <img src="https://github.com/amq92/simple_slurm/actions/workflows/python-package-conda.yml/badge.svg" alt="Publish to Conda" /> -->
<!-- </a> -->
<a href="https://github.com/takuma-yoneda/simple_slurm_command/actions/workflows/python-run-tests.yml">
    <img src="https://github.com/takuma-yoneda/simple_slurm_command/actions/workflows/python-run-tests.yml/badge.svg" alt="Run Python Tests" />
</a>
</p>

This is a fork of [amq92/simple_slurm](https://github.com/amq92/simple_slurm/).
If you are interested in using this repository, I would strongly encourage you to check out the original version first.

The only difference is that this version only produces a slurm command, whereas the original simple_slurm produces and *execute the command* assuming that slurm is available on the host machine it runs on.
