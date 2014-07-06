# Practice program using MJ's statistics homework
# Requires NBAPlayer2011.xls file to be in same directory
# This program practices importing the .xls file, pulling a 
# column of data, poping out the title, and plotting the data as 
# a box plot

import numpy as np
from pylab import *
from scipy.io import loadmat
from xlrd import open_workbook

#importing NBA player data and pulling player 'blocked shots' data
data = open_workbook('NBAPlayers2011.xls')
sheet0 = data.sheet_by_index(0)
blocks = sheet0.col_values(21)
blocks.pop(0)
blks = np.array(blocks)

figure(1)
boxplot(blks, vert=False)
title('NBA Player blocked shots')
xlabel('# of Shots Blocked')
ylabel('Number of shots blocked')

figure(2)
hist(blks, bins=10)

show()
