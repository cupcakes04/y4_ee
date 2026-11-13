student_id = 19;            % Replace with assigned ID, 1 to 20 
g = 9.81; 
m0 = round(100*(1.31 + 0.02*(student_id-1)))/100; 
arm_values = [0.23 0.24 0.25 0.26 0.27]; 
l = arm_values(mod(3*(student_id-1),5)+1); 
m_nom = 1.50*m0; 
m = m_nom; 
Jdiag = [0.03;0.03;0.05]*(m0/1.5)*(l/0.25)^2; 
J = diag(Jdiag); 
Omega_max = 800; 
kT = 2*m_nom*g/(4*Omega_max^2); 
kMT = 0.020; 
kM = kMT*kT; 
sigma = [1;-1;1;-1]; 
if student_id <= 10       % Plus configuration 
    rotor_xy = [l 0 -l 0; 0 l 0 -l]; 
else                      % X configuration 
    d = l/sqrt(2); 
    rotor_xy = [d d -d -d; -d d d -d]; 
end 
c_drag = 0; 
X0 = zeros(12,1); 
Omega_hover = sqrt(m_nom*g/(4*kT)); 
Omega_cmd = Omega_hover*ones(4,1); 