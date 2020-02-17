from cut import TrajProces
from MSD import MSD
from graph import Graph

####CHOOSE!
input = 'test.xyz' #path to input trajectory
output = '/tmp' #path to create temporary files
atoms = ['O5','C5','O6'] #atoms building molecule that you want to calculate MSD for.

"""
Processing initial trajctory to select only atoms of interest
"""
traj = TrajProces(input,output)
traj.inputGenerator(*atoms)

"""
msd options:
sorter - creats sorted files for single atoms
deleteTmp - deletes temporary files in output dictionary.
MSDX - calculates MSD in X direction and saves in msd.msdX
MSDY - calculates MSD in Y direction and saves in msd.msdY
MSDZ - calculates MSD in Z direction and saves in msd.msdZ
MSD - calculates MSD as a sum of MSD in every diection and saves in msd.msd + creates all msd.X/Y/Z attributes
"""
msd = MSD(output, *atoms)
msd.sorter()
msd.MSD()
msd.deleteTmp()


"""
graph creating
Grap(data, timestep in ps, title)
"""

fig1 = Graph(msd.msd, 0.01, 'MSD')
fig1.plot()

