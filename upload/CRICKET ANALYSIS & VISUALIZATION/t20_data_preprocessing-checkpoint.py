#!/usr/bin/env python
# coding: utf-8

# <h1 align="center"> T20 World Cup Cricket Data Pre Processing </h1>

# In[1]:


#import necessary libraries
import pandas as pd
import json


# <h4 style="color:blue">(1) Process Match Results</h4>

# In[2]:


with open('t20_json_files/t20_wc_match_results.json') as f:
    data = json.load(f)

df_match = pd.DataFrame(data[0]['matchSummary'])
df_match.head()


# In[ ]:


df_match.shape


# **Use scorecard as a match id to link with other tables**

# In[ ]:


df_match.rename({'scorecard': 'match_id'}, axis = 1, inplace = True)
df_match.head()


# **Create a match ids dictionary that maps team names to a unique match id. This will be useful later on to link with other tables**

# In[ ]:


match_ids_dict = {}

for index, row in df_match.iterrows():
    key1 = row['team1'] + ' Vs ' + row['team2']
    key2 = row['team2'] + ' Vs ' + row['team1']
    match_ids_dict[key1] = row['match_id']
    match_ids_dict[key2] = row['match_id']


# In[ ]:


df_match.to_csv('t20_csv_files/dim_match_summary.csv', index = False)


# <h4 style="color:blue">(2) Process Batting Summary</h4>

# In[ ]:


with open('t20_json_files/t20_wc_batting_summary.json') as f:
    data = json.load(f)
    all_records = []
    for rec in data:
        all_records.extend(rec['battingSummary'])

df_batting = pd.DataFrame(all_records)
df_batting.head(11)


# In[ ]:


df_batting['out/not_out'] = df_batting.dismissal.apply(lambda x: "out" if len(x)>0 else "not_out")
df_batting.head(11)


# In[ ]:


df_batting['match_id'] = df_batting['match'].map(match_ids_dict)
df_batting.head()


# In[ ]:


df_batting.drop(columns=["dismissal"], inplace=True)
df_batting.head(10)


# **Cleanup weird characters**

# In[ ]:


df_batting['batsmanName'] = df_batting['batsmanName'].apply(lambda x: x.replace('â€', ''))
df_batting['batsmanName'] = df_batting['batsmanName'].apply(lambda x: x.replace('\xa0', ''))
df_batting.head()


# In[ ]:


df_batting.shape


# In[ ]:


df_batting.to_csv('t20_csv_files/fact_bating_summary.csv', index = False)


# <h4 style="color:blue">(3) Process Bowling Summary</h4>

# In[ ]:


with open('t20_json_files/t20_wc_bowling_summary.json') as f:
    data = json.load(f)
    all_records = []
    for rec in data:
        all_records.extend(rec['bowlingSummary'])
all_records[:2]


# In[ ]:


df_bowling = pd.DataFrame(all_records)
print(df_bowling.shape)
df_bowling.head()


# In[ ]:


df_bowling['match_id'] = df_bowling['match'].map(match_ids_dict)
df_bowling.head()


# In[ ]:


df_bowling.to_csv('t20_csv_files/fact_bowling_summary.csv', index = False)


# <h4 style="color:blue">(4) Process Players Information</h4>

# In[ ]:


with open('t20_json_files/t20_wc_player_info.json') as f:
    data = json.load(f)


# In[ ]:


df_players = pd.DataFrame(data)

print(df_players.shape)
df_players.head(10)


# **Cleanup weird characters**

# In[ ]:


df_players['name'] = df_players['name'].apply(lambda x: x.replace('â€', ''))
df_players['name'] = df_players['name'].apply(lambda x: x.replace('†', ''))
df_players['name'] = df_players['name'].apply(lambda x: x.replace('\xa0', ''))
df_players.head(10)


# In[ ]:


df_players[df_players['team'] == 'India']


# In[ ]:


df_players.to_csv('t20_csv_files/dim_players_no_images.csv', index = False)

