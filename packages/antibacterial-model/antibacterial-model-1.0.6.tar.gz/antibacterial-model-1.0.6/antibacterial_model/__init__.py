from antibacterial_model.model import AntibacterialModel


if __name__ == '__main__':
    model = AntibacterialModel()
    model.predict("input.txt", "output.txt")