import numpy as np
from rdkit import Chem
from rdkit.Chem import Descriptors, EState, rdMolDescriptors, Fragments, GraphDescriptors
from sklearn.preprocessing import StandardScaler
import joblib
import datetime
import pandas as pd
import os

FEATURES_SELECTED = ['EState_VSA10', 'VSA_EState6', 'BCUT2D_LOGPHI', 'fr_lactam',
       'BCUT2D_CHGLO', 'EState_VSA2', 'BalabanJ', 'BCUT2D_MRHI',
       'NumHeteroatoms', 'MaxEStateIndex', 'EState_VSA5', 'Chi3v',
       'VSA_EState4', 'MaxAbsPartialCharge', 'TPSA', 'MinEStateIndex',
       'MinPartialCharge', 'VSA_EState8', 'Chi4v', 'BCUT2D_MWHI']

class AntibacterialModel:
    def __init__(self):
        # Model
        self.currentPath = os.path.dirname(os.path.abspath(__file__) , 'data')
        modelPath = os.path.join(self.currentPath, 'anti-bact-model.pkl')
        
        self.model = joblib.load(modelPath)
        self.model.set_params(random_state=42)
        self.model.feature_names = FEATURES_SELECTED
        
        self.scaler = StandardScaler()
        self.scaler.feature_names = FEATURES_SELECTED
        self._preload_data()
    # Predict from text files which contain SMILES strings
    def predict(self, file_path , output_file_path):
        # Get Data from file
        input_smiles_list = []
        with open(file_path, 'r') as file:
            input_smiles_list = [line.strip() for line in file.readlines()]
        # So if the file is empty, return None
        if len(input_smiles_list) == 0:
            return None
        
        input_desc = self.calculate_descriptors(input_smiles_list)
        scaled_input_desc = self.scale_data(input_desc)
        predictions = self.model.predict(scaled_input_desc)
        result = self.map_to_label(predictions)
        
        if output_file_path is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file_path = f'predictions_{timestamp}.txt'
        
        with open(output_file_path, 'w') as file:
            for smiles, pred in zip(input_smiles_list, result):
                file.write(f'{smiles} - Prediction : {pred}\n')

    def _preload_data(self):
        csvPath = os.path.join(self.currentPath, 'anti-bact-data.csv')
        data = pd.read_csv(csvPath)
        self.scaler.fit(data[self.scaler.feature_names].values)
        
    def scale_data(self, data):
        scaled_data = self.scaler.transform(data)
        return scaled_data
    
    def map_to_label(self, predictions):
        return ['Active' if pred == 1 else 'Inactive' for pred in predictions]
        
    def calculate_descriptors(self, smiles_list):
        descriptors_list = []
        for smiles in smiles_list:
            mol = Chem.MolFromSmiles(smiles)
            descriptors = {
                'EState_VSA10': EState.EState_VSA.EState_VSA10(mol),
                'VSA_EState6': EState.EState_VSA.VSA_EState6(mol),
                'BCUT2D_LOGPHI': Descriptors.BCUT2D_LOGPHI(mol),
                'fr_lactam': Fragments.fr_lactam(mol),
                'BCUT2D_CHGLO': Descriptors.BCUT2D_CHGLO(mol),
                'EState_VSA2': EState.EState_VSA.EState_VSA2(mol),
                'BalabanJ': GraphDescriptors.BalabanJ(mol),
                'BCUT2D_MRHI': Descriptors.BCUT2D_MRHI(mol),
                'NumHeteroatoms': rdMolDescriptors.CalcNumHeteroatoms(mol),
                'MaxEStateIndex': EState.EState.MaxEStateIndex(mol),
                'EState_VSA5': EState.EState_VSA.EState_VSA5(mol),
                'Chi3v': rdMolDescriptors.CalcChi3v(mol),
                'VSA_EState4': EState.EState_VSA.VSA_EState4(mol),
                'MaxAbsPartialCharge': Descriptors.MaxAbsPartialCharge(mol),
                'TPSA': rdMolDescriptors.CalcTPSA(mol),
                'MinEStateIndex': EState.EState.MinEStateIndex(mol),
                'MinPartialCharge': Descriptors.MinPartialCharge(mol),
                'VSA_EState8': EState.EState_VSA.VSA_EState8(mol),
                'Chi4v': rdMolDescriptors.CalcChi4v(mol),
                'BCUT2D_MWHI': Descriptors.BCUT2D_MWHI(mol)
            }
            descriptors_list.append(list(descriptors.values()))
        return np.array(descriptors_list)
    