import sympy as sp
s=sp.symbols('s')
def tf(A,B,C,D=0):
    n=A.shape[0]; return sp.simplify((C*(s*sp.eye(n)-A).inv()*B)[0]+D)
M=sp.Matrix
ok=lambda name,cond: print(('PASS ' if cond else 'FAIL ')+name)

# L02 slide 9 mass-spring-damper
m,b,k=sp.symbols('m b k',positive=True)
ok('L02 s9 MSD -> 1/(ms^2+bs+k)', sp.simplify(tf(M([[0,1],[-k/m,-b/m]]),M([0,1/m]),M([[1,0]]))-1/(m*s**2+b*s+k))==0)
# L02 slides 10-11 Ex3, reversed state order x1=ydd
A=M([[-6,-11,-6],[1,0,0],[0,1,0]]);B=M([6,0,0]);C=M([[0,0,1]])
ok('L02 s11 Ex3 -> 6/(s^3+6s^2+11s+6)', sp.simplify(tf(A,B,C)-6/(s**3+6*s**2+11*s+6))==0)
# L02 s16 generic beta, n=3
a1,a2,a3,b0,b1,b2,b3=sp.symbols('a1 a2 a3 b0 b1 b2 b3')
be0=b0;be1=b1-a1*be0;be2=b2-a1*be1-a2*be0;be3=b3-a1*be2-a2*be1-a3*be0
Ac=M([[0,1,0],[0,0,1],[-a3,-a2,-a1]])
G=(b0*s**3+b1*s**2+b2*s+b3)/(s**3+a1*s**2+a2*s+a3)
ok('L02 s16-17 beta form (n=3 symbolic) -> G', sp.simplify(tf(Ac,M([be1,be2,be3]),M([[1,0,0]]),be0)-G)==0)
# L02 Ex4
v=dict(a1=2,a2=3,a3=4,b0=5,b1=6,b2=7,b3=8); sub={sp.Symbol(x):y for x,y in v.items()}
print('   Ex4 betas:',[sp.simplify(e.subs(sub)) for e in (be0,be1,be2,be3)],'(slide 18: 5,-4,0,0)')
ok('L02 s19 Ex4 SS -> (5s^3+6s^2+7s+8)/(s^3+2s^2+3s+4)', sp.simplify(tf(M([[0,1,0],[0,0,1],[-4,-3,-2]]),M([-4,0,0]),M([[1,0,0]]),5)-G.subs(sub))==0)
# L03 s4 CCF generic n=3
Cc=M([[b3-a3*b0,b2-a2*b0,b1-a1*b0]])
ok('L03 s4 CCF (n=3 symbolic) -> G', sp.simplify(tf(Ac,M([0,0,1]),Cc,b0)-G)==0)
# L03 s6 OCF generic n=3
Ao=M([[0,0,-a3],[1,0,-a2],[0,1,-a1]]);Bo=M([b3-a3*b0,b2-a2*b0,b1-a1*b0])
ok('L03 s6 OCF (n=3 symbolic) -> G', sp.simplify(tf(Ao,Bo,M([[0,0,1]]),b0)-G)==0)
ok('[added] OCF = CCF transposed: Ao=Ac^T, Bo=Cc^T, Co=Bc^T', Ao==Ac.T and Bo==Cc.T and M([[0,0,1]])==M([0,0,1]).T)
# L03 s9 Jordan block, triple root
p,c1,c2,c3=sp.symbols('p c1 c2 c3')
J=M([[-p,1,0],[0,-p,1],[0,0,-p]])
ok('L03 s9 JCF block B=[0,0,1] -> c1/(s+p)^3+c2/(s+p)^2+c3/(s+p)', sp.simplify(tf(J,M([0,0,1]),M([[c1,c2,c3]]))-(c1/(s+p)**3+c2/(s+p)**2+c3/(s+p)))==0)
# L03 Ex1
G1=(s+3)/(s**2+3*s+2)
ok('L03 s11 Ex1 CCF', sp.simplify(tf(M([[0,1],[-2,-3]]),M([0,1]),M([[3,1]]))-G1)==0)
ok('L03 s12 Ex1 OCF', sp.simplify(tf(M([[0,-2],[1,-3]]),M([3,1]),M([[0,1]]))-G1)==0)
print('   partial fractions:',sp.apart(G1,s),'(slide 12: 2/(s+1) - 1/(s+2))')
ok('L03 s12 Ex1 DCF', sp.simplify(tf(M([[-1,0],[0,-2]]),M([1,1]),M([[2,-1]]))-G1)==0)
ok('[added] Ex1 eigenvalues same in all three forms', all(set(X.eigenvals())=={-1,-2} for X in (M([[0,1],[-2,-3]]),M([[0,-2],[1,-3]]),M([[-1,0],[0,-2]]))))
# L03 Ex2
A2=M([[-1,1,0],[0,-1,1],[0,0,-2]])
R=(s*sp.eye(3)-A2).inv(); print('   (sI-A)^-1 row1:',[sp.factor(x) for x in R.row(0)])
ok('L03 s18 Ex2 -> 1/((s+1)^2(s+2)) = 1/(s^3+4s^2+5s+2)', sp.simplify(tf(A2,M([0,0,1]),M([[1,0,0]]))-1/(s**3+4*s**2+5*s+2))==0 and sp.expand((s+1)**2*(s+2))==s**3+4*s**2+5*s+2)
# L01 s6 example
ok('L01 s6 1/(s^3+2s^2+5s+8)', sp.simplify(tf(M([[-2,-5,-8],[1,0,0],[0,1,0]]),M([1,0,0]),M([[0,0,1]]))-1/(s**3+2*s**2+5*s+8))==0)
# [added] similarity invariance
T=M([[1,2],[0,1]]);Ae=M([[0,1],[-2,-3]]);Be=M([0,1]);Ce=M([[3,1]])
Ti=T.inv()
ok('[added] x=Tz keeps G(s) and eigenvalues', sp.simplify(tf(Ti*Ae*T,Ti*Be,Ce*T)-G1)==0 and (Ti*Ae*T).eigenvals()==Ae.eigenvals())
