import os
import functools

class MSD:
    """
    Calculate MSD in choosen or all XYZ directions

    """
    def __init__(self, input, *atoms):
        self.outputPath = input
        self.inputPath = input+'/traj.tmp'
        self.atoms = atoms

    def sorter(self):
        """
        :return: Tworzy osobne, posortowane pliki dla każdego z atomu z cząsteczki dla której MSD ma być policzone
        """
        print('---Creating sorted files for every atom---')
        try:
            for atom in self.atoms:
                with open(self.inputPath, 'r') as file:
                    out = self.outputPath+f'/{atom}.tmp'
                    output = open(out, 'w')
                    for line in file:
                         if atom.strip() == line.split()[1]:
                             output.write(line.rstrip()+'\n')
                    output.close()
        except Exception as e:
            print(f'\n\n{e}')
            print('!Error - sorted files not created!')
        else:
            print(f"---Sorted files for {','.join(self.atoms)} created in '{self.outputPath}'---")

    @functools.lru_cache()
    def __MSDforSingleAtomInSingleDirection(self, atom, direction):
        """
        Liczy MSD dla jednego atomu w jedym kierunku
        """
        initial = []  # Lista wartości od których odejmujemy positions
        position = [] # Lista wartości które odejmujemy od initials
        diff = [] # Lista kwadratów różnicy initial i position
        sumDiff = 0 # Suma różnicy kwadratów
        MSDForSingleAtomInSingleDirection = {}

        try:
            with open(self.outputPath+f'/{atom}.tmp','r') as file:
                for line in file:
                    initial.append(line.split()[direction])  # Tworzenie listy koordynat w jednym kierunku (direction)

                position = initial.copy() # kopiowanie koordynat
                initial.pop() # usunięcie ostatniej koordynaty dla wartości od których będziemy odejmować
                position.remove(position[0]) # usunięcie pierwszej koordynaty dla wartości które będziemy odejmować
                for i, p in zip(initial, position):
                    diff.append((float(i)-float(p))**2)#Tworrzenie lity kwadadratów różnic
                for step, difference in enumerate(diff):
                    sumDiff += difference # dodawanie różnicy kwadratów dla każdego timestepu
                    MSDForSingleAtomInSingleDirection[step] = sumDiff # tworzenia słownika timestep : MSD dla jednego atomu w jednym kierunku

            return MSDForSingleAtomInSingleDirection

        except Exception as e:
            print(f'\n\n{e}')
            print(f'!Error - MSD not calculated for {atom}')

    @functools.lru_cache()
    def __MSDforAllAtomsInSingleDirection(self, direction, atoms):
        """
        Sumuje MSD dla wszytkich atomów w jedym kierunku i dzieli przz liczę atomow
        """
        try:
            # Tworzenie pustego słownika timestep MSD : dla wszystkich atomów
            MSDforAllAtomsInSingleDirection = {}
            for index in range(len(self.__MSDforSingleAtomInSingleDirection(atoms[0],direction))):
                MSDforAllAtomsInSingleDirection[index] = 0

            # sumowanie MSD dla każdego z atomów
            for atom in atoms:
                for index in range(len(self.__MSDforSingleAtomInSingleDirection(atom,direction))):
                    MSDforAllAtomsInSingleDirection[index] += self.__MSDforSingleAtomInSingleDirection(atom,direction)[index]
            # Dzielenie MSD dla każdego timestepu przez liczbę atomów
            for index in range(len(self.__MSDforSingleAtomInSingleDirection(atoms[0],direction))):
                MSDforAllAtomsInSingleDirection[index] = MSDforAllAtomsInSingleDirection[index]/len(atoms)

            return MSDforAllAtomsInSingleDirection

        except Exception as e:
            print(f'\n\n{e}')
            print(f'!Error - MSD not calculated for {atoms}')


    def MSDX(self):
        """
        calculates MSD in X direction and saves in msd.msdX attribute
        """
        print('---Calculating MSD in X direction---')
        try:
            self.msdX = self.__MSDforAllAtomsInSingleDirection(2, self.atoms)
            print('---MSD calculated in X direction')
        except Exception as e:
            print(f'\n\n{e}')
            print(f'!Error - MSD not calculated in X direction')




    def MSDY(self):
        """
        calculates MSD in Y direction and saves in msd.msdY attribute
        """
        print('---Calculating MSD in Y direction---')
        try:
            self.msdY = self.__MSDforAllAtomsInSingleDirection(3, self.atoms)
            print('---MSD calculated in Y direction')
        except Exception as e:
            print(f'\n\n{e}')
            print(f'!Error - MSD not calculated in Y direction')



    def MSDZ(self):
        """
        calculates MSD in Z direction and saves in msd.msdZ attribute
        """
        print('---Calculating MSD in Z direction---')
        try:
            self.msdZ = self.__MSDforAllAtomsInSingleDirection(4, self.atoms)
            print('---MSD calculated in Z direction')
        except Exception as e:
            print(f'\n\n{e}')
            print(f'!Error - MSD not calculated in Z direction')



    def MSD(self):
        """
        Calculates MSD as sum of MSD in all directions and saves in msd.msd
        """
        print('---Calculating MSD in all directions---')
        self.msdX = self.__MSDforAllAtomsInSingleDirection(2, self.atoms)
        print('---Calculated for X---')
        self.msdY = self.__MSDforAllAtomsInSingleDirection(3, self.atoms)
        print('---Calculated for Y---')
        self.msdZ = self.__MSDforAllAtomsInSingleDirection(4, self.atoms)
        print('---Calculated for Z---')

        # Tworzenie pustego słownika timestep : MSD dla wszystkich atomów we wszystkich kierunkach
        MSDforAllAtoms = {}
        for index in range(len(self.msdX)):
            MSDforAllAtoms[index] = 0
        print('---Summing MSD from XYZ---')
        # sumowanie MSD dla każdego z atomów w każdym kierunku
        for key, value in MSDforAllAtoms.items():
            MSDforAllAtoms[key] = self.msdX[key] + self.msdY[key] +self.msdZ[key]

        self.msd = MSDforAllAtoms


    def deleteTmp(self):
        """
        delete all temporary files
        """
        try:
            os.remove(f'{self.outputPath}/traj.tmp')
            for atom in self.atoms:
                os.remove(f'{self.outputPath}/{atom}.tmp')
        except Exception as e:
            print(f'\n\n{e}')
            print(f'!Error - Temporary files not deleted!')
        else:
            print('---Temporary files deleted successfully---')













