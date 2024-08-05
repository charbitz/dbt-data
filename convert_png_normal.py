import os
import pandas as pd
import pydicom as dicom

# %matplotlib inline
import matplotlib.pyplot as plt


from duke_dbt_data import dcmread_image, read_boxes, draw_box

datasource = "/mnt/seagate/DBT/manifest-1617905855234"

labels_path = os.path.join(datasource, "BCS-DBT labels-new-v0.csv")

df_labels = pd.read_csv(labels_path)


# keep only the volumes from normal group (because the rest is already converted) :
df_normal = df_labels[200:df_labels.shape[0]]

# Create a function for the preprocessing of strings:
# At the descriptive files, the "-NA" part of the strings was missing!!!
def str_preproc(image_path):
  str_cropped = image_path.split('000000')
  str_combined = str_cropped[0] + "000000-NA" + str_cropped[1]
  return str_combined

# Automating the above procedure for all volumes from all patients (paths_list -> paths_list_whole):
paths_list_whole = []

for ind in df_normal.index:
  str_processed = str_preproc(df_normal['descriptive_path'][ind])
  print(df_normal['PatientID'][ind], str_processed)
  # paths_list.append(df['descriptive_path'][ind])
  paths_list_whole.append(str_processed)

import matplotlib
import cv2
import numpy as np

for iter in range(len(paths_list_whole)):
  box_series = df_normal.iloc[iter]
  patient = box_series["PatientID"]
  study = box_series["StudyUID"]
  view = box_series["View"]

  print("volume:",iter)
  print("patient:", patient)
  print("study:",study)
  print("view:", view)

  specific_path = "saved_png_normal/" + str(patient) + "/" + str(study)
  os.makedirs(specific_path,exist_ok=True)
  image_read_path = os.path.join(datasource, paths_list_whole[iter])

  # read the DICOM once to take the number of slices :
  ds = dicom.dcmread(image_read_path)
  num_slices = ds[0x28, 0x08].value
  print("num_slices:", num_slices)

  for iter2 in range(num_slices):

    # try:
    image, num_slices = dcmread_image(fp=image_read_path, view=view, index=iter2)
    write_path = "saved_png_normal/" + str(patient) + "/" + str(study)          # extended_csv
    cv2.imwrite(os.path.join(write_path , str(view.upper()) + "TomosynthesisReconstruction_" + str(iter2) + "_.png"),image)
