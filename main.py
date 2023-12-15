import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from tkinter import *
from simpful import *


classifier = None
printer_mark_to_classify = 0
printer_paper_to_classify = 0
printer_age_to_classify = 0
printer_sound_to_classify = 0
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# laser printer, point printer
# not-coloured, coloured
#
features = ['Printer age', 'Printer mark', 'Chews paper', 'Target']
class Node:
    def __init__(self, feature_ind=None, threshold=None, left=None, right=None, info_gain=None, value=None):
        self.feature_ind = feature_ind
        self.threshold = threshold
        self.left = left
        self.right = right
        self.info_gain = info_gain
        self.value = value

class TreeDecision:
    def __init__(self, min_samples_split = 2, max_depth = 3):
        self.root = None
        self.min_samples_spit = min_samples_split
        self.max_depth = max_depth

    def build_tree(self, dataset, curr_depth=1):
        X, Y = dataset[:, :-1], dataset[ :, -1]
        num_samples, num_features = np.shape(X)
        if num_samples >= self.min_samples_spit and curr_depth <= self.max_depth:
            best_split = self.get_best_split(dataset, num_samples, num_features)
            if best_split["info_gain"] > 0:
                left_subt = self.build_tree(best_split["dataset_left"], curr_depth + 1)
                right_subt = self.build_tree(best_split["dataset_right"], curr_depth + 1)
                return Node(best_split["feature_index"], best_split["threshold"],
                            left_subt, right_subt, best_split["info_gain"])
        leaf_val = self.calculate_leaf_val(Y)

        return Node(value=leaf_val)

    def get_best_split(self, dataset, num_samples, num_features):
        best_split = {}
        max_info_gain = -float("inf")

        for feature_index in range(num_features):
            feature_val = dataset[:, feature_index]
            possible_thresholds = np.unique(feature_val)
            for threshold in possible_thresholds:
                dataset_left, dataset_right = self.split(dataset, feature_index, threshold)
                if len(dataset_left) > 0 and len(dataset_right) > 0:
                    y, left_y, right_y = dataset[:, -1], dataset_left[:, -1], dataset_right[:, -1]
                    curr_info_gain = self.information_gain(y, left_y, right_y, "entropy")
                    if curr_info_gain > max_info_gain:
                        best_split["feature_index"] = feature_index
                        best_split["threshold"] = threshold
                        best_split["dataset_left"] = dataset_left
                        best_split["dataset_right"] = dataset_right
                        best_split["info_gain"] = curr_info_gain
                        max_info_gain = curr_info_gain
        return best_split
    def split(self, dataset, feature_ind, threshold):
 #       print(dataset)
        dataset_left = np.array([row for row in dataset if row[feature_ind] <= threshold])
        dataset_right = np.array([row for row in dataset if row[feature_ind] > threshold])
        return dataset_left, dataset_right

    def information_gain(self, parent, l_ch, r_ch, mode="entropy"):
        weight_l = len(l_ch) / len(parent)
        weight_r = len(r_ch) / len(parent)
        if mode == "gini":
            gain = self.gini_index(parent) - (weight_l * self.gini_index(l_ch)) + (weight_r * self.gini_index(r_ch))
        else:
            gain = self.entropy(parent) - (weight_l * self.entropy(l_ch)) + (weight_r * self.entropy(r_ch))
        return gain

    def entropy(self, y):
        class_lbls = np.unique(y)
        entropy = 0
        for cls in class_lbls:
            p_cls = len(y[y == cls]) / len(y)
            entropy += -p_cls * np.log2(p_cls)
        return entropy

    def gini_index(self, x):
        total = 0
        for i, xi in enumerate(x[:-1], 1):
            total += np.sum(np.abs(xi - x[i:]))
        if total == 0:
            return total
        else:
            return total / (len(x) ** 2 * np.mean(x))

    def calculate_leaf_val(self, y):
        Y = list(y)
        unique, counts = np.unique(Y, return_counts = True)
        act = dict(zip(unique.astype(int), np.floor(100 * counts / len(Y)).astype(int)))
        if 0 not in act.keys():
            act[0] = 0
        if 1 not in act.keys():
            act[1] = 0
        return act

    def print_tree(self, tree=None, indent = ' ', left_indent = '<<', right_indent='>>'):
        if not tree:
            tree = self.root

        if tree.value is not None:
            tree.printable = f'{indent}{tree.value}'
            print(tree.printable)
        else:
            self.print_tree(tree.left, indent + indent)
            tree.printable = f'{indent}--{features[tree.feature_ind]}<={int(tree.threshold) if tree.threshold.is_integer() else "%.2f" % tree.threshold}'
            print(tree.printable)
            self.print_tree(tree.right, indent + indent)

    def fit(self, X, Y):
        dataset = np.concatenate((X, Y), axis=1)
        self.root = self.build_tree(dataset)

