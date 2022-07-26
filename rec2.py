

import numpy as np
import pandas as pd
import streamlit as st
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

data = pd.read_csv("Pro1.csv")
# data.drop("unnamed 0", axis=1, inplace=True)
df = data.pivot_table(index="Facilities", columns="Email", values="Rating").fillna(0)
df_matrix = csr_matrix(df.values) # converting the table to an array matrix
model_knn = NearestNeighbors(metric="cosine", algorithm="brute")
model_knn.fit(df_matrix)

def recom_system(distances, indices, index):
    pro = None
    rec = []
    for i in range(0, len(distances.flatten())):
        if i == 0:
            pro = df.index[index]
        else:
            rec.append(df.index[indices.flatten()[i]])
    return pro, rec



def main():
    st.title("Product Recommendation System")
    st.write("Banking Products")
    if st.checkbox("Registered Users"):
        st.write(data[["Email","Facilities","Rating"]].head())
    user = st.text_input("Enter your mail")
    if st.button("Enter"):
        if user in list(data["Email"].unique()):
            st.write(f"Welcome back! {user[:6].upper()}")
            index = data[data["Email"]==user].index[0]
            print(index)
            distances, indices = model_knn.kneighbors(df.iloc[index,:].values.reshape(1,-1), n_neighbors=6)
            product, rec = recom_system(distances, indices, index)
            print(product)
            st.write(f"your current product : ' __{product}__ '")
            st.write("#### Products you may like ")
            col1, col2, col3, col4, col5  = st.columns(5)
            with col1:
                st.write(f"__{rec[0]}__")
                # st.image("https://i.gifer.com/JVX7.gif")
            with col2:
                st.write(f"__{rec[1]}__")
                # st.image("https://i.gifer.com/JVX7.gif")
            with col3:
                st.write(f"__{rec[2]}__")
                # st.image("https://i.gifer.com/JVX7.gif")
            with col4:
                st.write(f"__{rec[3]}__")
                # st.image("https://i.gifer.com/JVX7.gif")
            with col5:
                st.write(f"__{rec[4]}__")
                # st.image("https://i.gifer.com/JVX7.gif")
            st.button("home")
        else:
            st.error("Invalid Username")
            # st.button("Home") 
            
        #st.write("## Thank you for Visiting \nProject by Suyog Hole") 
        #st.markdown("<h1 style='text-align: right; color: #d7e3fc; font-size: small;'><a href='https://github.com/suyog56recommendation'>Looking for Source Code?</a></h1>", unsafe_allow_html=True            

if __name__ == "__main__":
    main()