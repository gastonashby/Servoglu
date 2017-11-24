 function H=dose(t)
 H=0;
	 for n=0:50
		if(t >= 6*n)&(t < 6*n+.5)
			H=1;
	 end
 end
  
function e=e()
	e=0;
	if (N > 8.65)
		e= 0.03245 * mgut;
	else
		e = (0.000433 * (N**2) + 0.0075 * N) * mgut;
end
		
function H=H()
	H=0;
	if (BG <= BGthresh)
		H= Ah * BG + Bh * a( ) + Ch;
	else
		H= Ah * BGthresh + Bh * a( ) + Ch;
end

function Pglut1plus3=Pglut1plus3() 
	Pglut1plus3 = J1plus3 * BG / ( BG + Km1plus3);
end		

function Pglut4=Pglut4()
	Pglut4= J4 * BG / ( BG + KM4) * a( );
end

function R=R() 
	R= max( 0, ( FG * BG - Tmax) / W) 
end
	
function E=E()
	E=H( ) - R( ) - Pglut4( ) - Pglut1plus3( );
end

function a=a()
	a= i( ) * s 
end
function i=i()
	i=( iaster( ) - iaster0) / ( 1 - iaster0);
end
function iaster=iaster()
	iaster=( p( ) - p0) / root( d, pow( p( ) - p0, d) + pow( k, d)) ;
end
function p=p()
	p= gamma / C * Q ;
end
function U=U()
	U=0;
	if (DiabetesTypeOne = 0) #####NAASSEEEE
		U=42;
	else
		U= 1;
end