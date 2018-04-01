# PlumedWrapper

... or simply pyPlumed. I work with GROMACS and Plumed2 simulations a lot.
Aside from GROMACS trajectories, there are the text-based Plumed2 trajectories.
This library allows these files to be read-in as pandas DataFrame objects, making manipulation easier.

## Installation

Clone the repo and install using

```bash
git clone https://github.com/jandom/PlumedWrapper.git
cd PlumedWrapper
python setup.py
```

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

### Reading WHAM window energies

## Examples

### Compute per-frame free-energy
