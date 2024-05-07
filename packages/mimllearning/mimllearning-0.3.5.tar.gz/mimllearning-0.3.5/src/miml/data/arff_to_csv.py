def arff_to_csv(file: str, delimiter: str = "'") -> None:
    """
    Convert MIML Arff to CSV.

    Parameters
    ----------
    file : str
        Filepath of the file to be converted

    delimiter : str, default = '
        Delimiter used in arff file for the start and end of the bag values ( ' or " )
    """

    arff = open(file)
    csv = open(file[:-5] + ".csv", "w")
    attrib = []
    flag = 0

    for line in arff:
        # Comprobamos que la cadena no contenga espacios en blanco a la izquierda ni que sea vacía
        line = line.lstrip()
        if line == "":
            continue

        if line.startswith("%") or line.startswith("@"):
            if line.startswith("@attribute") and not line.startswith("@attribute bag relational"):
                attrib.append(line.split()[1])

        else:
            if flag == 0:
                csv.write(','.join(attrib) + '\n')
                flag = 1

            # Eliminanos el salto de línea del final de la cadena
            line = line.strip("\n")

            # Asumimos que el primer elemento de cada instancia es el identificador de la bolsa
            key = line[0:line.find(",")]
            # print("Key: ", key_bag)

            # Empiezan los datos de la bolsa cuando encontremos la primera '"' y terminan con la segunda '"'
            line = line[line.find(delimiter) + 1:]
            values = line[:line.find(delimiter, line.find(delimiter, line.find(delimiter)))]
            # Separamos los valores por instancias de la bolsa
            values = values.split("\\n")
            # print("Values ", values)

            # El resto de la cadena se trata de las etiquetas
            labels = line[line.find(delimiter, line.find(delimiter, line.find(delimiter))) + 2:]
            # print("Labels: ", labels)

            for v in values:
                csv.write(key + "," + v + "," + labels + "\n")
                # TODO: intentar optimizar la funcion, aprovechar que la string del arff
                # es parecida, separar solo los values
                # TODO: control de errores

    arff.close()
    csv.close()
