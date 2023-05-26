import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

current = os.getcwd()


with open(sys.argv[1], 'r') as csvfile:
    data = pd.read_csv(csvfile, usecols=[' x',' y']).to_numpy()
    x = [value[0] for value in data]
    y = [value[1] for value in data]
        
plt.plot(x, y, color="orange", label="Position")
plt.title("Position du robot")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend(loc="upper left")
plt.grid()
plt.savefig(os.path.join(current, sys.argv[2]+".jpeg"), dpi=300)
plt.clf()   


