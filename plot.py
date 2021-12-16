from src.attack import *
from src.create import *
from src.measure import *

## focus on 2 to 3
#ER250= np.loadtxt('./notebooks/results/sy/er/scale/ERn250s.csv',delimiter=",")
#ER500= np.loadtxt('./notebooks/results/sy/er/scale/ERn500s.csv',delimiter=",")

#plot_pinf([ER250, ER500], k=4, labels= ["ER model, N=250, <k>=4","ER model, N=500"], path="./notebooks/figure/ER_250_500.png", p_theory=True)


## normal plot 
ER250= np.loadtxt('./notebooks/results/sy/er/t20/ERn250k4.csv',delimiter=",")
ER500= np.loadtxt('./notebooks/results/sy/er/t20/ERn500k4.csv',delimiter=",")
ER1000= np.loadtxt('./notebooks/results/sy/er/t20/ERn1000k4.csv',delimiter=",")
ER2000= np.loadtxt('./notebooks/results/sy/er/t20/ERn2000k4.csv',delimiter=",")

plot_pinf([ER250, ER500, ER1000, ER2000], k=4,labels= ["ER model, N=250, <k>=4","ER model, N=500", "ER model, N=1000", "ER model, N=2000"], path="./notebooks/figure/ER_t20.png", p_theory=True)

