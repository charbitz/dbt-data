
# Initial csv files: 
#     * BCS-DBT boxes-train-v2.csv  : containing the bounding boxes ground truth ...for 224 bounding boxes...
#     * BCS-DBT labels-train-v2.csv : containing the labels ground truth ...for 19148 volumes...

# Some details about 224 in Biopsied cases:
# 224 are the number of bounding boxes in Biopsied cases,
# But the number of volumes in the Biopsied cases is 200

# New csv files for use: 
#     * BCS-DBT boxes-train-v2.csv  : containing the bounding boxes ground truth ...for 224 bounding boxes (=200 volumes)...(same as previously)
#     * BCS-DBT labels-new-v0.csv          : containing the labels ground truth ...


# New target:
# Now we should append one more information to the file's "BCS-DBT labels-new-v0.csv" dataframe.
# This is the columns "descriptive_path" (or "classic_path") from the "BCS-DBT file-paths-train-v2.csv" file.


import numpy as np
import pandas as pd
import random


def csv_processed(csv_views, r_seed):

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

    # gather all unique patients from Normal group to a set:
    pat_normal_set = set()
    for pat in range(df_normal.shape[0]):
        pat_normal_set.add(str(df_normal.loc[pat]["PatientID"]))

    print("Normal group, unique patients :", len(pat_normal_set))
    print()

    print("Biopsied group, unique patients :", len(pat_normal_set))
    print()

    # Sample patients with left views :
    # random.seed(r_seed)
    print("Sampling patients with left views:")
    df_sampled_left, pat_left_added = patients_sample(df_normal,
                                                      pat_normal_set,
                                                      num_pat_l,
                                                      target_values = ["lcc", "lmlo", "lcc1", "lmlo1", "lcc2", "lmlo2"],
                                                      r_seed= r_seed)

    df_biopsied = df_biopsied.append(df_sampled_left, ignore_index=True)

    # update the patients in order not to be sampled again with right views:
    pat_normal_no_left = pat_normal_set.difference(pat_left_added)
    for pat in range(df_normal.shape[0]):
        pat_normal_set.add(str(df_normal.loc[pat]["PatientID"]))

    # Sample patients with right views :
    # random.seed(r_seed+10)
    print("Sampling patients with right views:")
    df_sampled_right, pat_right_added = patients_sample(df_normal,
                                                        pat_normal_no_left,
                                                        num_pat_r,
                                                        target_values=["rcc", "rmlo", "rcc1", "rmlo1", "rcc2", "rmlo2"],
                                                        r_seed= r_seed)

    print("Total number of patients sampled:", len(pat_left_added)+len(pat_right_added))
    print("Total number of volumes sampled:", len(df_sampled_left) + len(df_sampled_right))
    print()

    # check if the two sets have common patients:
    have_not_common = pat_left_added.isdisjoint(pat_right_added)
    print("The two sets have not common patients:", have_not_common)

    df_biopsied = df_biopsied.append(df_sampled_right, ignore_index=True)

    print()

    return df_biopsied



def patients_sample(df_normal, pat_normal_set, num_patients, target_values, r_seed):

    # keep different seed between two view cases:
    if target_values == ["lcc", "lmlo", "lcc1", "lmlo1", "lcc2", "lmlo2"]:
        r_seed = r_seed
    else:
        r_seed = r_seed + 10

    # copy all unique patients to a list:
    pat_normal_list = list(pat_normal_set)

    # create an empty dataframe, where the new patients will be added :
    df_sampled = pd.DataFrame()

    # check how many patients were added to the df_biopsied :
    pat_added = set()

    # Create a list with all numbers from 0 to 4108:
    random_list = list(np.arange(0, len(pat_normal_set)))

    # random.seed(r_seed)

    # iterate till 100 patients added :
    # for i in range(num_pat_l):
    while len(pat_added) < num_patients:
        # sample a number 0 to 4109 :
        # rnd_pat = int(random.sample(random_list, 1))

        random.seed(r_seed)
        # np.random.seed(r_seed)
        rnd = random.sample(random_list, 1)

        # print("random patient sampled:", rnd)

        rnd_pat = int(rnd[0])

        # take the patient ID of the random number:
        rnd_pat_id = pat_normal_list[rnd_pat]

        # take all views of that patient if exist :
        df_temp = df_normal.loc[(df_normal['PatientID'] == rnd_pat_id) & (df_normal['View'].isin(target_values))]

        df_sampled = df_sampled.append(df_temp, ignore_index=True)

        # delete element in order not to be sampled again :
        random_list.remove(rnd_pat)

        # df_temp empty :
        df_temp = pd.DataFrame()

        for pat in range(df_sampled.shape[0]):
            pat_added.add(str(df_sampled.loc[pat]["PatientID"]))

    print("Sampled patients:", len(pat_added))
    print("Sampled volumes:", len(df_sampled))
    print()

    return df_sampled, pat_added


def df_add_desc_path(df, csv_paths):

    df_paths = pd.read_csv(csv_paths)

    primary_key = ("PatientID", "StudyUID", "View")
    df_merged = pd.merge(df, df_paths, on=primary_key)

    return df_merged


if __name__ == "__main__":
    # the seed = 42 was chosen arbitrarily :
    df_new_p = csv_processed(csv_views ="/mnt/seagate/DBT/duke-dbt-data_github/data/manifest-1617905855234/BCS-DBT labels-train-v2.csv",
                             r_seed=42)

    print("Dataframe shape after extension:", df_new_p.shape)

    df_new_p_path = df_add_desc_path(df = df_new_p,
                                     csv_paths = "/mnt/seagate/DBT/duke-dbt-data_github/data/manifest-1617905855234/BCS-DBT file-paths-train-v2.csv")
    print("Dataframe shape after appending paths:", df_new_p_path.shape)

    # saving the expanded df_biopsied dataframe (with the paths columns) into a csv file:
    df_new_p_path.to_csv("/mnt/seagate/DBT/duke-dbt-data_github/data/manifest-1617905855234/BCS-DBT labels-new-v0.csv", index = False)
