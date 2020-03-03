name = "tltsne"

libnames = [('mdtraj', 'md'), ('scipy', 'sp'), ('argparse', 'arg'), ('datetime', 'dt'), ('sys', 'sys')]

for (name, short) in libnames:
  try:
    lib = __import__(name)
  except ImportError:
    print("Library %s cannot be loaded, exiting" % name)
    exit(0)
  else:
    globals()[short] = lib

try:
  import sklearn.manifold as sk
except ImportError:
  print("Library sklearn.manifold is not installed, exiting")
  exit(0)
try:
  import pyemma.coordinates as coor
except ImportError:
  print("Library pyemma.coordinates is not installed, exiting")
  exit(0)
try:
  import scipy.spatial as spat
except ImportError:
  print("Library scipy.spatial is not installed, exiting")
  exit(0)


def dotltsne(infilename='', intopname='', nofit=0, lagtime=1, pcadim=2, ticadim=2,
             maxpcs=50, ncomp=2, perplex1=10.0, perplex2=10.0, exag=12.0,
             rate=200.0, niter=1000, command='', ofilename='out.txt'):
  # Reading and superimposing the trajectory
  try:
    print("Loading trajectory")
    refpdb = md.load_pdb(intopname)
    X = md.load(infilename, top=intopname)
    print("Fitting trajectory")
    if nofit!=1:
      X.superpose(refpdb)
  except IOError:
    print("Cannot load %s or %s, exiting." % (infilename, intopname))
    exit(0)
  else:
    print("%s succesfully loaded and fitted" % X)
  print("")

  # Conversion of trajectory into matrix
  Xt = sp.zeros((X.n_frames, 3*X.n_atoms))
  for i in range(X.n_frames):
    for j in range(X.n_atoms):
      Xt[i,3*j] = X.xyz[i,j,0]
      Xt[i,3*j+1] = X.xyz[i,j,1]
      Xt[i,3*j+2] = X.xyz[i,j,2]

  # PCA
  print("Runing PCA")
  T = X.n_frames
  if lagtime > T:
    print("Lag time higher than the number of frames, exiting.")
    exit(0)
  pca = coor.pca(data = Xt)
  projs_pca = pca.get_output()

  # TICA
  print("Runing TICA")
  tica = coor.tica(data = Xt, lag=lagtime, dim=ticadim)
  projs_tica = tica.get_output()

  # t-SNE
  print("Runing t-SNE")
  Xembtsne = sk.TSNE(n_components=ncomp, perplexity=perplex1,
                     early_exaggeration=exag, learning_rate=rate, n_iter=niter,
                     metric="euclidean").fit_transform(Xt)

  # time-lagged t-SNE
  print("Runing time-lagged t-SNE")
  Xm = Xt-sp.mean(Xt, axis=0)
  Xc = sp.cov(sp.transpose(Xm))
  eva, eve = sp.linalg.eig(Xc)
  order=sp.argsort(eva)[::-1]
  eve = eve[:,order]
  eva = eva[order]
  projs = Xm.dot(eve)
  projs = projs/sp.sqrt(eva)
  C1 = sp.transpose(projs[:-lagtime,]).dot(projs[lagtime:,])/(T-lagtime-1)
  C1 = (C1+sp.transpose(C1))/2
  eva2, eve2 = sp.linalg.eig(C1)
  order=sp.argsort(eva2)[::-1]
  eve2 = eve2[:,order]
  eva2 = eva2[order]
  projs = projs.dot(eve2[:,:maxpcs])
  projs = projs*sp.real(eva2[:maxpcs])
  Xd = spat.distance_matrix(projs, projs)
  Xembtltsne = sk.TSNE(n_components=ncomp, perplexity=perplex2,
                       early_exaggeration=exag, learning_rate=rate, n_iter=niter,
                       metric="precomputed").fit_transform(Xd)

  # Saving results
  print("Saving results")
  ofile = open(ofilename, 'w')
  ofile.write("# Command: %s\n" % command)
  if(nofit==0):
    ofile.write("# structures were superimposed onto reference structure\n")
  else:
    ofile.write("# structures were NOT superimposed onto reference structure\n")
  ofile.write("# lag time set to %i frames\n" % lagtime)
  ofile.write("# output dimension for PCA set to %i\n" % pcadim)
  ofile.write("# output dimension for TICA set to %i\n" % ticadim)
  ofile.write("# number of top principle components passed to time-lagged t-SNE set to %i\n" % maxpcs)
  ofile.write("# output dimension for t-SNE and time-lagged t-SNE set to %i\n" % ncomp)
  ofile.write("# perplexity of t-SNE set to %f\n" % perplex1)
  ofile.write("# perplexity of time-lagged t-SNE set to %f\n" % perplex2)
  ofile.write("# early_exaggeration set to %f\n" % exag)
  ofile.write("# structure_ID")
  for j in range(pcadim):
    ofile.write(" PCA%i" % (j+1))
  for j in range(ticadim):
    ofile.write(" TICA%i" % (j+1))
  for j in range(ncomp):
    ofile.write(" tSNE%i" % (j+1))
  for j in range(ncomp):
    ofile.write(" tltSNE%i" % (j+1))
  ofile.write("\n")
  for i in range(T):
    output = " %i" % (i+1)
    for j in range(pcadim):
      output = output + " %f" % projs_pca[0][i,j]
    for j in range(ticadim):
      output = output + " %f" % projs_tica[0][i,j]
    for j in range(ncomp):
      output = output + " %f" % Xembtsne[i,j]
    for j in range(ncomp):
      output = output + " %f" % Xembtltsne[i,j]
    ofile.write("%s\n" % output)
  ofile.close()

