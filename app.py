from flask import Flask, request, jsonify
import pandas as pd
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Converting values to correct Mobile number format
def convert_to_int(phone):
    type_val = type(phone)
    if type_val == str:
        numeric_part = ''.join(char for char in phone if char.isdigit())
        return int(numeric_part[-9:])
    elif type_val == float:
        return int(str(int(phone))[-9:])
    else:
        return int(phone)

curr_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(curr_dir, 'card_status.db')

# File names to read data from
pickup_file = 'Sample Card Status Info - Pickup.csv'
exceptions_file = 'Sample Card Status Info - Delivery exceptions.csv'
delivered_file = 'Sample Card Status Info - Delivered.csv'
returned_file = 'Sample Card Status Info - Returned.csv'

# Creating DataFrames from csv files
pickup_df = pd.read_csv(os.path.join(curr_dir, 'data', pickup_file))
exceptions_df = pd.read_csv(os.path.join(curr_dir, 'data', exceptions_file))
delivered_df = pd.read_csv(os.path.join(curr_dir, 'data', delivered_file)) 
returned_df = pd.read_csv(os.path.join(curr_dir, 'data', returned_file))

# Renaming inconsistent Column names of Phone Numbers to "User Mobile" for easier processing
for df in [pickup_df, exceptions_df, delivered_df, returned_df]:
    if 'User contact' in df.columns:
        df.rename(columns={'User contact': 'User Mobile'}, inplace=True)

# Converting Mobile numbers to valid format
pickup_df['User Mobile'] = pickup_df['User Mobile'].apply(convert_to_int)
exceptions_df['User Mobile'] = exceptions_df['User Mobile'].apply(convert_to_int)
delivered_df['User Mobile'] = delivered_df['User Mobile'].apply(convert_to_int)
returned_df['User Mobile'] = returned_df['User Mobile'].apply(convert_to_int)

# Adding Status Column to return Card status
pickup_df['Status'] = 'Card is picked up by Courier Partner'
exceptions_df['Status'] = 'Card could not be delivered'
delivered_df['Status'] = 'Card Delivered Successfully'
returned_df['Status'] = 'Card is Returned'

# Converting 12 Hour time to 24 Hour time in returned database
returned_df['Timestamp'] =  pd.to_datetime(returned_df['Timestamp']).dt.strftime('%d-%m-%Y %H:%M')
# Convert ISO 8601 time to a datetime object in delivered database
delivered_df['Timestamp'] = delivered_df['Timestamp'].apply(lambda x: datetime.fromisoformat(x[:-1]).strftime('%d-%m-%Y %H:%M'))

# Setting Default comments for pickup, exceptions, delivered, returned
if 'Comment' not in pickup_df.columns:
    pickup_df['Comment'] = 'PICKUP'
if 'Comment' not in exceptions_df.columns:
    exceptions_df['Comment'] = 'EXCEPTION'
if 'Comment' not in delivered_df.columns:
    delivered_df['Comment'] = 'DELIVERED'
if 'Comment' not in returned_df.columns:
    returned_df['Comment'] = 'RETURNED'

# Creating Database with SQL queries into different Tables
with sqlite3.connect(db_path) as conn:
    pickup_df.to_sql('pickup', conn, index=False, if_exists='replace', method='multi')
    exceptions_df.to_sql('exceptions', conn, index=False, if_exists='replace', method='multi')
    delivered_df.to_sql('delivered', conn, index=False, if_exists='replace', method='multi')
    returned_df.to_sql('returned', conn, index=False, if_exists='replace', method='multi')

@app.route('/get_card_status', methods=['GET'])
def get_card_status():
    with sqlite3.connect(db_path) as conn:
        card_id = request.args.get('card_id')
        user_mobile = request.args.get('user_mobile')

        #Using SQL command to retirve all the records and then get the latest record
        if card_id:
            query = f"SELECT * FROM (SELECT * FROM pickup WHERE `Card ID` = '{card_id}' UNION SELECT * FROM exceptions WHERE `Card ID` = '{card_id}' UNION SELECT * FROM delivered WHERE `Card ID` = '{card_id}' UNION SELECT * FROM returned WHERE `Card ID` = '{card_id}') ORDER BY Timestamp DESC LIMIT 1"
        elif user_mobile:
            query = f"SELECT * FROM (SELECT * FROM pickup WHERE `User Mobile` = '{user_mobile}' UNION SELECT * FROM exceptions WHERE `User Mobile` = '{user_mobile}' UNION SELECT * FROM delivered WHERE `User Mobile` = '{user_mobile}' UNION SELECT * FROM returned WHERE `User Mobile` = '{user_mobile}') ORDER BY Timestamp DESC LIMIT 1"
        else:
            return jsonify({'status': 'Error, Please check Card ID or Mobile number', 'message': 'Card Details not found'})

        df = pd.read_sql(query, conn)

        if not df.empty:
            latest_result = df.iloc[0].to_dict()
            status_info = {
                'Status': latest_result.get('Status', ''),
                'Comment': latest_result.get('Comment', ''),
                'timestamp': latest_result['Timestamp'],
                'Card ID': latest_result['Card ID'],
                'Mobile': latest_result['User Mobile']
            }
            return jsonify(status_info)

    return jsonify({'status': 'Error, Please check Card ID or Mobile number', 'message': 'Card Details not found'})

# To print Database
@app.route('/print_db', methods=['GET'])
def print_database():
    with sqlite3.connect(db_path) as conn:
        result = {}
        for table_name in ['pickup', 'exceptions', 'delivered', 'returned']:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, conn)
            result[table_name] = df.to_dict(orient='records')

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
