import requests

BASE_URL='http://localhost:8080'

left,bottom,right,top=[-69.73895843749992, 37.59310012248169, -62.5319271874999, 41.52151087392275]
low_pressure,high_pressure=[1000,5000]

formdata = {
    'left': left,
    'bottom': bottom,
    'right': right,
    'top': top,
    'low_pressure': low_pressure,
    'high_pressure': high_pressure
}
r = requests.get(BASE_URL+'/query.csv',params=formdata,stream=True)
for line in r.iter_lines():
    print line
