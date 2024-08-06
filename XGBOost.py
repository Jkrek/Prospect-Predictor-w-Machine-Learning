#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 12:43:07 2024
Updated to include ML model and API endpoint

@author: jkrek
"""

import os
import requests
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from sportsreference.nfl.roster import Player
import joblib

app = Flask(__name__)
CORS(app)

# Function to fetch NFL player data
def fetch_nfl_player_data():
    url = 'https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes?limit=1000&active=true'
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Error fetching data from API. Status code: {response.status_code}")
    
    data = response.json()
    
    players = []
    for player in data['items']:
        player_info = {
            'id': player.get('id'),
            'uid': player.get('uid'),
            'guid': player.get('guid'),
            'type': player.get('type'),
            'fullName': player.get('fullName'),
            'displayName': player.get('displayName'),
            'shortName': player.get('shortName'),
            'headshot': player.get('headshot', {}).get('href'),
            'jersey': player.get('jersey'),
            'position': player.get('position', {}).get('name'),
            'team': player.get('team', {}).get('name')
        }
        players.append(player_info)
    
    return players

# Function to save data to CSV
def save_to_csv(players, filename='nfl_players.csv'):
    df = pd.DataFrame(players)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Function to train the model
def train_model():
    # Load and preprocess data
    df = pd.read_csv('nfl_players.csv')
    df['position'] = df['position'].fillna('Unknown')
    df['team'] = df['team'].fillna('Unknown')

    # Encode categorical variables
    label_encoders = {}
    for column in ['position', 'team']:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        label_encoders[column] = le

    # Prepare features and labels
    features = df.drop(columns=['id', 'uid', 'guid', 'type', 'fullName', 'displayName', 'shortName', 'headshot'])
    labels = df['position']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

    # Train the XGBoost model
    model = xgb.XGBClassifier()
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy}")

    # Save the model and label encoders
    model.save_model('nfl_xgboost_model.json')
    joblib.dump(label_encoders, 'label_encoders.pkl')

# Uncomment to fetch data and train the model
if os.getenv('FETCH_DATA', 'false').lower() == 'true':
    players = fetch_nfl_player_data()
    save_to_csv(players)

if os.getenv('TRAIN_MODEL', 'false').lower() == 'true':
    train_model()

# Load the model and label encoders
model = xgb.XGBClassifier()
model.load_model('nfl_xgboost_model.json')
label_encoders = joblib.load('label_encoders.pkl')

# Function to fetch player data using the sportsreference API
def fetch_player_data(player_name):
    try:
        player = Player(player_name)
        if not player:
            raise ValueError("Player not found")
        player_data = {
            'name': player.name,
            'position': player.position,
            'games_played': player.games,
            'passing_touchdowns': player.passing_touchdowns,
            'passing_yards': player.passing_yards,
            'rushing_touchdowns': player.rushing_touchdowns,
            'rushing_yards': player.rushing_yards,
            # Add other relevant stats here
        }
        return player_data
    except Exception as e:
        print(f"Error fetching data for player {player_name}: {e}")
        return None

# Function to determine success in NFL or no success
def determine_success(player_stats):
    if player_stats['passing_touchdowns'] > 20 and player_stats['passing_yards'] > 3000:
        return 'Success'
    else:
        return 'No Success'

# Flask API endpoint to handle predictions
@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    if request.method == 'OPTIONS':
        response = make_response('', 200)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    data = request.get_json(force=True)
    player_name = data['name']
    player_data = fetch_player_data(player_name)
    
    if player_data:
        # Convert player data to a DataFrame
        player_df = pd.DataFrame([player_data])
    
        # Preprocess the player data (similar to training data)
        for column in ['position']:
            if column in player_df and column in label_encoders:
                player_df[column] = label_encoders[column].transform(player_df[column])
        
        # Drop non-feature columns
        player_features = player_df.drop(columns=['name'])
    
        # Predict success (assuming success is defined as position for demonstration)
        player_prediction = model.predict(player_features)
        player_position = label_encoders['position'].inverse_transform(player_prediction)
        
        player_success = determine_success(player_data)
        return jsonify({
            'predicted_position': player_position[0],
            'success': player_success
        })
    else:
        return jsonify({'error': 'Player not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
