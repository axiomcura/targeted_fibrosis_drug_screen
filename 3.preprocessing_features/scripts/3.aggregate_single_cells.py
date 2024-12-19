#!/usr/bin/env python
# coding: utf-8

# ## Aggregating single cells
# In this notebook, we process single-cell feature-selected profiles to generate compound-level aggregated profiled for each plate using the pycytominer. The single-cell profiles are grouped by treatment (Metadata_treatment) and are saved as Parquet files in the aggregated_profiles directory. These aggregated profiles provide concise and interpretable data for downstream analysis at the compound level.

# In[1]:


import pathlib

import pandas as pd
from pycytominer import aggregate

# In[2]:


# parameters
sc_fs_tag = "sc_feature_selected"
agg_tag = "aggregated"

# setting up paths
data_dir = pathlib.Path("./data").resolve(strict=True)
sc_data_dir = pathlib.Path(
    "../3.preprocessing_features/data/single_cell_profiles/"
).resolve(strict=True)
metadata_dir = pathlib.Path("../metadata/updated_platemaps").resolve(strict=True)

# setting metadata paths
updated_barcode_path = (metadata_dir / "updated_barcode_platemap.csv").resolve(
    strict=True
)
all_profiles_paths = list(sc_data_dir.glob("*sc_feature_selected.parquet"))

# output files paths
aggregated_dir_path = (data_dir / "aggregated_profiles").resolve()
aggregated_dir_path.mkdir(exist_ok=True)


# Next, we use the aggregation functionality provided by pycytominer to consolidate single-cell profiles into compound-level summaries for each plate. This step groups the data by a specified metadata column (e.g., Metadata_treatment) and computes aggregate statistics by using the median.

# In[3]:


# Iterate over all profile file paths to process and aggregate data
for plate_path in all_profiles_paths:
    # Extract the plate name from the file stem
    plate_name = plate_path.stem.split("_", 1)[0]

    # Load the single-cell profile data from the current Parquet file into a DataFrame
    profile_df = pd.read_parquet(plate_path)

    # Apply the aggregation function using pycytominer
    # This step groups the single-cell data by the 'Metadata_treatment' column
    # and computes aggregate statistics to summarize profiles at the compound level
    agg_df = aggregate(profile_df, strata=["Metadata_treatment"])

    # Save the aggregated data to the output directory as a Parquet file
    agg_df.to_parquet(aggregated_dir_path / f"{plate_name}_{agg_tag}.parquet")
