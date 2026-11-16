%% Practical 3 setup (run before EVERY test, then apply overrides)
practical2_parameters
m = m_nom;
c_drag = 0;
A = [ones(1,4); -rotor_xy(2,:); rotor_xy(1,:); (kM/kT)*sigma(:).'];
wnAtt = 6; wnXY = 0.70; wnD = 1.00; zeta = 1.00;
tiltMax = 20*pi/180;
p0 = zeros(3,1); p1 = p0;
e0 = zeros(3,1); e1 = e0;
mode = 1;           % 1 = attitude only, 2 = position and attitude
