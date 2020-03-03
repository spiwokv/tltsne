# tltsne

Time-lagged t-SNE of molecular trajectories. 

## Usage

```
usage: tltsne [-h] [-i INFILE] [-p INTOP] [-o OUTFILE] [-nofit NOFIT]
              [-lagtime LAGTIME] [-pcadim PCADIM] [-ticadim TICADIM]
              [-maxpcs MAXPCS] [-ncomp NCOMP] [-perplex1 PERPLEX1]
              [-perplex2 PERPLEX2] [-rate RATE] [-niter NITER] [-exag EXAG]

Time-lagged t-SNE of simulation trajectories, requires scimpy, pyemma, sklearn
and mdtraj

optional arguments:
  -h, --help          show this help message and exit
  -i INFILE           Input trajectory in pdb, xtc, trr, dcd, netcdf or mdcrd
                      of atoms to be analyzed. No jumps in PBC allowed.
  -p INTOP            Input topology in pdb with atoms to be analyzed.
  -o OUTFILE          Output file.
  -nofit NOFIT        Structure is NOT fit to reference topology if nofit is
                      set to 1 (default 0).
  -lagtime LAGTIME    Lag time in number of frames (default 1).
  -pcadim PCADIM      Number o PCA coordinates to be printed (defaut 2).
  -ticadim TICADIM    Number o TICA coordinates to be printed (defaut 2).
  -maxpcs MAXPCS      Number of TICA coordinates to be passed to t-SNE
                      (default 50).
  -ncomp NCOMP        Number of t-SNE and time-lagged t-SNE coordinates to be
                      printed (defaut 2).
  -perplex1 PERPLEX1  Perplexity of t-SNE (default 10.0
  -perplex2 PERPLEX2  Perplexity of time-lagged t-SNE (default 10.0
  -rate RATE          Learnning rate of t-SNE and time-lagged t-SNE (default
                      200.0).
  -niter NITER        Number of iterations of t-SNE and time-lagged t-SNE
                      (default 1000).
  -exag EXAG          Early exaggeration of t-SNE and time-lagged t-SNE
```

## Install




