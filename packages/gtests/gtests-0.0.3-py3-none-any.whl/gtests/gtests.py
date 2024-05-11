import numpy as np
from . import graphutilities as gu
from scipy.stats import norm
from scipy.stats import chi2

# calculate R values
# R0 is the number of between-sample edges (between samples n and m)
# Rn is the number of edges connecting observations both from sample n
# G is the graph (MST)
# nID is a numpy array of nodes belonging to sample n
# mID is only used when calculating R0, its default is None
def Rk(G, nID, mID = None):
    G = np.triu(G)
    # a tuple of vectors
    # each vector represents a new dimension
    # together, all dimensions denote an edge
    # e.g. (edges[0][0], edges[1][0]) = (1, 5) denotes an edge connecting node 1 to node 5
    edges = np.nonzero(G)
    sum = 0
    
    # calculate R0
    if mID is not None:
        for i in range(0, edges[0].size):
            sum = sum+(((edges[0][i] in nID) and (edges[1][i] in mID)) or ((edges[1][i] in nID) and (edges[0][i] in mID)))
        return sum
    
    # otherwise calculate Rk for k ≥ 1
    for i in range(0, edges[0].size):
        sum = sum+((edges[0][i] in nID) and (edges[1][i] in nID))
    return sum

# expectation of Rk values
# G is the graph (MST)
# n is the sample size of group k
def Uk(G, n, m = None):
    N = G.shape[0]
    
    # if m is provided, calculate U0
    if m is not None:
        return gu.edge_count(G)*2*n*m/(N*(N-1))
    
    # if m is not provided, calculate U1, U2, etc
    return gu.edge_count(G)*(n*(n-1))/(N*(N-1))

# sigma function
# G is the graph (MST)
# n is the size of sample n
# m is the size of sample m
def sigma(G, n, m, sig0 = False):
    sigma_mat = np.zeros((2, 2))
    N = G.shape[0]
    C = gu.C(G)
    E = gu.edge_count(G)
    U0 = Uk(G, n, m)
    U1 = Uk(G, n)
    U2 = Uk(G, m)
    
    if sig0 == True:
        sigma0 = U0*(1-U0)+2*C*(n*m)/(N*(N-1))+(E*(E-1)-2*C)*(4*n*m*(n-1)*(m-1))/(N*(N-1)*(N-2)*(N-3))
        return sigma0
    
    sigma_mat[0, 0] = U1*(1-U1)+2*C*(n*(n-1)*(n-2))/(N*(N-1)*(N-2))+(E*(E-1)-2*C)*(n*(n-1)*(n-2)*(n-3))/(N*(N-1)*(N-2)*(N-3))
    sigma_mat[1, 1] = U2*(1-U2)+2*C*(m*(m-1)*(m-2))/(N*(N-1)*(N-2))+(E*(E-1)-2*C)*(m*(m-1)*(m-2)*(m-3))/(N*(N-1)*(N-2)*(N-3))
    sigma_mat[0, 1] = (E*(E-1)-2*C)*(n*m*(n-1)*(m-1))/(N*(N-1)*(N-2)*(N-3))-U1*U2
    sigma_mat[1, 0] = sigma_mat[0, 1]
    
    return sigma_mat

# GENERALIZED
# calculate the S statistic
# G is the graph (MST)
# n is the size of sample n
# m is the size of sample m
def S(G, nID, mID):
    n = len(nID)
    m = len(mID)
    R1 = Rk(G, nID)
    R2 = Rk(G, mID)
    U1 = Uk(G, n)
    U2 = Uk(G, m)
    Sigma = sigma(G, n, m)
    
    # the @ operator peforms matrix multiplication, don't confuse with function decorator
    S = np.hstack((R1-U1, R2-U2))@np.linalg.inv(Sigma)@np.vstack((R1-U1, R2-U2))
    return S[0]

# G is the graph (MST)
# n is the size of sample k
# m is the size of sample l
# nreps is the number of repetitions to use for permutation calculations
def Perm(G, n, m, nID, mID, nreps = 1e4):
    nreps = int(nreps)
    N = G.shape[0]
    ID = np.arange(G.shape[0])
    
    r1 = np.zeros(nreps)
    r2 = np.zeros(nreps)
    for i in np.arange(nreps):
        np.random.shuffle(ID)
        nIDp = ID[:n]
        mIDp = ID[n:(n+m)]
        
        R1p = Rk(G, nIDp)
        R2p = Rk(G, mIDp)
        
        r1[i] = R1p
        r2[i] = R2p
    
    R1 = Rk(G, nID)
    R2 = Rk(G, mID)
    U1 = np.mean(r1)
    U2 = np.mean(r2)
    Sigma = np.cov(r1, r2)
    
    S = np.hstack((R1-U1, R2-U2))@np.linalg.inv(Sigma)@np.vstack((R1-U1, R2-U2))
    
    return S

