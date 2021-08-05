// cylinder
Nx1 = 4; Rx1 = 0.86;
Nx2 = 8; Rx2 = 1.0;
Nx3 = 15; Rx3 = 1.13;
Nc  = 6; Rc  = 0.8;
Nj  = 2;  Rj  = 1.00;
Nx4  = 4;  Rx4  = 1.00;
Noutx = 3; Routx = 4;
Nouty = Ny; Routy = 1.0;


Point(1) = {-2, 1, 0, 1.0};
Point(2) = {-1, 1, 0, 1.0};
Point(3) = {1,  1, 0, 1.0};
Point(4) = {10, 1, 0, 1.0};
Point(5) = {-2, -1, 0, 1.0};
Point(6) = {-1, -1, 0, 1.0};
Point(7) = {1,  -1, 0, 1.0};
Point(8) = {10, -1, 0, 1.0};

Point(9) = {-0.353553/5.0*2.5, 0.353553/5.0*2.5, 0, 1.0};
Point(10) = {0.353553/5.0*2.5, 0.353553/5.0*2.5, 0, 1.0};
Point(11) = {0.353553/5.0*2.5,-0.353553/5.0*2.5, 0, 1.0};
Point(12) = {-0.353553/5.0*2.5,-0.353553/5.0*2.5, 0, 1.0};
Point(13) = {0, 0, 0, 1.0};


Point(21) = {-0.1, 1., 0, 1.0};
Point(22) = {0.1, 1., 0, 1.0};

Point(23) = {-0.04357787137382908/5.0*2.5, 0.4980973490458728/5.0*2.5, 0, 1.0};
Point(24) = {0.04357787137382908/5.0*2.5, 0.4980973490458728/5.0*2.5, 0, 1.0};
Point(25) = {-0.04357787137382908/5.0*2.5, -0.4980973490458728/5.0*2.5, 0, 1.0};
Point(26) = {0.04357787137382908/5.0*2.5, -0.4980973490458728/5.0*2.5, 0, 1.0};

Point(27) = {-0.1, -1, 0, 1.0};
Point(28) = {0.1, -1, 0, 1.0};


Line(1) = {1, 2}; Transfinite Line {1} = Nx1 Using Progression Rx1;
//Line(2) = {2, 3}; Transfinite Line {2} = Nx2 Using Progression Rx2;
Line(3) = {3, 4}; Transfinite Line {3} = Nx3 Using Progression Rx3;

Line(4) = {5, 6}; Transfinite Line {4} = Nx1 Using Progression Rx1;
//Line(5) = {6, 7}; Transfinite Line {5} = Nx2 Using Progression Rx2;
Line(6) = {7, 8}; Transfinite Line {6} = Nx3 Using Progression Rx3;

Line(7) = {5, 1}; Transfinite Line {7} = Nx2 Using Progression Rx2;
Line(8) = {6, 2}; Transfinite Line {8} = Nx2 Using Progression Rx2;
Line(9) = {7, 3}; Transfinite Line {9} = Nx2 Using Progression Rx2;
Line(10) = {8, 4}; Transfinite Line {10} = Nx2 Using Progression Rx2;

Line(11) = {2, 9}; Transfinite Line {11} = Nc Using Progression Rc;
Line(12) = {3, 10}; Transfinite Line {12} = Nc Using Progression Rc;
Line(13) = {7, 11}; Transfinite Line {13} = Nc Using Progression Rc;
Line(14) = {6, 12}; Transfinite Line {14} = Nc Using Progression Rc;

Line(31) = {2, 21}; Transfinite Line {31} = Nx4 Using Progression Rx4;
Line(32) = {21, 22}; Transfinite Line {32} = Nj Using Progression Rj;
Line(33) = {22, 3}; Transfinite Line {33} = Nx4 Using Progression Rx4;

