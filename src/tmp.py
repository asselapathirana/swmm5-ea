from subprocess import Popen,PIPE

gnuplot = r'..\\gnuplot\\pgnuplot.exe'

data = [(x,x*x) for x in range(10)]

plot=Popen([gnuplot,'-persist'],stdin=PIPE,stdout=PIPE )

plot.communicate(b"plot '-' with lines\n")
plot.communicate("\n".join("%f %f"%d for d in data).encode())
plot.communicate(b"\ne\n")
plot.stdin.flush()