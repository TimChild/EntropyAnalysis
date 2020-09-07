from JupyterImport import *
import re
from src.DatObject.Attributes import SquareEntropy as SE

def merge_dat_parts(dats, centers=None):  # TODO: This could be a lot more general and not only work for SE
    """
    Merges two part Square entropy dats.
    Args:
        dats (List[DatHDF]): 
        centers (Optional[np.ndarray]):  

    Returns:
        Tuple[np.ndarray, np.ndarray]: full_x, full_cycled_data
    """
    assert len(dats) == 2
    
    for dat in dats:    
        comments = dat.Logs.comments.split(',')
        comments = [com.strip() for com in comments]
        part_comment = [com for com in comments if re.match('part*', com)][0]
        part_num = int(re.search('(?<=part)\d+', part_comment).group(0))
        dat.Other.part_num = part_num
        if part_num == 1:
            p1_dat = dat
        elif part_num == 2:
            p2_dat = dat

    full_x = p1_dat.SquareEntropy.Processed.outputs.x
    p1_data = p1_dat.SquareEntropy.Processed.outputs.cycled

    p2_x = p2_dat.SquareEntropy.Processed.outputs.x
    p2_data = p2_dat.SquareEntropy.Processed.outputs.cycled
    idxs = CU.get_data_index(full_x, [p2_x[0], p2_x[-1]])

    p2_data = np.pad(p2_data, ((0, 0), (0, 0), (idxs[0], full_x.shape[0]-idxs[1]-1)), mode='constant', constant_values=np.nan)

    full_data = np.concatenate((p1_data, p2_data), axis=0)
    full_x, full_avg_data = SE.average_2D(full_x, full_data, avg_nans=True, centers=centers)
    return full_x, full_avg_data