def test(x, tree):
    root = tree.root
    while not root.value:
        if x[root.feature_ind] >= root.threshold and root.right:
            root = root.right
            print('Go right')
        elif x[root.feature_ind] < root.threshold and root.left:
            root = root.left
            print('Go left')


def sel1():
    global printer_mark_to_classify
    printer_mark_to_classify = int(printer_mark_int.get())

def sel2():
    global printer_paper_to_classify
    printer_paper_to_classify = int(printer_paper_int.get())

def sel3():
    global printer_sound_to_classify
    printer_sound_to_classify = int(printer_sound_int.get())

def test_with_values():
    root = classifier
    tree = root.root
    x = np.array([int(printer_age_string.get()), printer_mark_to_classify, printer_paper_to_classify, int(printer_dpi_string.get())])
    print('x : ', x)
    while not tree.value:
        if x[tree.feature_ind] >= tree.threshold and tree.right:
            tree = tree.right
 #           print('Go right')
        elif x[tree.feature_ind] < tree.threshold and tree.left:
            tree = tree.left
 #           print('Go left')
    print(tree.value)

def fuzzy_rules_and_system_create():
    FS = FuzzySystem()
    S_1 = FuzzySet(function=Triangular_MF(a=0, b=0, c=25), term="quiet")
    S_2 = FuzzySet(function=Triangular_MF(a=20, b=30, c=70), term="medium")
    S_3 = FuzzySet(function=Triangular_MF(a=65, b=80, c=100), term="loud")
    FS.add_linguistic_variable("Sound", LinguisticVariable([S_1, S_2, S_3], concept="Printer sound",
                                                             universe_of_discourse=[0, 100]))
    S_11 = FuzzySet(function=Triangular_MF(a=0, b=0, c=10), term="low")
    S_22 = FuzzySet(function=Triangular_MF(a=0, b=10, c=20), term="medium")
    S_33 = FuzzySet(function=Triangular_MF(a=10, b=20, c=30), term="high")
    FS.add_linguistic_variable("Chewing", LinguisticVariable([S_11, S_22, S_33], concept="Printer chewing",
                                                             universe_of_discourse=[0, 30]))

    S_111 = FuzzySet(function=Triangular_MF(a=0, b=0, c=2), term="young")
    S_222 = FuzzySet(function=Triangular_MF(a=1, b=5, c=6), term="medium")
    S_333 = FuzzySet(function=Triangular_MF(a=4, b=7, c=10), term="old")
    FS.add_linguistic_variable("Age", LinguisticVariable([S_111, S_222, S_333], concept="Printer chewing",
                                                             universe_of_discourse=[0, 10]))

    T_1 = FuzzySet(function=Triangular_MF(a=0, b=0, c=20), term="small")
    T_2 = FuzzySet(function=Triangular_MF(a=10, b=30, c=40), term="average")
    T_3 = FuzzySet(function=Trapezoidal_MF(a=30, b=40, c=55, d=100), term="high")
    FS.add_linguistic_variable("Defects", LinguisticVariable([T_1, T_2, T_3], universe_of_discourse=[0, 100]))

    R1 = "IF (Sound IS loud) THEN (Defects IS high)"
    R2 = "IF (Sound IS quiet) AND (Chewing IS low) OR (Age IS young) AND (Sound IS quiet) THEN (Defects IS small)"
    R3 = "IF (Sound IS medium) AND (Chewing IS high) OR (Age IS young) AND (Sound IS medium) THEN (Defects IS high)"
    R4 = "IF (Sound IS medium) AND (Chewing IS low) OR (Age IS young) AND (Sound IS loud) THEN (Defects IS high)"
    R5 = "IF (Sound IS medium) AND (Chewing IS medium) OR (Age IS old) AND (Sound IS medium) THEN (Defects IS small)"
    R6 = "IF (Sound IS quiet) AND (Chewing IS medium) OR (Age IS medium) AND (Sound IS quiet) THEN (Defects IS small)"
    R7 = "IF (Sound IS quiet) AND (Chewing IS high) OR (Age IS old) AND (Sound IS loud) THEN (Defects IS high)"
    FS.add_rules([R1, R2, R3, R4, R5, R6, R7])

    FS.set_variable("Sound", 99)
    FS.set_variable("Chewing", 20)
    FS.set_variable("Age", 5)
    print(FS.Mamdani_inference(["Defects"]))

printer_age = np.array([1, 2, 5, 12, 10, 2, 1, 13, 15, 2, 6, 8])

