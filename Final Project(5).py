#!/usr/bin/env python
# coding: utf-8

# In[29]:


import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

alcSales = pd.read_csv('alc_sales.csv', header = 0)

alcSales.head()


# In[30]:


StateCodes = {
                2:'Alaska',
                5:'Arkansas',
                8:'Colorado',
                9:'Connecticut',
                12:'Florida',
                17:'Illinois',
                20:'Kansas',
                21:'Kentucky',
                22:'Louisiana',
                25:'Massachusetts',
                29:'Missouri',
                38:'North Dakota',
                41:'Oregon',
                47:'Tennessee',
                48:'Texas',
                51:'Virginia',
                55:'Wisconsin'
}

alcSales["State"] = alcSales["FIPS"].replace(StateCodes)

alcSales = alcSales.drop(['FIPS'], axis = 1)

alcSales.head()


# In[31]:


alcSales.to_csv('Alc_Sales_States.csv')


# In[32]:


df_state = alcSales.groupby(by=['Year', 'Month', 'State'], as_index=False).sum()[['Year', 'Month', 'State', 'Gallons', 'Ethanol', 'PerCapita']]

dfStateNormal = df_state[df_state['Year'] < 2020][df_state['Month'] <= 7]
dfStateLockdown = df_state[df_state['Year'] == 2020]


# In[33]:


def state_norm(state):
    x = dfStateNormal[dfStateNormal['State'] == state]
    return x

def state_lockdown(state):
    x = dfStateLockdown[dfStateLockdown['State'] == state]
    return x


# In[34]:


StateNames = list(alcSales.State.unique())

normalStateDFs = [pd.DataFrame() for i in range(len(StateNames))]

lockdownStateDFs = [pd.DataFrame() for i in range(len(StateNames))]


# In[35]:


for i in range(len(StateNames)):
    normalStateDFs[i] = state_norm(StateNames[i])
    
normalStateDict = dict(zip(StateNames, normalStateDFs))

for i in range(len(StateNames)):
    lockdownStateDFs[i] = state_lockdown(StateNames[i])

lockdownStateDict = dict(zip(StateNames, lockdownStateDFs))


# In[36]:


normalStateDict['North Dakota'].head(10)


# In[37]:


lockdownStateDict['Massachusetts'].head()


# In[46]:


df_bev = alcSales.groupby(by=['Year', 'Month', 'Beverage'], as_index=False).sum().drop(labels=['PerCapita', 'PerCapita3yr', 'PctChange'], axis=1)

df_bev['PerCapita'] = df_bev['Ethanol']/df_bev['Population']

dfBevNormal = df_bev[df_bev['Year'] < 2020][df_bev['Month'] <= 7]
dfBevLockdown = df_bev[df_bev['Year'] == 2020]

def bev_norm(bev):
    x = dfBevNormal[dfBevNormal['Beverage'] == bev]
    return x

def bev_lockdown(bev):
    x = dfBevLockdown[dfBevLockdown['Beverage'] == bev]
    return x


# In[47]:


normalBevDFs = [pd.DataFrame() for i in range(3)]

lockdownBevDFs = [pd.DataFrame() for i in range(3)]


# In[48]:


for i in range(3):
    normalBevDFs[i] = bev_norm(i+1)
    
normalBevDict = dict(zip(['Spirits', 'Wine', 'Beer'], normalBevDFs))

for i in range(3):
    lockdownBevDFs[i] = bev_lockdown(i+1)
    
lockdownBevDict = dict(zip(['Spirits', 'Wine', 'Beer'], lockdownBevDFs))


# In[49]:


normalBevDict['Beer'].head()


# In[50]:


lockdownBevDict['Wine'].head()


# In[51]:



chosenState = st.sidebar.selectbox('State to include:', StateNames )
min_year, max_year = st.sidebar.slider('Years to include:', 2017, 2020,( 2017, 2020 ), step = 1 )
years = range( min_year, max_year + 1 )


#stateDf = df_state.loc[df_state['State'] == chosenState and df_state['Year'] in years]
stateDf= df_state[df_state['State'] == chosenState][df_state['Year'] in years]

fig, ax = plt.subplots()

st.title( 'Ethanol Sales Per Capita' )
stateDf.groupby('Year').plot('Month','PerCapita', legend='upper left', ax=ax )
plt.gcf().set_size_inches(8,10)
plt.title( f'Ethanol Per Capita for {chosenState}', fontsize=20 )
plt.xticks( range(1,13) )
plt.ylabel( 'Ethanol Sales in Gallons Per Capita', fontsize=14 )
plt.xlabel(None)
st.pyplot(fig)

"""
#change this to change the charted state
chosenState = 'Alaska'

stateDf = df_state.loc[df_state['State'] == chosenState]

fig, ax = plt.subplots()

stateDf.groupby('Year').plot('Month','PerCapita', legend='upper left', ax=ax )
plt.gcf().set_size_inches(8,10)
plt.title( f'Ethanol Per Capita for {chosenState}', fontsize=20 )
#plt.xticks( df_pcts.index, rotation=90 )
plt.ylabel( 'Ethanol Sales in Gallons Per Capita', fontsize=14 )
plt.xlabel(None)
plt.show()
"""


# In[56]:




chosenBev = st.sidebar.selectbox('State to include:', range(1,4) )
chosenBevDf = df_bev.loc[df_bev['Beverage'] == chosenBev]

fig, ax = plt.subplots()

chosenBevDf.groupby('Year').plot('Month','PerCapita', legend='upper left', ax=ax )
plt.gcf().set_size_inches(8,10)
plt.title( f'Ethanol Per Capita for Beverage {chosenBev}', fontsize=20 )
plt.xticks( range(1,13) )
plt.ylabel( 'Ethanol Sales in Gallons Per Capita', fontsize=14 )
plt.xlabel(None)
st.pyplot(fig)


"""
#change this to change the charted Beverage

chosenBev = 1

chosenBevDf = df_bev.loc[df_bev['Beverage'] == chosenBev]

fig, ax = plt.subplots()
chosenBevDf.groupby('Year').plot('Month','PerCapita', legend='upper left', ax=ax )
plt.gcf().set_size_inches(8,10)
plt.title( f'Ethanol Per Capita for Beverage {chosenBev}', fontsize=20 )
#plt.xticks( df_pcts.index, rotation=90 )
plt.ylabel( 'Ethanol Sales in Gallons Per Capita', fontsize=14 )
plt.xlabel(None)
plt.show()
"""


# In[ ]:




