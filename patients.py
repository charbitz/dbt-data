import pandas as pd
import numpy as np

# Reading the csv file with category labels, containing both the biopsied volumes (200) and the normal ones (+200): 
df_labels = pd.read_csv("/mnt/seagate/DBT/duke-dbt-data_github/data/manifest-1617905855234/BCS-DBT labels-new-v0.csv")

# Printing to check the dataframe:
print(df_labels.head())
print()
print("df shape:", df_labels.shape)
print(df_labels.columns.tolist())

# Creating a set for all Patients in the biopsied :{"Benign", "Cancer"} groups:
set_biopsied = set(df_labels[(df_labels["Benign"] == 1) | (df_labels["Cancer"] == 1)]["PatientID"])
print("Number of patients at the biopsied groups:", len(set_biopsied))

# Creating a set for all patients in the "Normal" group:
set_normal = set(df_labels[df_labels["Normal"] == 1]["PatientID"])
print("Number of patients at the 'Normal' group:", len(set_normal))

# Creating a set for all patients in two previously sets to check if there are common parts:
set_final = set_biopsied.union(set_normal)
print("Number of patients at all 3 groups:", len(set_final))

# set_final = sorted(set_final)
#
# # Printing all unique patients:
# for i in set_final:
#   print(i)
#
# # Printing again:
# print(set_final)



set_triplets_norm = set()
list_triplets_norm = []

set_triplets_bio = set()
list_triplets_bio = []


for iter in range(df_labels.shape[0]):
  elem = str(df_labels.loc[iter]["PatientID"]) + str(df_labels.loc[iter]["StudyUID"]) + str(df_labels.loc[iter]["View"])
  if iter >= 200:
    # print("elem:", elem)
    set_triplets_norm.add(elem)
    list_triplets_norm.append(elem)
  set_triplets_bio.add(elem)
  list_triplets_bio.append(elem)



print("Number of normal volumes at PatientID/StudyUID/View in a list:", len(list_triplets_norm))
print("Number of normal volumes at PatientID/StudyUID/View in a set:", len(set_triplets_norm))
 

print("Number of all biopsied and normal volumes at PatientID/StudyUID/View in a list:", len(list_triplets_bio))
print("Number of all biopsied and normal volumes at PatientID/StudyUID/View in a set:", len(set_triplets_bio))





