# Check python speed

research of checking speed of numpy for several systems


## How to reproduce

There are 3 ways to install `numpy`:

* *pip*
* *conda standart*
* *conda forge*

For all of them create conda environment:

```
conda create -n test_pip python==3.8.5

conda create -n test_conda python==3.8.5

conda create -n test_conda_f python==3.8.5

```

In every environment install `numpy` by:

* `test_pip`: `pip install numpy==1.21.2`
* `test_conda`: `conda install -c defaults numpy==1.21.2`
* `test_conda_f`: `conda install -c conda-forge numpy==1.21.2`

In each environment run command like:

```
python test.py pip

python test.py conda

python test.py conda_forge
```


How to remove all these envs:

```
conda remove --name test_pip --all

conda remove --name test_conda --all

conda remove --name test_conda_f --all
```
