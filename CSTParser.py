import re
import csv
import matplotlib.pyplot as plt
import numpy as np

# (?<=-{70}\n)(\s|.)*?(?=(?:^\s*$))
# (?<=-{70}\n)(?:[\s\S]*?)(?=(?:^\s*$)) Fixed catastrophic backtracking
# Last line in the dataset should be empty means two empty lines at last of the dataset otherwise the regex match fails
class CSTParser:
    data_regex = r'(?<=-{70}\n)(?:\s|.)*?(?=\n\n)'
    mid_regex = r' {10,}(?=-)'
    start_regex = r' +(?=\d)'
    fmin = 0.5
    fmax = 5
    list_params = ['run_id' , 'a' , 'r0' , 'theta0' , "Fl" , "Fh"];

    # parameters_list_sequence = run_id , a , r0 , theta0

    def __init__(self , filename , listfilename):
        with open(filename , 'r') as file:
            self.process_cst_export(file.read())

        with open(listfilename , 'r') as file:
            self.process_cst_list(file)

    def process_cst_list(self , file):
            lines = csv.reader(file);
            csv_lines = []
            for i in lines:
                csv_lines.append(i)
            csv_lines = np.array(csv_lines[1:-1] , dtype="float")
            self.cst_list = csv_lines      # cst parameters list lines

    def process_cst_export(self , cst_export):
        regex_compiled = re.compile(self.data_regex);
        self.parsed_cst = regex_compiled.findall(cst_export); # array of datasets of strings

    def process_dataset(self , processed_cst):
        dataset = re.sub(self.mid_regex , ',' , processed_cst)
        dataset = re.sub(self.start_regex , '' , dataset)
        return dataset
        
    def calculateFreq(self , dataset):
        lines = self.process_dataset(dataset).splitlines()
        return list(csv.reader(lines));

    def calculateflh(self , data):
        flag = False;
        fl = self.fmin;
        fh = self.fmax;
        for row in data:
            if float(row[-1]) < -10 :
                fh = float(row[0]);
                flag = True;
            else :
                if(flag):
                    break;
                fl = float(row[0])
        return [fl , fh]

    def plot_graph(self , run_id):
        data_dict = self.generate_data_dict()[run_id-1]
        dataset = data_dict["dataset"]
        list_lines = data_dict["run_info"]
        arr = np.asarray(dataset , dtype=float)
        x_points = arr[:,0]
        y_points = arr[:,1]
        plt.plot(x_points , y_points , label=self.cst_list_label(list_lines))
        plt.legend()
        plt.xlabel("Frequency / GHZ")
        plt.ylabel("db")
        plt.title("S Parameters [Magnitude in db]")
        plt.grid(True)
        plt.show()

    def cst_list_label(self , arr):
        title = ''
        for a , b in zip(self.list_params , arr):
            title += str(a) + '=' + str(b) + ','

        return title

    def plot_graphs(self):
        for i in self.generate_data_dict():
            dataset = i["dataset"]
            list_lines = i["run_info"]
            arr = np.asarray(dataset , dtype=float)
            x_points = arr[:,0]
            y_points = arr[:,1]
            plt.plot(x_points , y_points , label=self.cst_list_label(list_lines))

        plt.legend()
        plt.xlabel("Frequency / GHZ")
        plt.ylabel("db")
        plt.title("S Parameters [Magnitude in db]")
        plt.grid(True)
        plt.show()

    def generate_data_dict(self):
        data_dict = [] # A dictionary of all different parameters and different values
        index = 1;
        for dataset , list_lines in zip(self.parsed_cst , self.cst_list):
            dct = {};
            rows = self.calculateFreq(dataset);
            flh = self.calculateflh(rows);
            dct["run_info"] = list(list_lines);
            dct["run_info"].append(flh[0]);
            dct["run_info"].append(flh[1]);
            dct["dataset"] = rows;
            index += 1;
            data_dict.append(dct)
        return data_dict


    def generate_csv(self , filename):
        csv_data = []
        for dataset in self.generate_data_dict():
            csv_data.append(dataset["run_info"])

        with open(filename , 'w' , encoding='UTF-8' , newline='')  as file:
            writer = csv.writer(file)
            writer.writerow(self.list_params);
            writer.writerows(csv_data)



cst_data = CSTParser('cst_ascii_export.txt' , 'cst_linear_sweep_export.csv');
cst_data.generate_csv('ml_dataset.csv');
# cst_data.plot_graph(10)