# WEIGHTED
# G is the graph (MST)
# nID is a numpy array of the nodes belonging to sample n
# mID is a numpy array of the nodes belonging to sample m
def Z(G, nID, mID):
    n = nID.size
    m = mID.size
    N = n+m
    p = n/N
    q = 1-p
    
    R1 = Rk(G, nID)
    R2 = Rk(G, mID)
    U1 = Uk(G, n)
    U2 = Uk(G, m)
    V = sigma(G, n, m)
    
    Zw = (q*(R1-U1)+p*(R2-U2))/(np.sqrt((q**2)*V[0, 0]+(p**2)*V[1, 1]+2*q*p*V[0, 1]))
    Zd = (R1-R2-(U1-U2))/(np.sqrt(V[0, 0]+V[1, 1]-2*V[0, 1]))
    return {"Zw" : Zw, "Zd" : Zd}

# ORIGINAL
# G is the graph (MST)
# nID is a numpy array of the nodes belonging to sample n
# mID is a numpy array of the nodes belonging to sample m
def W(G, nID, mID):
    n = len(nID)
    m = len(mID)
    R1 = Rk(G, nID)
    R2 = Rk(G, mID)
    U0 = Uk(G, n, m)
    Sigma = sigma(G, n, m, sig0 = True)
    return (gu.edge_count(G)-R1-R2-U0)/(np.sqrt(Sigma))

# MAIN FUNCTION
def gtests(G, nID, mID, type = "all", kappa = 1.14, perm = 0):
    perm = int(perm)
    n = len(nID)
    m = len(mID)
    type = type.lower()
    gresults = {}
    
    if type == "all" or type == "original" or type == "o":
        W0 = W(G, nID, mID)
        gresults["original.stat"] = W0
        gresults["original.pval"] = norm.cdf(W0)
    if type == "all" or type == "generalized" or type == "g":
        S0 = S(G, nID, mID)
        gresults["generalized.stat"] = S0
        gresults["generalized.pval"] = chi2.sf(S0, df = 2)
    if type == "all" or type == "weighted" or type == "w":
        Z0 = Z(G, nID, mID)["Zw"]
        gresults["weighted.stat"] = Z0
        gresults["weighted.pval"] = norm.cdf(-Z0)
    if type == "all" or type == "maxkappa" or type == "m":
        M = Z(G, nID, mID)
        M0 = np.maximum(kappa*M["Zw"], np.absolute(M["Zd"]))
        gresults["maxkappa.stat"] = M0
        gresults["maxkappa.pval"] = 1-norm.cdf(M0/kappa)*(2*norm.cdf(M0)-1)
    
    if perm > 0:
        W0p = np.zeros(perm)
        S0p = np.zeros(perm)
        Z0p = np.zeros(perm)
        M0p = np.zeros(perm)
        
        ID = np.arange(G.shape[0])
        for i in np.arange(perm):
            np.random.shuffle(ID)
            nIDp = ID[:n]
            mIDp = ID[n:(n+m)]
            
            if type == "all" or type == "original" or type == "o":
                W0p[i] = W(G, nIDp, mIDp)
            if type == "all" or type == "generalized" or type == "g":
                S0p[i] = S(G, nIDp, mIDp)
            if type == "all" or type == "weighted" or type == "w":
                Z0p[i] = Z(G, nIDp, mIDp)["Zw"]
            if type == "all" or type == "maxkappa" or type == "m":
                Mp = Z(G, nIDp, mIDp)
                M0p[i] = np.maximum(kappa*Mp["Zw"], np.absolute(Mp["Zd"]))
                
        if type == "all" or type == "original" or type == "o":
            gresults["original.perm"] = np.mean(W0p <= W0)
        if type == "all" or type == "generalized" or type == "g":
            gresults["generalized.perm"] = np.mean(S0p >= S0)
        if type == "all" or type == "weighted" or type == "w":
            gresults["weighted.perm"] = np.mean(Z0p >= Z0)
        if type == "all" or type == "maxkappa" or type == "m":
            gresults["maxkappa.perm"] = np.mean(M0p >= M0)
    
    return gresults