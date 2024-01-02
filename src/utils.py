import pandas as pd
import random
import os
import json

def save_data_by_country(input_csv, output_folder='../data/countries'):
    df = pd.read_csv(input_csv)
    os.makedirs(output_folder, exist_ok=True)
    unique_countries = df['Country'].unique()

    for country in unique_countries:
        country_df = df[df['Country'] == country]
        output_file = os.path.join(output_folder, f'{country}_data.csv')
        country_df.to_csv(output_file, index=False)

    print(f'Data saved in separate files in the "{output_folder}" folder.')

def generate_email_sending_plan(days, initial_emails, increment_range, max_emails_per_day):
    plan = {}
    current_emails = initial_emails

    for day in range(1, days + 1):
        max_inc = random.randint(increment_range[0], increment_range[1])
        emails_to_send = {
            "min": current_emails,
            "max": current_emails + max_inc
        }

        plan[day] = {"emails": emails_to_send}
        current_emails += increment_range[0]

    return {"email_sending_plan": plan}

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    total_days = 25
    initial_emails_to_send = 1
    increment_range = (1, 3)
    max_emails_per_day = 25
    output_filename = "../email_sending_plan.json"

    email_plan = generate_email_sending_plan(total_days, initial_emails_to_send, increment_range, max_emails_per_day)
    save_to_json(email_plan, output_filename)

    print(f"Email sending plan generated and saved to {output_filename}")

