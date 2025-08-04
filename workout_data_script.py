#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from datetime import datetime

raw_data = pd.read_csv('daily_strength2.csv')
df = raw_data.copy()


# In[5]:


df = df.drop(['Notes'], axis=1) #No notes are present

#Will keep distance and duration in case cardio gets logged in future; all entries are currently null


# In[9]:


#Quite certain this is a warm-up set with an unloaded bar, so will change to 0

df['Weight'] = df['Weight'].fillna(0)


# In[17]:


df['Date'] = pd.to_datetime(df['Date'], format = '%Y-%m-%d %H:%M:%S').dt.date


# In[22]:


cutoff_date = pd.Timestamp('2025-03-01').date()
df = df[df['Date'] >= cutoff_date]


# In[25]:


df = df.reset_index()


# In[27]:


df.rename(columns={'index': 'ID'}, inplace=True)


# In[32]:


exercises = pd.DataFrame(columns=['exercise_id', 'exercise_name', 'primary_muscle'])
muscles = pd.DataFrame(columns=['muscle_id', 'muscle_name', 'muscle_group'])
secondary_muscles = pd.DataFrame(columns=['exercise_id', 'muscle_id'])


# In[34]:


ex = exercises.copy()


# In[36]:


exercise_list = df['Exercise'].unique()


# In[37]:


ex['exercise_name'] = exercise_list


# In[39]:


mu = muscles.copy()


# In[40]:


muscle_names = ['chest', 'shoulders', 'traps', 'lats', 'middle back', 'lower back', 'biceps', 'triceps', 'forearms', 'abs',\
                'quadriceps', 'hamstrings', 'glutes', 'abductors', 'adductors', 'calves', 'cardio']


# In[41]:


mu['muscle_name'] = muscle_names


# In[43]:


muscle_groups = {'chest':'chest', 'shoulders':'shoulders', 'traps':'shoulders', 'lats':'back', 'middle back':'back', 'lower back':'back',\
                 'biceps':'arms', 'triceps':'arms', 'forearms':'arms', 'abs':'abs', 'quadriceps':'legs', 'hamstrings':'legs', 'glutes':'legs',\
                 'abductors':'thighs', 'adductors':'thighs', 'calves':'legs', 'cardio':'cardio'}


# In[44]:


mu['muscle_group'] = mu['muscle_name'].map(muscle_groups)


# In[46]:


mu['muscle_id'] = range(1, len(mu) + 1)


# In[48]:


ex['exercise_id'] = range(1, len(ex) + 1)


# In[50]:


ex['exercise_name'].unique()


# In[51]:


primary_muscle_dict = {'One Arm Dumbbell Row':'Middle Back', 'Wide Grip Lat Pull Down':'Lats',
       'Seated Cable Rows':'Middle Back', 'Alternating Dumbbell Hammer Curls':'Biceps',
       'Dumbbell Concentration Curl':'Biceps', 'Barbell Bench Press':'Chest',
       'Incline Barbell Bench Press':'Chest', 'Chest Press Machine':'Chest',
       'Incline Dumbbell Fly':'Chest', 'Butterfly Machine':'Chest',
       'Lying Dumbbell Triceps Extension':'Triceps',
       'Seated Dumbbell Triceps Extension':'Triceps', 'Cable Triceps Pushdown':'Triceps',
       'Barbell Squat':'Quadriceps', 'Leg Press':'Quadriceps', 'Leg Extensions':'Quadriceps',
       'Stiff Legged Barbell Deadlift':'Hamstrings', 'Seated Leg Curl':'Hamstrings',
       'Seated Calf Raise Machine':'Calves', 'Arnold Press':'Shoulders',
       'Lateral Dumbbell Raises':'Shoulders', 'Seated Shoulder Press Machine':'Shoulders',
       'Dumbbell Upright Row':'Traps', 'Dumbbell Shrugs':'Traps', 'Barbell Deadlifts':'Hamstrings',
       'Preacher Curl Machine':'Biceps', 'Seated Dumbbell Bicep Curls':'Biceps',
       'Incline Dumbbell Bench Press':'Chest', 'Dumbbell Bench Press':'Chest',
       'Dumbbell Lunges':'Quadriceps', 'Dumbbell Hammer Curls':'Biceps'}


# In[53]:


ex['primary_muscle'] = ex['exercise_name'].map(primary_muscle_dict)


# In[59]:


