import os
import shutil

indir = os.path.join('..', 'assets')
outdir = os.path.join(indir, 'swe')
if not os.path.exists(outdir):
    os.mkdir(outdir)
indirs = [dir for dir in os.listdir(indir) if '2100' in dir]
for dir in indirs:
    inpath = os.path.join(indir, dir)
    outpath = os.path.join(outdir, dir)
    shutil.move(inpath, outdir)
    print('Moved: {} --> {}'.format(inpath, outdir))

print('Complete!')
