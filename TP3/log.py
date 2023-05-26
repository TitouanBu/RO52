#!/usr/bin/env pybricks-micropython
import time

def write_log(distance,vitesse):
    # date_string = time.strftime("%d-%m-%Y")
    # time_string = time.strftime("%H:%M:%S")
    
    message = "{};{}\n".format(distance,vitesse)
    
    # Écrire la donnée dans le fichier txt
    with open('log.txt', 'a') as file:
        file.write(message)

def clear_log():
    with open("log.txt", "w") as f:
        f.write("")