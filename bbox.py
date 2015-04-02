from query import query_data

left,bottom,right,top=[-69.73895843749992, 37.59310012248169, -62.5319271874999, 41.52151087392275]
lo_press,hi_press=[2000,3000]

for row in query_data(left,bottom,right,top,lo_press,hi_press):
    print row
