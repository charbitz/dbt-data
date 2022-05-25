
# Initial csv files: 
#     * BCS-DBT boxes-train-v2.csv  : containing the bounding boxes ground truth ...for 224 bounding boxes...
#     * BCS-DBT labels-train-v2.csv : containing the labels ground truth ...for 19148 volumes...

# Some details about 224 in Biopsied cases:
# 224 are the number of bounding boxes in Biopsied cases,
# But the number of volumes in the Biopsied cases is 200

# New csv files for use: 
#     * BCS-DBT boxes-train-v2.csv  : containing the bounding boxes ground truth ...for 224 bounding boxes (=200 volumes)...
#     * csv_labels_pr.csv           : containing the labels ground truth ...for 400 volumes... (200 from Biopsied cases + 200 from Normal group) 


# New target:
# Now we should append one more column to the file's "csv_labels.csv" dataframe.
# This is the column "descriptive_path" from the "BCS-DBT file-paths-train-v2.csv" file.


import numpy as np
import pandas as pd
import random


def csv_processed(csv_views, seed):

    df_labels = pd.read_csv(
        csv_views, dtype={
            "Normal": np.int, "Actionable": np.int, "Benign": np.int, "Cancer": np.int})

    # The number of samples we want to expand our dataset :
    num_samples = 200
    num_pat_l = 100
    num_pat_r = 100

    # create a new dataframe and keep the Normal cases :
    df_normal = df_labels[df_labels["Normal"] == 1]

    # delete the index in order to be able to iterate later:
    df_normal = df_normal.reset_index(drop=True)

    # create a new dataframe and keep the biopsied cases {Benign, Cancer}:
    df_biopsied = df_labels[(df_labels["Benign"] == 1) | (df_labels["Cancer"] == 1)]

    # delete the index :
    df_biopsied = df_biopsied.reset_index(drop=True)

    # new_df = df_labels.loc[( df_labels['PatientID'] == "DBT-P03258" ) & ( df_labels['View'].isin(["lcc", "lmlo", "lcc1", "lmlo1", "lcc2", "lmlo2"]) )]
    # print()

    # gather all unique patients from Normal group to a set:
    pat_normal_set = set()
    for pat in range(df_normal.shape[0]):
        pat_normal_set.add(str(df_normal.loc[pat]["PatientID"]))

    print("number of unique patients in Normal group :", len(pat_normal_set))

    # copy all unique patients to a list:
    pat_normal_list = list(pat_normal_set)

    print("pat_normal_list length:", len(pat_normal_list))

    # create an empty dataframe, where the new patients will be added :
    df_sampled = pd.DataFrame()

    # check how many patients were added to the df_biopsied :
    pat_added = set()

    # Create a list with all numbers from 0 to 4108:
    random_list = list(np.arange(0, len(pat_normal_set)))

    random.seed(seed)

    # iterate till 100 patients added :
    # for i in range(num_pat_l):
    while len(pat_added) < num_pat_l:
        # sample a number 0 to 4109 :
        # rnd_pat = int(random.sample(random_list, 1))
        rnd = random.sample(random_list, 1)

        # print("random patient sampled:", rnd)

        rnd_pat = int(rnd[0])

        # take the patient ID of the random number:
        rnd_pat_id = pat_normal_list[rnd_pat]
        # print("random patient id:", rnd_pat_id)


        # take all left breast volumes of that patient if exist :
        df_temp = df_normal.loc[(df_normal['PatientID'] == rnd_pat_id) & (df_normal['View'].isin(["lcc", "lmlo", "lcc1", "lmlo1", "lcc2", "lmlo2"]))]

        df_sampled = df_sampled.append(df_temp, ignore_index=True)

        # delete element in order not to be sampled again :
        random_list.remove(rnd_pat)

        # df_temp empty :
        df_temp = pd.DataFrame()

        for pat in range(df_sampled.shape[0]):
            pat_added.add(str(df_sampled.loc[pat]["PatientID"]))

    print("df_sampled length:", len(df_sampled))

    df_biopsied = df_biopsied.append(df_sampled, ignore_index=True)


    print()

    print("pat_added length:", len(pat_added))

    return df_biopsied


def df_add_desc_path(df, csv_paths):

    df_paths = pd.read_csv(csv_paths)

    primary_key = ("PatientID", "StudyUID", "View")
    df_merged = pd.merge(df, df_paths, on=primary_key)

    return df_merged


if __name__ == "__main__":
    # the seed = 42 was chosen arbitrarily :
    df_new_p = csv_processed(csv_views ="/mnt/seagate/DBT/duke-dbt-data_github/data/manifest-1617905855234/BCS-DBT labels-train-v2.csv",
                             seed=42)

    print()
    print("After calling the func:")
    print("df_400 shape:", df_new_p.shape)

    # print()
    # print("df_400 head:")
    # print(df_400.head())
    #
    # print()
    # print("df_400 tail:")
    # print(df_400.tail())

    df_new_p_path = df_add_desc_path(df = df_new_p,
                                     csv_paths = "/mnt/seagate/DBT/duke-dbt-data_github/data/manifest-1617905855234/BCS-DBT file-paths-train-v2.csv")
    # print("df_400_path:")
    # print(df_400_path.head())
    # print(df_400_path.tail())
    print(df_new_p_path.shape)
    # print(df_400_path.columns.tolist())

    # saving the expanded df_biopsied dataframe (with the paths columns) into a csv file:
    df_new_p_path.to_csv("/mnt/seagate/DBT/duke-dbt-data_github/data/manifest-1617905855234/BCS-DBT labels-new-v0.csv", index = False)
