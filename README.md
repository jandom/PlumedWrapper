TODOS
- adding the TPS code here

# PlumedWrapper

... or simply pyPlumed. I work with GROMACS and Plumed2 simulations a lot.
Aside from GROMACS trajectories, there are the text-based Plumed2 trajectories.
This library allows these files to be read-in as pandas DataFrame objects, making manipulation easier.

[![Build Status](https://travis-ci.org/jandom/PlumedWrapper.svg?branch=master)](https://travis-ci.org/jandom/PlumedWrapper)

## Installation

Clone the repo and install using

```bash
git clone https://github.com/jandom/PlumedWrapper.git
cd PlumedWrapper
python setup.py
```

## Examples

Below is a single most useful example for analyzing Umbrella Sampling (US) simulations.

### Compute per-frame free-energy

Using a WHAM free energy profile estimated from an Umbrella Sampling simulation, we can calculate the free-energy per-frame. This free energy per-frame is simply a sum of:

- the free energy of the window,
- bias energy, as recorded for the frame.

The typical setup is a 10-replica simulation: 10 windows generate 10 trajectories.

```python
In [1]: import plumed

In [2]: import glob

In [2]: import pandas as pd

In [2]: import numpy as np

In [3]: sorted(glob.glob("COLVAR.?"))
Out[3]:
['COLVAR.0',
 'COLVAR.1',
 'COLVAR.2',
 'COLVAR.3',
 'COLVAR.4',
 'COLVAR.5',
 'COLVAR.6',
 'COLVAR.7',
 'COLVAR.8',
 'COLVAR.9']

In [4]: file = sorted(glob.glob("COLVAR.?"))

In [5]: data = [(f, plumed.read_colvar(f)) for f in files]

In [6]: windows = plumed.read_fes("result_128_0.001_5.dat")

In [7]: windows
Out[7]:
    Window        Free       +/-
0        0    0.000000  0.000000
1        1   -2.962629  0.009029
2        2   -0.819930  0.016131
3        3    6.424908  0.020912
4        4   18.764319  0.023116
5        5   36.184953  0.023431
6        6   58.665439  0.024853
7        7   86.073163  0.032630
8        8  108.772854  0.067440
9        9  118.034358  0.115036

In [8]: for f, df in data:
  df["window.bias"] = windows["Free"].values[int(f.split("COLVAR.")[-1])]

In [9]: df = pd.concat(zip(*data)[1])

In [10]: beta = 1/(2.479 * 310./300.)

In [11]: df["weights"] = np.exp(-beta*(df["window.bias"] - df["restraint.bias"]))

```

See this paper, eq. 2 https://www.sciencedirect.com/science/article/pii/S0010465500002150

## Usage

### Reading a collective variable file COLVAR

Assume you have the following COLVAR file

```bash
$ head COLVAR
#! FIELDS time v.x v.y v.z d.x d.y d.z d2 dist distances.min restraint.bias restraint.force2
 0.000000 -1.640806 -0.290569 -1.760758 -3.798299 2.503861 -3.303975 10.916252 3.303975 0.473081 2.670422 5340.844815
 29.999999 -1.629709 -0.424727 -1.784937 2.824048 -2.400719 -3.358084 11.276729 3.358084 0.501038 5.104302 10208.604324
 59.999999 -1.647561 -0.734689 -1.649616 -4.166563 -1.607917 -3.353104 11.243305 3.353104 0.476641 2.936907 5873.814045
 89.999998 -1.665416 -0.676483 -1.562421 2.269357 0.283753 -3.245199 10.531320 3.245199 0.483370 3.475311 6950.622491
 119.999997 -1.494495 -0.860597 -1.670672 -1.451372 -2.115068 -3.341465 11.165386 3.341465 0.482442 3.398304 6796.608996
 149.999997 -1.612333 -0.856558 -1.413775 3.040517 2.787686 -3.321970 11.035486 3.321970 0.489207 3.978927 7957.854806
 179.999996 -1.460117 -0.552365 -1.879782 -3.797217 1.850908 -3.295563 10.860736 3.295563 0.483233 3.463835 6927.669979
 209.999995 -1.433626 -0.428419 -1.894602 -4.212299 -2.234372 -3.327392 11.071540 3.327392 0.482861 3.432947 6865.894313
 239.999995 -1.433039 -0.334814 -1.950592 2.886008 -0.180834 -3.351645 11.233523 3.351645 0.483527 3.488397 6976.794135
```

You can read it into a DataFrame

```python
In [1]: import plumed

In [2]: df = plumed.read_colvar("COLVAR")

In [3]: df.head()
Out[3]:
    time       v.x       v.y       v.z       d.x       d.y       d.z  \
0    0.0 -1.640806 -0.290569 -1.760758 -3.798299  2.503861 -3.303975   
1   30.0 -1.629709 -0.424727 -1.784937  2.824048 -2.400719 -3.358084   
2   60.0 -1.647561 -0.734689 -1.649616 -4.166563 -1.607917 -3.353104   
3   90.0 -1.665416 -0.676483 -1.562421  2.269357  0.283753 -3.245199   
4  120.0 -1.494495 -0.860597 -1.670672 -1.451372 -2.115068 -3.341465   

          d2      dist  distances.min  restraint.bias  restraint.force2  
0  10.916252  3.303975       0.473081        2.670422       5340.844815  
1  11.276729  3.358084       0.501038        5.104302      10208.604324  
2  11.243305  3.353104       0.476641        2.936907       5873.814045  
3  10.531320  3.245199       0.483370        3.475311       6950.622491  
4  11.165386  3.341465       0.482442        3.398304       6796.608996  
```

### Reading a WHAM free energy profile

Suppose you have a WHAM file like this

```bash
$ head wham_result.dat
#Coor		Free	+/-		Prob		+/-
0.427930	inf	-nan	0.000000	0.000000
0.432227	17.503672	1.274852	0.000341	0.000167
0.436523	17.500549	-nan	0.000342	0.000232
0.440820	13.467288	0.586424	0.001366	0.000275
0.445117	10.810190	0.141913	0.003403	0.000202
0.449414	9.289215	0.382910	0.005739	0.000667
#Window		Free	+/-
#0	0.000000	0.000000
#1	-2.976647	0.010652
```

To load the free energy profile into python

```python
In [1]: import plumed

In [2]: df = plumed.read_wham("wham_result.dat")

In [3]: df.head()
Out[3]:
       Coor       Free   FreeErr      Prob   ProbErr
0  0.427930        inf       NaN  0.000000  0.000000
1  0.432227  17.503672  1.274852  0.000341  0.000167
2  0.436523  17.500549       NaN  0.000342  0.000232
3  0.440820  13.467288  0.586424  0.001366  0.000275
4  0.445117  10.810190  0.141913  0.003403  0.000202
```

### Reading WHAM window energies

Suppose you have a WHAM result file for a simulation run with 16 windows, looking something like this

```bash
$ tail wham_result.dat
#Window		Free	+/-
#0	0.000000	0.000000
#1	-2.976647	0.010652
...
#6	58.650331	0.026025
#7	86.074917	0.031203
#8	108.786612	0.069581
#9	118.055129	0.119232
#10	119.295804	0.173617
#11	119.326201	0.152721
#12	119.399530	0.146030
#13	119.844711	0.187421
#14	120.466334	0.189525
#15	122.303841	0.206086

```

To load the window energies into python

```python
In [1]: import plumed

In [2]: df = plumed.read_fes("wham_result.dat")

In [3]: df
Out[3]:
    Window        Free       +/-
0        0    0.000000  0.000000
1        1   -2.976647  0.010652
2        2   -0.843520  0.018557
3        3    6.396160  0.023641
4        4   18.734943  0.025849
5        5   36.159876  0.025815
6        6   58.650331  0.026025
7        7   86.074917  0.031203
8        8  108.786612  0.069581
9        9  118.055129  0.119232
10      10  119.295804  0.173617
11      11  119.326201  0.152721
12      12  119.399530  0.146030
13      13  119.844711  0.187421
14      14  120.466334  0.189525
15      15  122.303841  0.206086
```
