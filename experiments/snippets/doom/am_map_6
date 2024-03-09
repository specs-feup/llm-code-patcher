void AM_findMinMaxBoundaries(void)
{
    int i;
    fixed_t a;
    fixed_t b;

    min_x = min_y =  MAXINT;
    max_x = max_y = -MAXINT;
  
    for (i=0;i<numvertexes;i++)
    {
	    if (vertexes[i].x < min_x)
	        min_x = vertexes[i].x;
	    else if (vertexes[i].x > max_x)
	        max_x = vertexes[i].x;

    	if (vertexes[i].y < min_y)
	        min_y = vertexes[i].y;
	    else if (vertexes[i].y > max_y)
	        max_y = vertexes[i].y;
    }
  
    max_w = max_x - min_x;
    max_h = max_y - min_y;

    min_w = 2*PLAYERRADIUS; // const? never changed?
    min_h = 2*PLAYERRADIUS;

    a = FixedDiv(f_w<<FRACBITS, max_w);
    b = FixedDiv(f_h<<FRACBITS, max_h);
  
    min_scale_mtof = a < b ? a : b;
    max_scale_mtof = FixedDiv(f_h<<FRACBITS, 2*PLAYERRADIUS);
}