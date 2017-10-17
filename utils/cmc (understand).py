import numpy as np


def _cmc_core(D, G, P):
    m, n = D.shape
    order = np.argsort(D, axis=0)#将D按列从小到大排序
    match = (G[order] == P) 
    return (match.sum(axis=1) * 1.0 / n).cumsum()#


def cmc(distmat, glabels=None, plabels=None, ds=None, repeat=None):
    """Compute the Cumulative Match Characteristic (CMC)
    This function assumes that gallery labels have no duplication. If there are
    duplications, random downsampling will be performed on gallery labels, and
    the computation will be repeated to get an average result.
    Parameters
    ----------
    distmat : numpy.ndarray
        The distance matrix. ``distmat[i, j]`` is the distance between i-th
        gallery sample and j-th probe sample.
    glabels : numpy.ndarray or None, optional
    plabels : numpy.ndarray or None, optional
        If None, then gallery and probe labels are assumed to have no
        duplications. Otherwise, they represent the vector of gallery and probe
        labels. Default is None.
    ds : int or None, optional
        If None, then no downsampling on gallery labels will be performed.
        Otherwise, it represents the number of gallery labels to be randomly
        selected. Default is None.
    repeat : int or None, optional
        If None, then the function will repeat the computation for 100 times
        when downsampling is performed. Otherwise, it specifies the number of
        repetition. Default is None.
    Returns
    -------
    out : numpy.ndarray
        The rank-1 to rank-m accuracy, where m is the number of (downsampled)
        gallery labels.
    """
    m, n = distmat.shape#m=glabel数量,n=plabel数量
    if glabels is None and plabels is None:
        glabels = np.arange(0, m) #0到m-1
        plabels = np.arange(0, n) #0到n-1
    if isinstance(glabels, list):
        glabels = np.asarray(glabels)
    if isinstance(plabels, list):
        plabels = np.asarray(plabels)
    ug = np.unique(glabels) #ug是glabel去除重复id之后的数组
    if ds is None:
        ds = ug.size #downsampling在glabels
    if repeat is None: #如果label里面没有id重复，且没有下采样，则只运行一次；否则100次。
        if ds == ug.size and ug.size == len(glabels):
            repeat = 1
        else:
            repeat = 100

    ret = 0
    for __ in xrange(repeat):
        # Randomly select gallery labels e.g.downsampling
        G = np.random.choice(ug, ds, replace=False)# 正式的galleryid数组，若不下采样 G = ug
        # Select corresponding probe samples
        p_inds = [i for i in xrange(len(plabels)) if plabels[i] in G]#plable中在G中出现过的元素索引
        P = plabels[p_inds]#正式的Probe id ：plable中在G中出现过的元素
        # Randomly select one gallery sample per label selected
        D = np.zeros((ds, P.size))
        for i, g in enumerate(G):#i是索引，g是元素
            samples = np.where(glabels == g)[0] #返回在G中出现的glabels的id的索引，可能有多个位置
            j = np.random.choice(samples) #多个位置中取一个
            D[i, :] = distmat[j, p_inds] #生成新距离矩阵D，纵轴是g,横轴是p; D[i,j]=距离（G[i],P[j]）
        # Compute CMC
        ret += _cmc_core(D, G, P)
    return ret / repeat
