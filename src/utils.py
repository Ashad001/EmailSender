import pandas as pd
import os

def save_data_by_country(input_csv, output_folder='../data/countries'):
    df = pd.read_csv(input_csv)
    os.makedirs(output_folder, exist_ok=True)
    unique_countries = df['Country'].unique()

    for country in unique_countries:
        country_df = df[df['Country'] == country]
        output_file = os.path.join(output_folder, f'{country}_data.csv')
        country_df.to_csv(output_file, index=False)

    print(f'Data saved in separate files in the "{output_folder}" folder.')

# save_data_by_country('../data/emails.csv')