secondary_muscles_dict = {
    'One Arm Dumbbell Row': ["Biceps", 'Traps', 'Lats'],
    'Wide Grip Lat Pull Down': ['Biceps', 'Traps', 'Middle Back'],
    'Seated Cable Rows': ["Biceps", 'Traps', 'Lats'],
    'Alternating Dumbbell Hammer Curls': ['Forearms'],
    'Barbell Bench Press': ['Shoulders', 'Triceps'],
    'Incline Barbell Bench Press': ['Shoulders', 'Triceps'],
    'Chest Press Machine': ['Shoulders', 'Triceps'],
    'Incline Dumbbell Fly': ['Shoulders', 'Triceps'],
    'Barbell Squat': ['Hamstrings', 'Calves', 'Glutes'],
    'Leg Press': ['Hamstrings', 'Calves', 'Glutes'],
    'Stiff Legged Barbell Deadlift': ['Lower Back', 'Quadriceps', 'Glutes'],
    'Arnold Press': ['Triceps'],
    'Seated Shoulder Press Machine': ['Triceps'],
    'Dumbbell Upright Row': ['Shoulders'],
    'Barbell Deadlifts': ['Lower Back', 'Quadriceps', 'Glutes', 'Calves'],
    'Incline Dumbbell Bench Press': ['Shoulders', 'Triceps'],
    'Dumbbell Bench Press': ['Shoulders', 'Triceps'],
    'Dumbbell Lunges': ['Hamstrings', 'Calves', 'Glutes'],
    'Dumbbell Hammer Curls': ['Forearms']
}


# In[61]:


sec = secondary_muscles.copy()


# In[63]:


rows = []

for ex_name, muscle_list in secondary_muscles_dict.items():
    # Try to find the exercise_id from the ex DataFrame
    ex_match = ex[ex['exercise_name'] == ex_name]

    if ex_match.empty:
        print(f"⚠️ Exercise not found: {ex_name}")
        continue

    ex_id = ex_match.iloc[0]['exercise_id']

    for muscle_name in muscle_list:
        # Try to find the muscle_id from the mu DataFrame
        mu_match = mu[mu['muscle_name'].str.lower() == muscle_name.lower()]

        if mu_match.empty:
            print(f"⚠️ Muscle not found: {muscle_name}")
            continue

        mu_id = mu_match.iloc[0]['muscle_id']

        # Append the link to the list
        rows.append({'exercise_id': ex_id, 'muscle_id': mu_id})

# Create the sec DataFrame
sec = pd.DataFrame(rows)


# In[65]:


mu_fin = mu.copy()
ex_fin = ex.copy()
sec_fin = sec.copy()


# In[70]:


df['set_index'] = (df['Set'] == 1).cumsum()


# In[73]:


columns = ['ID', 'Date', 'Workout name', 'Exercise', 'set_index', 'Set', 'Weight', 'Reps',
       'Distance', 'Duration', 'Measurement unit']


# In[74]:


df = df[columns]


# In[76]:


df.rename(columns={'ID': 'log_ID'}, inplace=True)


# In[80]:


ex['primary_muscle'] = ex['primary_muscle'].str.strip().str.lower()


# In[81]:


ex = ex.merge(                          # ex = ex merged as below with mu
    mu[['muscle_name', 'muscle_id']],   #This uses only the necessary columns from muscles
    left_on='primary_muscle',               
    right_on='muscle_name',                 # From the muscle table
    how='left'                              # Keep all rows from exercises
)


# In[83]:


ex = ex.drop(['primary_muscle','muscle_name'], axis=1)


# In[89]:


exercise_map = ex.set_index('exercise_name')['exercise_id'].to_dict()


# In[90]:


df['exercise_id'] = df['Exercise'].map(exercise_map)


# In[92]:


df = df.drop('Exercise', axis =1)


# In[94]:


columns_order = ['log_ID', 'Date', 'Workout name', 'exercise_id', 'set_index', 'Set', 'Weight', 'Reps',
       'Distance', 'Duration', 'Measurement unit']


# In[95]:


df = df[columns_order]


# In[99]:


df_fin = df.copy()
mu_fin = mu.copy()
ex_fin = ex.copy()
sec_fin = sec.copy()


# In[101]:


df_fin.to_csv('main_0725.csv', index=False)
mu_fin.to_csv('muscles_0725.csv', index=False)
ex_fin.to_csv('exercises_0725.csv', index=False)
sec_fin.to_csv('secondary_muscles_0725.csv', index=False)

