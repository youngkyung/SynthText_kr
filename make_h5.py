import numpy as np
import h5py
import os, sys, traceback
import os.path as osp
# from visualize_depth import *
# import titan_utils as titu

import matplotlib
matplotlib.use('Agg')

from common import *
from synthgen import *
from PIL import Image

START_IMG_IDX = 4400
NUM_IMG = -1

INSTANCE_PER_IMAGE = 1
SECS_PER_IMG = 5 #max time per image in seconds

CONFIG_LOCAL = {'im_dir'   : 'bg_img',
                'depth_db' : 'depth.h5',
                'seg_db'   : 'seg.h5',
                'out_dir'  : 'gen',
                'data_dir' : 'data'}

def add_res_to_db(imgname, res, db):
    ninstance = len(res)
    for i in xrange(ninstance):
        dname = "%s_%d"%(imgname, i)
        db['data'].create_dataset(dname,data=res[i]['img'])
        db['data'][dname].attrs['charBB'] = res[i]['charBB']
        db['data'][dname].attrs['wordBB'] = res[i]['wordBB']
        db['data'][dname].attrs['txt'] = res[i]['txt']

def main(viz=False):
    config = CONFIG_LOCAL

    # open databases:
    imdir = config['im_dir']
    outdir = config['out_dir']
    depth_db = h5py.File(config['depth_db'],'r')
    seg_db = h5py.File(config['seg_db'],'r')

    out_db = h5py.File(outdir + '/dset_kr.h5', 'w')
    out_db.create_group('/data')

    imnames = sorted(depth_db.keys())
    N = len(imnames)

    # restrict the image indices:
    start_idx = min(START_IMG_IDX, N-1)
    global NUM_IMG
    if NUM_IMG < 0:
        NUM_IMG = N
    end_idx = min(START_IMG_IDX+NUM_IMG, N)
    print(NUM_IMG)
    print(start_idx, end_idx, N)

    RV3 = RendererV3(config['data_dir'], max_time=SECS_PER_IMG)

    for i in (range(start_idx, end_idx)):
        imname = imnames[i]
        try:
            # get the image:
            print(imdir+'/'+imname)
            img = Image.open(imdir+'/'+imname)
            if img is None:
                continue

            # get depth:
            depth = depth_db[imname][:].T
            depth = depth[:,:,0]

            # get segmentation:
            seg = seg_db['mask'][imname][:].astype('float32')
            area = seg_db['mask'][imname].attrs['area']
            label = seg_db['mask'][imname].attrs['label']

            # re-size uniformly:
            sz = depth.shape[:2][::-1]
            img = np.array(img.resize(sz,Image.ANTIALIAS))
            seg = np.array(Image.fromarray(seg).resize(sz,Image.NEAREST))

            print colorize(Color.RED,'%d of %d'%(i,end_idx-1), bold=True)
            res = RV3.render_text(img,depth,seg,area,label,
                                  ninstance=INSTANCE_PER_IMAGE,viz=viz)
            if len(res) > 0:
                # non-empty : successful in placing text:
                add_res_to_db(imname, res, out_db)

            # if viz:
                # if 'q' in raw_input(colorize(Color.RED,'continue?',True)):
                    # break
        except:
            traceback.print_exc()
            print(colorize(Color.GREEN,'>>>> CONTINUING....', bold=True))
            continue

    depth_db.close()
    seg_db.close()
    out_db.close()

if __name__=='__main__':
    main(True)