le1 = LabelEncoder()
le_paper = LabelEncoder()
le_sound = LabelEncoder()
printer_mark = np.array(le1.fit_transform(['NP', 'Canon', 'Samsung', 'Nixon', 'Samsung', 'NP', 'Samsung', 'NP', 'Samsung', 'Nixon', 'NP', 'Samsung']))
printer_chews_paper = np.array(le_paper.fit_transform(['Very strong', 'Strong', 'Medium', 'Medium', 'Low', 'Low', 'Low', 'Medium', 'Low', 'Medium', 'Medium', 'Low']))
printer_sound = np.array(le_sound.fit_transform(['Very loud', 'Medium Loudness', 'Very loud', 'Quiet', 'Quiet', 'Very loud', 'Very loud', 'Medium Loudness', 'Quiet', 'Quiet', 'Quiet', 'Quiet']))
printer_dpi = np.array([1000, 2000, 500, 300, 500, 600, 800, 800, 900, 1000, 900])
target = np.array([1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0])
dataset = np.array([printer_age, printer_mark, printer_chews_paper, printer_sound, target])
dataset = dataset.transpose()
X, Y = dataset[:, :-1], dataset[:, -1]
Y = Y.reshape(-1, 1)
classifier = TreeDecision(min_samples_split=5, max_depth=10)
classifier.fit(X, Y)
 #   x_test = np.array([4, le1.transform(['NP'])[0], le_paper.transform(['Strong'])[0]])
 #   test(x_test, classifier)
print(printer_mark)
fuzzy_rules_and_system_create()

window = Tk()
window.columnconfigure([0, 1, 2], minsize=100)
window.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], minsize=20)
printer_mark_int = IntVar()
printer_age_string = StringVar()
printer_paper_int = IntVar()
printer_sound_int = IntVar()
printer_dpi_string = StringVar()
label1 = Label(text="Enter printer age")
label1.grid(row=0, column=0)

Entry(window, textvariable = printer_age_string).grid(row=0, column=1, sticky=E)

label2 = Label(text="Enter printer mark")
label2.grid(row=2, column=0)

print(le1.transform(['NP'])[0])
rad1 = Radiobutton(window,  text="NP", variable=printer_mark_int, value=le1.transform(['NP'])[0], command=sel1)
rad2 = Radiobutton(window,  text="Canon", variable=printer_mark_int, value=le1.transform(['Canon'])[0], command=sel1)
rad3 = Radiobutton(window,  text="Samsung", variable=printer_mark_int, value=le1.transform(['Samsung'])[0], command=sel1)
rad4 = Radiobutton(window,  text="Nixon", variable=printer_mark_int, value=le1.transform(['Nixon'])[0], command=sel1)
rad1.grid(row=3, column=0)
rad2.grid(row=3, column=1)
rad3.grid(row=3, column=2)
rad4.grid(row=3, column=3)

label3 = Label(text = "How it chews paper?")
label3.grid(row=4, column=0)
rad11 = Radiobutton(window, text="Very strong", variable=printer_paper_int, value=le_paper.transform(['Very strong'])[0], command=sel2)
rad22 = Radiobutton(window, text="Strong", variable=printer_paper_int, value=le_paper.transform(['Strong'])[0], command=sel2)
rad33 = Radiobutton(window, text="Medium", variable=printer_paper_int, value=le_paper.transform(['Medium'])[0], command=sel2)
rad44 = Radiobutton(window, text="Low", variable=printer_paper_int, value=le_paper.transform(['Low'])[0], command=sel2)
rad11.grid(row=5, column=0)
rad22.grid(row=5, column=1)
rad33.grid(row=5, column=2)
rad44.grid(row=5, column=3)

label4 = Label(text = "How it sounds?")
label4.grid(row=6, column=0)
rad111 = Radiobutton(window, text="Very loud", variable=printer_sound_int, value=le_sound.transform(['Very loud'])[0], command=sel3)
rad222 = Radiobutton(window, text="Medium Loudness", variable=printer_sound_int, value=le_sound.transform(['Medium Loudness'])[0], command=sel3)
rad444 = Radiobutton(window, text="Quiet", variable=printer_sound_int, value=le_sound.transform(['Quiet'])[0], command=sel3)
rad111.grid(row=7, column=0)
rad222.grid(row=7, column=1)
rad444.grid(row=7, column=3)

label5 = Label(text = "Enter DPI")
label5.grid(row=8, column=0)
Entry(window, textvariable = printer_dpi_string).grid(row=8, column=1, sticky=E)

get_button = Button(window, text="Get result", command=test_with_values)
get_button.grid(row=9, column=0)
"""
window.mainloop()

#classifier.print_tree()
"""
