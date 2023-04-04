import h5py
from scipy import sparse as sp
import numpy as np

def load_matlab_file(path_file, name_field):

    db = h5py.File(path_file, 'r')
    ds = db[name_field]
    try:
        if 'ir' in ds.keys():
            data = np.asarray(ds['data'])
            ir   = np.asarray(ds['ir']) # ir: 行下标
            print(jc) 
            jc   = np.asarray(ds['jc']) # jc: 列下标
            out  = sp.csc_matrix((data, ir, jc)).astype(np.float32) # 加载稀疏矩阵存储格式
    except AttributeError:
        # Transpose in case is a dense matrix because of the row- vs column- major ordering between python and matlab
        out = np.asarray(ds).astype(np.float32).T # 如果不是稀疏矩阵就直接加载
    db.close()
    return out