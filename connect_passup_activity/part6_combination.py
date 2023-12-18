# this part is to connect the boardings and the pass-ups for each stop
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

TOTAL_PASS_UPS = 3958
severiy_df = pd.read_csv("severity_ranking.csv")

os.makedirs("combinations for top15 of severity rankings",exist_ok=True)
os.makedirs("figures for top15 of severity rankings",exist_ok=True)

for index in range(15):
    combination_df = pd.DataFrame({}, columns=['pass_up_support', 'boardings', 'stop_id'])  #this is the new df
    route_direct_id = severiy_df["route_direction"][index]
    
    boarding_df = pd.read_csv("boardings for each stop of different directions/"+route_direct_id+".csv")
    pass_up_df = pd.read_csv("pass-ups for each stop of different directions/"+route_direct_id+".csv")
    
    for new_index in range(len(boarding_df)):
        combination_df.loc[new_index] = {"pass_up_support": pass_up_df["pass_up_support"][new_index], "boardings":boarding_df["average_boardings"][new_index], "stop_id":boarding_df["stop_id"][new_index]}
    #plt.figure()
    #plt.plot(combination_df.index, TOTAL_PASS_UPS*combination_df["pass_up_support"], 'r', combination_df.index, combination_df["boardings"], 'b')
    #plt.savefig("figures for top15 of severity rankings/"+route_direct_id+".png")
    #plt.close()
    t = combination_df.index
    data1 = TOTAL_PASS_UPS*combination_df["pass_up_support"]
    data2 = combination_df["boardings"]
    
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Indices of the stops in the order of the bus direction')
    ax1.set_ylabel('pass up\nsupport', color='red', rotation=0, labelpad=10)
    ax1.plot(t, data1, color='red', label='pass up support')
    ax1.tick_params(axis='y', colors='red', labelsize=10, pad=2)
    ax1.spines['left'].set_color('red')
    plt.legend(loc=(0.65, 0.88), labelcolor='red', fontsize=10)
    
    ax2 = ax1.twinx()
    
    ax2.set_ylabel('average\n   boardings', color='blue', rotation=0, labelpad=10)  # we already handled the x-label with ax1
    ax2.plot(t, data2, color='blue', label='avearge boardings')
    ax2.tick_params(axis='y', colors='blue', labelsize=10, pad=2)
    ax2.spines['right'].set_color('blue')
    font = {'family':'serif','color':'darkred','size':14}
    plt.title(route_direct_id, x=0.5, y=0.94, fontweight="bold")
    plt.legend(loc=(0.65, 0.82), labelcolor='blue', fontsize=10)
    fig.tight_layout()
    plt.savefig("figures for top15 of severity rankings/"+route_direct_id+".png")
    plt.close()
    
    combination_df.to_csv("combinations for top15 of severity rankings/"+route_direct_id+".csv")

