import os

gp = os.popen('gnuplot -persist', 'w')
print >> gp, "set yrange [-300:300]"
for n in range(300):
	print >> gp, "plot %i*cos(x)+%i*log(x+10)" % (n,150-n)