Circle(34) = {9,13, 23}; Transfinite Line {34} = Nx4 Using Progression Rx4;
Circle(35) = {23,13,24}; Transfinite Line {35} = Nj Using Progression Rj;
Circle(36) = {24,13,10}; Transfinite Line {36} = Nx4 Using Progression Rx4;

Circle(37) = {25,13,12}; Transfinite Line {37} = Nx4 Using Progression Rx4;
Circle(38) = {26,13,25}; Transfinite Line {38} = Nj Using Progression Rj;
Circle(39) = {11,13,26}; Transfinite Line {39} = Nx4 Using Progression Rx4;

//Circle(15) = {9, 13, 10}; Transfinite Line {15} = Nx2 Using Progression Rx2;
Circle(16) = {10, 13, 11}; Transfinite Line {16} = Nx2 Using Progression Rx2;
//Circle(17) = {11, 13, 12}; Transfinite Line {17} = Nx2 Using Progression Rx2;
Circle(18) = {12, 13, 9}; Transfinite Line {18} = Nx2 Using Progression Rx2;

Line(40) = {6, 27}; Transfinite Line {40} = Nx4 Using Progression Rx4;
Line(41) = {27, 28}; Transfinite Line {41} = Nj Using Progression Rj;
Line(42) = {28, 7}; Transfinite Line {42} = Nx4 Using Progression Rx4;

Line(43) = {21, 23}; Transfinite Line {43} = Nc Using Progression Rc;
Line(44) = {22, 24}; Transfinite Line {44} = Nc Using Progression Rc;
Line(45) = {27, 25}; Transfinite Line {45} = Nc Using Progression Rc;
Line(46) = {28, 26}; Transfinite Line {46} = Nc Using Progression Rc;


// surfaces
Line Loop(20) = {7, 1, -8, -4}; Plane Surface(1) = {20};
//Line Loop(21) = {-11, 2, 12, -15}; Plane Surface(2) = {21};
Line Loop(22) = {-12, -9, 13, -16}; Plane Surface(3) = {22};
//Line Loop(23) = {-13, -5, 14, -17}; Plane Surface(4) = {23};
Line Loop(24) = {-14,  8, 11, -18}; Plane Surface(5) = {24};
Line Loop(25) = {3, -10, -6, 9}; Plane Surface(6) = {25};

Line Loop(51) = {-11, 31, 43, -34}; Plane Surface(11) = {51};
Line Loop(52) = {-43, 32, 44, -35}; Plane Surface(12) = {52};
Line Loop(53) = {-44, 33, 12, -36}; Plane Surface(13) = {53};
Line Loop(54) = {-13, -42, 46, -39}; Plane Surface(14) = {54};
Line Loop(55) = {-46, -41, 45, -38}; Plane Surface(15) = {55};
Line Loop(56) = {-45, -40, 14, -37}; Plane Surface(16) = {56};


Transfinite Surface {1}; Recombine Surface {1};
//Transfinite Surface {2}; Recombine Surface {2};
Transfinite Surface {3}; Recombine Surface {3};
//Transfinite Surface {4}; Recombine Surface {4};
Transfinite Surface {5}; Recombine Surface {5};
Transfinite Surface {6}; Recombine Surface {6};

Transfinite Surface {11}; Recombine Surface {11};
Transfinite Surface {12}; Recombine Surface {12};
Transfinite Surface {13}; Recombine Surface {13};
Transfinite Surface {14}; Recombine Surface {14};
Transfinite Surface {15}; Recombine Surface {15};
Transfinite Surface {16}; Recombine Surface {16};


// physical groups
Physical Line("inlet")  = {7};
Physical Line("outlet") = {10};
Physical Line("swalls") = {1,31,32,33,3,4,40,41,42,6,34,36,16,37,39,18};  // straight walls and circular walls
Physical Line("jets") = {35,38};  // straight walls and circular walls
Physical Surface("fluid") = {1,3,5,6,11,12,13,14,15,16};


