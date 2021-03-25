#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


data = pd.read_excel("MO14-Round-1-Dealing-With-Data-Workbook (1).xlsx", sheet_name="Usage", header=None)
data


# In[3]:


data.info()


# In[4]:


data.isnull().sum()


# In[5]:


data.rename(columns={0:"column1"}, inplace=True)
data.head()


# In[6]:


data.column1 = data.column1.apply(lambda x: x.strip(" _"))
data


# ### KWH

# In[7]:


data["column1"].str.rsplit("_", n=1)


# In[8]:


data["kwh"] = data["column1"].str.rsplit("_", n=1).str[1]
data.head()


# In[9]:


data["kwh"] = data["kwh"].str.rstrip(" kwh ")
data.head()


# In[ ]:





# ### Split date

# In[10]:


data.column1.str.rstrip(" kwh").str.rsplit("_")


# In[11]:


data["date"] = data.column1.str.rstrip(" kwh").str.rsplit("_").str[0]
data.head()


# In[12]:


data = data.drop("column1", axis = 1)
data.head()


# In[ ]:





# ### Day

# In[13]:


data.date.str.rsplit(" ",n= 1)


# In[14]:


data["day"] = data.date.str.rsplit(" ",n= 1).str[1]
data.head()


# In[15]:


data["day"].unique()[:50]


# In[16]:


data["day"] = data["day"].str.replace("th","")
data["day"] = data["day"].str.replace("rd","")
data["day"] = data["day"].str.replace("st","")
data["day"] = data["day"].str.replace("nd","")


# In[17]:


data.head(10)


# In[ ]:





# ### Hour and Weekday

# In[18]:


data.date.str.rsplit(" ",n = 1)


# In[19]:


data["hour_weekday"] = data.date.str.rsplit(" ",n = 1).str[0]
data.head()


# In[20]:


data = data.drop("date", axis = 1)
data.head()


# In[ ]:





# ### Hour

# In[21]:


data["hour_weekday"] = data["hour_weekday"].str.replace(" ","")
data


# In[22]:


data["hour"] = data["hour_weekday"].str[:4]
data


# In[23]:


data["hour"].str.rstrip("MTWFS")


# In[24]:


data["hour"] = data["hour"].str.rstrip("MTWFS") + "M"
data.head()


# In[25]:


data["hour"].unique()


# In[ ]:





# ### Weekday

# In[26]:


data.info()


# In[27]:


data["day"] = data["day"].astype("datetime64")
data.info()


# In[28]:


data["day_name"] = data["day"].dt.day_name()


# In[29]:


data.head()


# In[30]:


data.drop("hour_weekday", axis = 1, inplace = True)
data.head()


# In[ ]:





# In[ ]:





# # Question 1

# In[31]:


data.info()


# In[32]:


data["kwh"] = data["kwh"].astype("float64")
data.info()


# In[33]:


round(data["kwh"].mean(),3)


# In[ ]:





# # Question 2

# In[34]:


data.head()


# In[35]:


data["Month"] = data["day"].dt.month_name()
data.head()


# In[36]:


data.groupby("Month")["kwh"].mean()["February"].round(3)


# In[ ]:





# # Question 3

# In[37]:


data.groupby("day_name")["kwh"].mean().nlargest(1)


# In[ ]:





# In[ ]:





# # Question 4

# In[38]:


data.head()


# In[39]:


data["hour"].str.rstrip("PM")


# In[40]:


data["new_hour"] = data["hour"].str.rstrip("PM").transform(lambda x: x if x.startswith("12")
                                                           else
                                                           int(x) + 12 
                                                           if "A" not in x                                                        
                                                           else x.replace("A", ""))
data 


# In[41]:


data[data["hour"] == "12AM"]


# In[42]:


data[data["hour"] == "12AM"] = data[data["hour"] == "12AM"].transform(lambda x: x.replace("12A", 0))


# In[43]:


data.head(20)


# In[44]:


data["new_hour"] = data["new_hour"].transform(lambda x: str(x) + ":00:00")
data.head(13)


# In[ ]:





# In[45]:


data["new_hour"].nunique()


# In[46]:


data.head()


# In[47]:


data["day"] = data["day"].astype("str")


# In[48]:


def concat(x):
    return str(x["day"]) + " " + str(x["new_hour"])


# In[49]:


data["time"] = data.apply(concat, axis = 1)


# In[50]:


data


# In[51]:


data["time"] = data["time"].astype("datetime64")


# In[52]:


data.head()


# In[53]:


data.resample('4H', on='time').kwh.sum()


# In[54]:


data.resample('4H', on='time').kwh.sum().max()


# In[ ]:





# # Question 5

# In[55]:


data.head()


# In[56]:


data["kwh"].describe().T


# In[57]:


data.groupby("Month")["kwh"].sum()


# In[58]:


cost_data = data.groupby("Month")["kwh"].sum().reset_index()
cost_data


# In[59]:


contract = pd.read_excel("MO14-Round-1-Dealing-With-Data-Workbook (1).xlsx").copy()
contract


# In[60]:


monthly_data = contract.iloc[8:20,4:6]
monthly_data


# In[61]:


monthly_data.rename(columns={"Unnamed: 4" : "Month", "Unnamed: 5" : "Flex"}, inplace = True)
monthly_data


# In[62]:


cost_data.sort_values("Month")


# In[63]:


amount_data = pd.merge(monthly_data, cost_data, on = "Month")
amount_data


# In[64]:


amount_data["cost"] = amount_data["Flex"] * amount_data["kwh"]
amount_data


# In[65]:


round(amount_data["cost"].sum(), 2)


# In[ ]:





# # Question 6

# In[66]:


contract


# In[67]:


no_flex = contract.iloc[8,[0,1]]
no_flex


# In[68]:


no_flex_cost = data["kwh"].sum() * no_flex[1]
round(no_flex_cost, 2)


# In[69]:


monthly_flex_cost = round(amount_data["cost"].sum(), 2)
monthly_flex_cost


# In[ ]:





# In[70]:


hourly_data = contract.iloc[8:32, 8:10]
hourly_data.rename(columns = {"Unnamed: 8" : "hour", "Unnamed: 9" : "flex"}, inplace = True)
hourly_data = hourly_data.reset_index(drop = True)
hourly_data


# In[71]:


data.head()


# In[72]:


data["new_hour2"] = data["new_hour"].astype("datetime64")
data


# In[73]:


hourly_cost = data.resample("H", on = "new_hour2")["kwh"].sum()
hourly_cost = hourly_cost.reset_index()
hourly_cost.rename(columns = {"new_hour2" : "hours"}, inplace=True)
hourly_cost


# In[74]:


hourly_cost["hours"] = hourly_cost["hours"].astype("object")


# In[75]:


hourly_flex_cost = pd.concat([hourly_data, hourly_cost], axis = 1)
hourly_flex_cost


# In[76]:


hourly_flex_cost["cost"] = hourly_flex_cost["flex"] * hourly_flex_cost["kwh"]
hourly_flex_cost


# In[77]:


round(hourly_flex_cost["cost"].sum(), 2)


# In[ ]:





# ### no_flex_cost = 1438.34
# ### monthly_flex_cost = 1421.82
# ### hourly_flex_cost = 1369.36
# 
# 
# ## "Hourly Contract" is the lowest cost

# In[ ]:





# In[ ]:




