class TrajProces:

    """
    inputGenerator - Wycina z trajektorii tylko atomy dla który ma być policzone MSD
    inputSort - Tworzy osobne, posortowane pliki dla każdego atomu, dla którego ma być policzone MSD

    """

    def __init__(self, inputPath, outputPath):
        """
        :param inputPath: Plik XYZ z trajektorią
        :param outputPath: Miejsce do tworzenia plików tymaczasowych
        """
        self.outputPath = outputPath+'/traj.tmp'
        self.path = inputPath

    def inputGenerator(self, *atoms):
        """
        :param atoms: Atomy dla których ma być liczone MSD np. O5, C5, O6
        :return: Tworzy plik tymczasowy z wyciętymi atomami do obróbki
        """
        try:
            print('---File processing---')

            output = open(self.outputPath, 'w')

            with open(self.path, 'r') as file:
                output.write('Index | Atom | X | Y | Z |\n')
                for line in file:
                    for index, atom in enumerate(atoms):
                        if line.startswith(atom):
                            templine = line.rsplit()
                            output.write(f'{index}   {templine[0]}    {templine[1]}   {templine[2]}   {templine[3]}\n')
            output.close()
        except Exception as e:
            print(f'\n\n{e}')
            print('!Error - temporary file not created!')
        else:
            print(f"---Trajectory for {','.join(atoms)} created in '{output.name}'---")

