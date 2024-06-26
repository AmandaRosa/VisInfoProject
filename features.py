import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from filters import LowPassFilter
from timedomain import TimeDomain
import numpy as np
import random

def read_data(directory_path, dict_data):

    array_data = list()

    arrays = [[] for _ in range(0, 9)]
    i=0
    for root, dirs, files in os.walk(directory_path):
        key = os.path.relpath(root, start="../data_unbalanced_g")
        for file in sorted(files):
            if i==0:
                i+=1
                if file.endswith(".txt"):
                    print(file)
                    file_path = os.path.join(root, file)

                    with open(file_path, "r") as f:
                        lines = f.readlines()
                        filtered_data = [item.strip() for item in lines if item.strip()]
                        for item in filtered_data:
                            array_info = item.split(";")
                            for i in range(0, 9):
                                arrays[i].append(float(array_info[i]))
                        # array_data_normal1 = (np.array(arrays))
                        # print(array_data_normal1.shape)

    array_data = np.array(arrays)
    dict_data[key] = array_data.T
    return dict_data

def add_noise(signal, percentage=0.025):
    """
    Add Gaussian noise to the input signal based on a percentage of the signal's amplitude.

    Parameters:
        signal (numpy.ndarray): Input signal.
        percentage (float): Percentage of the signal's amplitude to use as the noise level.

    Returns:
        numpy.ndarray: Noisy signal.
    """
    if percentage < 0 or percentage > 1:
        raise ValueError("Percentage must be between 0 and 1")

    noise = np.random.normal(scale=1, size=len(signal))
    noise_level = percentage * np.sqrt(np.mean((signal - np.mean(signal)) ** 2))
    noisy_signal = signal + noise_level * noise
    return noisy_signal

