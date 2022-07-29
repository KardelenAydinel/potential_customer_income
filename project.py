import pandas as pd
df = pd.read_csv('persona.csv')
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
df['SOURCE'].nunique()
df['SOURCE'].value_counts()
df['PRICE'].nunique()

def output_groupby(column, sorted_by, action):
    return df.groupby(column).agg({sorted_by: action})


agg_df =df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE" : "mean"}).sort_values("PRICE", ascending=False)
agg_df = agg_df.reset_index()
agg_df["AGE_CAT"] = pd.cut(x = agg_df["AGE"], bins =[0,18,23,30,40,66], labels=['0_18', '19_23', '24_30', '31_40', '41_66'] )
agg_df["COUNTRY"]=agg_df["COUNTRY"].str.upper()
agg_df["SEX"]=agg_df["SEX"].str.upper()
agg_df["SOURCE"]=agg_df["SOURCE"].str.upper()
agg_df = agg_df.applymap(str)
agg_df["PRICE"] = agg_df["PRICE"].astype(float)
#created customer_level_base to segment it into different groups
agg_df["customer_level_base"] = agg_df["COUNTRY"] + "_" + agg_df["SOURCE"]+ "_" + agg_df["SEX"] + "_" + agg_df["AGE_CAT"]
#created unique customer_level_base rows
agg_df.groupby(["customer_level_base"]).agg({"PRICE": "mean"}).sort_values("PRICE", ascending=False)
#divided price into 4 different segments
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels = ["D", "C", "B", "A"])
agg_df.groupby("SEGMENT").agg({"PRICE": ["mean", "max", "sum"]})

new_agg = agg_df.groupby(["customer_level_base"]).agg({"PRICE": "mean"})
new_agg.reset_index(inplace = True)

def new_users_price_segment():
    new_user = input("give the new user's customer_level_base")
    for i in range(len(new_agg["customer_level_base"])):
        if new_agg["customer_level_base"][i] == new_user:
            return str(new_agg["PRICE"][i])+ " "+ str(agg_df["SEGMENT"][i])
