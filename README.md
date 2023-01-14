# Weather Data Collection
# Web Srcapping using Python to collect wather data from https://weather.gc.ca/city/pages/on-143_metric_e.html
Basic idea: benchmark for the forecast performance.

Indicators:
	Stability: 
	Credibility: 

Measurement:
	temperature: native data: diff(temp1,temp2)=abs(temp1-temp2)
	condition: assign value to condition
Sunny/Clear=0, 
Mainly Sunny/A mix of sun and cloud=1, 
Mainly cloudy=2, 
Cloudy=3, 
chance of showers=4, 
showers=5, 
heavy showers = 6
		diff(con1,con2) = abs(con1-con2)
	wind direction:  assign value to wind direction:
N=0, NE=1, E=2, SE=3, S=4, SW=5, W=6, NW=7. 
diff(wd1,wd2) = min(abs(wd1-wd2), 8-abs(wd1-wd2))
wind speed: native
	diff(ws1,ws2) = abs(ws1-ws2)
Algorithm:
	For day: x0,x1,x2,x3,x4,x(=x5)
		stability:  i=15diff(xi-xi-1)2/5
		credibility: i=04diff(xi-x)2 /5

	For hour: x0,x1..x23
		stability: i=123diff(xi-xi-1)2/23

		credibility: i=022diff(xi-x23)2/23

For day:
		
1. See the stability and credibility of weather forecast in different seasons, expecting the larger value when seasons are changing.
2. See if the weather forecast technology is improved or not over years.
3. See if the forecast technology should be dynamic as time passing by as the climate and environment of the earth might be always in change.


For hours:
1. See the stability and credibility of weather forecast in different hours in a day. Expect large values in the morning and down and when season changes. 
2. See if the weather forecast technology is improved or not over years.
3. See if the forecast technology should be dynamic as time passing by as the climate and environment of the earth might be always in change.
