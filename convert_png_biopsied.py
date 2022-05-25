# This is a file for converting the DICOMs to PNG images.
# Here the whole dataset from biopsied groups: {"Benign", "Cancer"} is being converted.

import os

# %matplotlib inline
import matplotlib.pyplot as plt

from duke_dbt_data import dcmread_image, read_boxes, draw_box

datasource = "/mnt/seagate/DBT/manifest-1617905855234"

boxes_path = os.path.join(datasource, "BCS-DBT boxes-train-v2.csv")
filepaths_path = os.path.join(datasource, "BCS-DBT file-paths-train-v2.csv")

df =  read_boxes(boxes_fp= boxes_path, filepaths_fp= filepaths_path)

print(df.head())
print("Shape of df:", df.shape)

print(df.columns.tolist())

# Create a function for the preprocessing of strings:
# At the descriptive files, the "-NA" part of the strings was missing!!!
def str_preproc(image_path):
  str_cropped = image_path.split('000000')
  str_combined = str_cropped[0] + "000000-NA" + str_cropped[1]
  return str_combined


# Try automate the above procedure for all volumes from all patients (paths_list -> paths_list_whole):
paths_list_whole = []

for ind in df.index:
  str_processed = str_preproc(df['descriptive_path'][ind])
  print(df['PatientID'][ind],str_processed)
  # paths_list.append(df['descriptive_path'][ind])
  paths_list_whole.append(str_processed)


print()
print(paths_list_whole[0])
print()

import matplotlib
import cv2
import numpy as np


for iter in range(len(paths_list_whole)):
  box_series = df.iloc[iter]
  patient = box_series["PatientID"]
  study = box_series["StudyUID"]
  view = box_series["View"]
  num_slices = box_series["VolumeSlices"]
  slice_index = box_series["Slice"]

  print("iteration:",iter)
  print("patient:", patient)
  print("study:",study)
  print("view:", view)

  specific_path = "saved_png_biopsied/" + str(patient) + "/" + str(study)
  os.makedirs(specific_path,exist_ok=True)
  image_read_path = os.path.join(datasource, paths_list_whole[iter])

  for slice in range(num_slices):
    image = dcmread_image(fp=image_read_path, view=view, index=slice)
    
    write_path = "saved_png_biopsied/" + str(patient) + "/" + str(study)
    cv2.imwrite(os.path.join(write_path , str(view.upper()) + "TomosynthesisReconstruction_" + str(slice) + "_.png"),image)
