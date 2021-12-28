# Potential improvements: Refining of hyperparameters, hidden layer sizes, alpha, learning rate, etc.
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from transfer_data import *
import pandas as pd

# MLP = Multi-layer perceptron
def MLP(X, y, X_2022):
    pass

def main():
    X, y = get_all_player_stats()
    X_2022 = get_2022_stats()
    MLP(X, y, X_2022)

if __name__ == "__main__":
    main()