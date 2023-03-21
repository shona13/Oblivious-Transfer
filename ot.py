import random
import secrets
import gmpy2 as gmp

'''
    Author : Sonal Joshi
    Description : 1-out-of-n protocol using RSA cryptosystem
'''

# Key generation function for RSA
def key_gen(p,q):
    N = p*q
    phi_n = (p-1)*(q-1)
    e = random.randint(2,phi_n)
    # Checking for gcd of (r,n) = 1 i.e Check if r belongs to Zn*
    while gmp.gcd(e, phi_n) != gmp.mpz(1):
        e = random.randint(2,phi_n)
    # -1 is for inverse
    d = gmp.powmod(e,-1,phi_n)
    return N,phi_n,e,d


# Alice input/output function
def io_alice():
    # List of indexes from 0,1,.. n-1
    pr_index = [int(i) for i in range(n)]
    # Private index - randomly chosen from the above list
    pri = random.randint(0,n-1)
    return pr_index,pri


# Bob input/output function
def io_bob():
    x = []
    for i in range(n):
        x.append(random.randint(0,N))
    return x


# Creates C_sigma for Bob for indexes 0,1,..n-1
def bob(e):
    ri = []
    state = gmp.random_state(hash(gmp.random_state()))
    # Randomy generates r for each index n
    [ri.append(gmp.mpz_random(state,N)) for _ in range(n)]
#    print("ri",ri)
    # C_sigma for each index
    C_row = [gmp.powmod(ri[i],e,N) for i in range(n)]
    return C_row


# Randomly chooses C_sigma from C0,C1,..Cn-1 & creates C using a randomly generated r
def alice(e,N,Cr):
    ranC = gmp.mpz(secrets.choice(Cr))
    r = secrets.randbelow(N)
    C = ranC + gmp.powmod(r,e,N)
    return r,C


# Bob 's side of calculation of zi & ci = zi + xi
def output(d,C,Cr,x):
    z = []
    c = []
    for i in range(n):
        z.append(gmp.powmod(C-Cr[i],d,N))
        xi = gmp.mod(x[i],N)
        c.append(z[i]+xi)
    return c


if __name__ == '__main__':
    ### Global n,N values make it easier for each function to use it without needing to pass it as parameters ###
    global n, N

    ### Primes p,q (given) ###
    p = gmp.mpz(19211916981990472618936322908621863986876987146317321175477459636156953561475008733870517275438245830106443145241548501528064000686696553079813968930084003413592173929258239545538559059522893001415540383237712787805857248668921475503029012210091798624401493551321836739170290569343885146402734119714622761918874473987849224658821203492683692059569546468953937059529709368583742816455260753650612502430591087268113652659115398868234585603351162620007030560547611)
    q = gmp.mpz(49400957163547757452528775346560420645353827504469813702447095057241998403355821905395551250978714023163401985077729384422721713135644084394023796644398582673187943364713315617271802772949577464712104737208148338528834981720321532125957782517699692081175107563795482281654333294693930543491780359799856300841301804870312412567636723373557700882499622073341225199446003974972311496703259471182056856143760293363135470539860065760306974196552067736902898897585691
)

    ### User input for n ###
    n = int(input("Please Enter n>=2: "))


    '''
        Calling the functions and creating objects for each function 
    '''
    N, phi, e, d = key_gen(p,q)
    pr_ind, ran_ind = io_alice()
    x = io_bob()
    Cr = bob(e)
    r,C = alice(e,N,Cr)
    c = output(d,C,Cr,x)
    x_sigma = gmp.mod(c[ran_ind]-r,N)


    '''
        Printing the values on terminal
    '''
    print("-" * 100)
    print("Print the values in X: ",x)
    print("Print \u03C3:",ran_ind)

    print("-" * 100)
    print("Print C0,C1,..,Cn-1: ", Cr)
    print("Print C: ", C)
    print("Print c0,c1,..,cn-1: ",c)

    print("-" * 100)
    print("x\u03C3:",x_sigma)
    print("-" * 100)

