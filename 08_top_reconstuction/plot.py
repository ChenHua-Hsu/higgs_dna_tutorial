import pandas as pd
import awkward as ak
import numpy

df = pd.read_parquet(f'/eos/user/c/chenhua/higgsdna_finalfits_tutorial_24/08_top_reconstuction/NTuples/tth_M-125_preEE/nominal/d5487028-9b3b-11ee-a54d-168ed380beef_%2FEvents%3B1_0-174835.parquet')
pd.set_option('display.max_columns', None)
file = f'/eos/user/c/chenhua/higgsdna_finalfits_tutorial_24/08_top_reconstuction/NTuples_lepton1_phi0.75/tth_M-125_preEE/nominal/d5487028-9b3b-11ee-a54d-168ed380beef_%2FEvents%3B1_0-174835.parquet'
output = ak.from_parquet(file)
print(output.fields)
# Print the column names
# print(df.columns)

# import matplotlib.pyplot as plt
#import awkward as ak

# Assuming your array is called 'arr'
if 'top_mass' in output.fields:
    print("The array contains 'top_mass'.")
else:
    print("'top_mass' is not found in the array.")

# # Assuming 'top_mass' is the column name
# plt.hist(df['diphotons']['hadronic_top_mass'], bins=50, edgecolor='black')
# plt.xlabel('Top Mass (GeV)')
# plt.ylabel('Frequency')
# plt.title('Top Mass Distribution')
# plt.savefig("top_mass_distribution.png")

import matplotlib.pyplot as plt

# Extract 'top_mass' from the awkward array
top_mass = output['w_mass']

# Convert the awkward array to a numpy array for plotting
top_mass_np = ak.to_numpy(top_mass)

# Plot the 'top_mass' data
bin = numpy.linspace(0, 300, 200)
plt.hist(top_mass_np, bins=bin, edgecolor='black')
plt.xlabel('W Mass (GeV)')
plt.ylabel('Frequency')
plt.xlim(0,300)
#plt.ylim(0,5000)
plt.title('W Mass Distribution(n_lepton=1 delta_phi<0.75)')
plt.savefig('W_mass_distribution4.png')