class Features:

    def __init__(self):

        self.dict_data = {}

        self.dict_data_final = read_data("../data/Normal_1/", self.dict_data)
        self.dict_data_final = read_data("../data/Unbalance_30_g/", self.dict_data)
        self.dict_data_final = read_data("../data/Horizontal_Misalignment_2_0mm/", self.dict_data)
        self.dict_data_final = read_data("../data/Vertical_Misalignment_1.27_mm/", self.dict_data)
        self.dict_data_final = read_data("../data/Ver. Misalignment_1.27_mm+Hor. Misalignment_2_mm/", self.dict_data)
        self.dict_data_final = read_data("../data/Unbalance_30_g+Hor. Misalignment_2.0_mm/", self.dict_data)
        self.dict_data_final = read_data("../data/Unbalance_30_g+Ver. Misalignment_1.27_mm/", self.dict_data)

        self.channels = ['ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8']
        self.normal1_signal = {channel: [] for channel in self.channels}
        self.unbalanced30g_signal = {channel: [] for channel in self.channels}
        self.horizontalmisalign_2mm_signal = {channel: [] for channel in self.channels}
        self.verticalmisalign_1_27mm_signal = {channel: [] for channel in self.channels}
        self.verticalmisalign_1_27mm_horizontalmisaling_2_mm_signal = {channel: [] for channel in self.channels}
        self.Unbalance_30_g_Hor_Misalignment_2_0_mm_signal = {channel: [] for channel in self.channels}
        self.Unbalance_30_g_Ver_Misalignment_1_27_mm_signal = {channel: [] for channel in self.channels}

        for i in range(2,9,1):

            for array in self.dict_data_final["../data/Normal_1"]:
                self.normal1_signal[f'ch{i}'].append(array[i-1])  # Assuming column 1 is time_vector

            for array in self.dict_data_final["../data/Unbalance_30_g"]:
                self.unbalanced30g_signal[f'ch{i}'].append(array[i-1]) # Assuming column 1 is time_vector

            for array in self.dict_data_final["../data/Horizontal_Misalignment_2_0mm"]:
                self.horizontalmisalign_2mm_signal[f'ch{i}'].append(array[i-1]) # Assuming column 1 is time_vector

            for array in self.dict_data_final["../data/Vertical_Misalignment_1.27_mm"]:
                self.verticalmisalign_1_27mm_signal[f'ch{i}'].append(array[i-1]) # Assuming column 1 is time_vector

            for array in self.dict_data_final["../data/Ver. Misalignment_1.27_mm+Hor. Misalignment_2_mm"]:
                self.verticalmisalign_1_27mm_horizontalmisaling_2_mm_signal[f'ch{i}'].append(array[i-1]) # Assuming column 1 is time_vector

            for array in self.dict_data_final["../data/Unbalance_30_g+Hor. Misalignment_2.0_mm"]:
                self.Unbalance_30_g_Hor_Misalignment_2_0_mm_signal[f'ch{i}'].append(array[i-1]) # Assuming column 1 is time_vector

            for array in self.dict_data_final["../data/Unbalance_30_g+Ver. Misalignment_1.27_mm"]:
                self.Unbalance_30_g_Ver_Misalignment_1_27_mm_signal[f'ch{i}'].append(array[i-1]) # Assuming column 1 is time_vector

        self.noise_values = np.linspace(0.001, 0.2, 5)

        self.normal1_signal_list = {channel: [] for channel in self.channels}
        self.unbalanced30g_signal_list = {channel: [] for channel in self.channels}
        self.horizontalmisalign_2mm_signal_list = {channel: [] for channel in self.channels}
        self.verticalmisalign_1_27mm_signal_list = {channel: [] for channel in self.channels}
        self.verticalmisalign_1_27mm_horizontalmisaling_2_mm_signal_list = {channel: [] for channel in self.channels}
        self.Unbalance_30_g_Hor_Misalignment_2_0_mm_signal_list = {channel: [] for channel in self.channels}
        self.Unbalance_30_g_Ver_Misalignment_1_27_mm_signal_list = {channel: [] for channel in self.channels}

        for i in range(2,9,1):
            self.normal1_signal_list[f'ch{i}'] = [None] * len(self.noise_values)
            self.unbalanced30g_signal_list[f'ch{i}'] = [None] * len(self.noise_values)
            self.horizontalmisalign_2mm_signal_list[f'ch{i}'] = [None] * len(self.noise_values)
            self.verticalmisalign_1_27mm_signal_list[f'ch{i}'] = [None] * len(self.noise_values)
            self.verticalmisalign_1_27mm_horizontalmisaling_2_mm_signal_list[f'ch{i}'] = [None] * len(self.noise_values)
            self.Unbalance_30_g_Hor_Misalignment_2_0_mm_signal_list[f'ch{i}'] = [None] * len(self.noise_values)
            self.Unbalance_30_g_Ver_Misalignment_1_27_mm_signal_list[f'ch{i}'] = [None] * len(self.noise_values)

        sample = 0
        for noise_level in self.noise_values:
            for i in range(2,9,1):
                self.normal1_signal_list[f'ch{i}'][sample] = LowPassFilter(add_noise(self.normal1_signal[f'ch{i}'], noise_level))
                self.unbalanced30g_signal_list[f'ch{i}'][sample] = LowPassFilter(add_noise(self.unbalanced30g_signal[f'ch{i}'], noise_level))
                self.horizontalmisalign_2mm_signal_list[f'ch{i}'][sample] = LowPassFilter(add_noise(self.horizontalmisalign_2mm_signal[f'ch{i}'], noise_level))
                self.verticalmisalign_1_27mm_signal_list[f'ch{i}'][sample] = LowPassFilter(add_noise(self.verticalmisalign_1_27mm_signal[f'ch{i}'], noise_level))
                self.verticalmisalign_1_27mm_horizontalmisaling_2_mm_signal_list[f'ch{i}'][sample] = LowPassFilter(add_noise(self.verticalmisalign_1_27mm_horizontalmisaling_2_mm_signal[f'ch{i}'], noise_level))
                self.Unbalance_30_g_Hor_Misalignment_2_0_mm_signal_list[f'ch{i}'][sample] = LowPassFilter(add_noise(self.Unbalance_30_g_Hor_Misalignment_2_0_mm_signal[f'ch{i}'], noise_level))
                self.Unbalance_30_g_Ver_Misalignment_1_27_mm_signal_list[f'ch{i}'][sample] = LowPassFilter(add_noise(self.Unbalance_30_g_Ver_Misalignment_1_27_mm_signal[f'ch{i}'], noise_level))
            sample+=1

        subsample = 50000
        time_domain_instance = TimeDomain(subsample=subsample)

        features_function = {
                            # 'Margin_Factor': time_domain_instance.margin_factor, 
                            # 'Mean_Value': time_domain_instance.mean_value, 
                            # 'Peak_to_Peak_Amplitude': time_domain_instance.peak_to_peak_amplitude,  
                            'Root_Mean_Square': time_domain_instance.root_mean_square, 
                            # 'Shape_Factor': time_domain_instance.shape_factor,
                            # 'Skewness': time_domain_instance.skewness, 
                            # 'Standard_Error': time_domain_instance.standard_error, 
                            # 'Std': time_domain_instance.std, 
                            # 'Variance': time_domain_instance.variance, 
                            # 'Wavelength': time_domain_instance.wavelength, 
                            # 'Wilson_Amplitude': time_domain_instance.wilson_amplitude,
                            # 'Zero_Crossing': time_domain_instance.zero_crossing, 
                            # 'Average_Mean_from_Envelope': time_domain_instance.average_mean_from_envelope, 
                            # 'Clearance_Factor': time_domain_instance.clearance_factor,
                            # 'Crest_Factor': time_domain_instance.crest_factor, 
                            # 'Entropy': time_domain_instance.entropy, 
                            # 'Impulse_Factor': time_domain_instance.impulse_factor, 
                            # 'Kurtosis': time_domain_instance.kurtosis,
                            # 'Peak_Acceleration': time_domain_instance.peak_acceleration
        }

        dict_features_labels = {}

        for channel in self.channels:
            print(f'CHANNEL:{channel}')
            dict_features_labels[channel] = {}
            for key, func in features_function.items():
                features = []
                labels = []

                for sample in range(0,5,1):

                    normal1_signal_filtered = self.normal1_signal_list[channel][sample]
                    unbalanced30g_signal_filtered = self.unbalanced30g_signal_list[channel][sample]
                    horizontalmisalign_2mm_signal_filtered = self.horizontalmisalign_2mm_signal_list[channel][sample]
                    verticalmisalign_1_27mm_signal_filtered = self.verticalmisalign_1_27mm_signal_list[channel][sample]
                    verticalmisalign_1_27mm_horizontalmisaling_2_mm_signal_filtered = self.verticalmisalign_1_27mm_horizontalmisaling_2_mm_signal_list[channel][sample]
                    Unbalance_30_g_Hor_Misalignment_2_0_mm_signal_filtered = self.Unbalance_30_g_Hor_Misalignment_2_0_mm_signal_list[channel][sample]
                    Unbalance_30_g_Ver_Misalignment_1_27_mm_signal_filtered = self.Unbalance_30_g_Ver_Misalignment_1_27_mm_signal_list[channel][sample]

                    array_X_normal_signal = []
                    array_y_normal_signal = []
                    array_X_fault1_signal = []
                    array_y_fault1_signal = []
                    array_X_fault2_signal = []
                    array_y_fault2_signal = []
                    array_X_fault3_signal = []
                    array_y_fault3_signal = []
                    array_X_fault4_signal = []
                    array_y_fault4_signal = []
                    array_X_fault5_signal = []
                    array_y_fault5_signal = []
                    array_X_fault6_signal = []
                    array_y_fault6_signal = []

                    array_method_normal_signal = func(normal1_signal_filtered)
                    array_method_fault1_signal = func(unbalanced30g_signal_filtered)
                    array_method_fault2_signal = func(horizontalmisalign_2mm_signal_filtered)
                    array_method_fault3_signal = func(verticalmisalign_1_27mm_signal_filtered)
                    array_method_fault4_signal = func(verticalmisalign_1_27mm_horizontalmisaling_2_mm_signal_filtered)
                    array_method_fault5_signal = func(Unbalance_30_g_Hor_Misalignment_2_0_mm_signal_filtered)
                    array_method_fault6_signal = func(Unbalance_30_g_Ver_Misalignment_1_27_mm_signal_filtered)
                
                    array_method_normal_signal = np.array(array_method_normal_signal)
                    array_method_fault1_signal = np.array(array_method_fault1_signal)
                    array_method_fault2_signal = np.array(array_method_fault2_signal)
                    array_method_fault3_signal = np.array(array_method_fault3_signal)
                    array_method_fault4_signal = np.array(array_method_fault4_signal)
                    array_method_fault5_signal = np.array(array_method_fault5_signal)
                    array_method_fault6_signal = np.array(array_method_fault6_signal)

                    size1 = array_method_normal_signal.shape[0]
                    size2 = array_method_fault1_signal.shape[0]
                    size3 = array_method_fault2_signal.shape[0]
                    size4 = array_method_fault3_signal.shape[0]
                    size5 = array_method_fault4_signal.shape[0]
                    size6 = array_method_fault5_signal.shape[0]
                    size7 = array_method_fault6_signal.shape[0]

                    min_size = min(size1, size2, size3, size4, size5, size6, size7)

                    array_method_normal_signal = array_method_normal_signal[:min_size]
                    array_method_fault1_signal = array_method_fault1_signal[:min_size]
                    array_method_fault2_signal = array_method_fault2_signal[:min_size]
                    array_method_fault3_signal = array_method_fault3_signal[:min_size]
                    array_method_fault4_signal = array_method_fault4_signal[:min_size]
                    array_method_fault5_signal = array_method_fault5_signal[:min_size]
                    array_method_fault6_signal = array_method_fault6_signal[:min_size]
                    
                    labels_normal = np.zeros(len(array_method_normal_signal))
                    labels_fault1 = np.ones(len(array_method_fault1_signal))
                    labels_fault2 = np.full(len(array_method_fault2_signal), 2)
                    labels_fault3 = np.full(len(array_method_fault3_signal), 3)
                    labels_fault4 = np.full(len(array_method_fault4_signal), 4)
                    labels_fault5 = np.full(len(array_method_fault5_signal), 5)
                    labels_fault6 = np.full(len(array_method_fault6_signal), 6)

                    array_X_normal_signal.append(array_method_normal_signal)
                    array_y_normal_signal.append(labels_normal)

                    array_X_fault1_signal.append(array_method_fault1_signal)
                    array_y_fault1_signal.append(labels_fault1)

                    array_X_fault2_signal.append(array_method_fault2_signal)
                    array_y_fault2_signal.append(labels_fault2)

                    array_X_fault3_signal.append(array_method_fault3_signal)
                    array_y_fault3_signal.append(labels_fault3)

                    array_X_fault4_signal.append(array_method_fault4_signal)
                    array_y_fault4_signal.append(labels_fault4)

                    array_X_fault5_signal.append(array_method_fault5_signal)
                    array_y_fault5_signal.append(labels_fault5)

                    array_X_fault6_signal.append(array_method_fault6_signal)
                    array_y_fault6_signal.append(labels_fault6)

                    self.features_normal = array_method_normal_signal.reshape(min_size, -1)
                    self.features_fault1 = array_method_fault1_signal.reshape(min_size, -1)
                    self.features_fault2 = array_method_fault2_signal.reshape(min_size, -1)
                    self.features_fault3 = array_method_fault3_signal.reshape(min_size, -1)
                    self.features_fault4 = array_method_fault4_signal.reshape(min_size, -1)
                    self.features_fault5 = array_method_fault5_signal.reshape(min_size, -1)
                    self.features_fault6 = array_method_fault6_signal.reshape(min_size, -1)

    def escolher_chave(self, dict_disparo):
            # Definindo as chaves
            chaves = list(dict_disparo.keys())
            
            # Definindo as probabilidades, com 80% para 'Normal'
            probabilidades = [0.8 if chave == 'Normal' else 0.2 / (len(chaves) - 1) for chave in chaves]
            
            # Escolhendo uma chave aleatoriamente com base nas probabilidades
            chave_escolhida = random.choices(chaves, weights=probabilidades, k=1)[0]
            
            # Retornando a chave e o valor correspondente
            return chave_escolhida, dict_disparo[chave_escolhida]
    
    
    def disparar(self):

        dict_disparo = {
            'Normal': self.features_normal,
            'Unbalanced_30g': self.features_fault1,
            'Horizontal_Mis_2mm': self.features_fault2,
            'Vertical_Mis_127mm': self.features_fault3,
            'Vertical_127_Hor_2_Mis': self.features_fault4,
            'Unbalanced_30g_Hor_Mis_2mm': self.features_fault5,
            'Unbalanced_30g_Ver_Mis_127mm': self.features_fault6
        }

        chave, valor = self.escolher_chave(dict_disparo)
        return chave,valor