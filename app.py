# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 01:59:03 2022

@author: Gaming PC
"""

import numpy as np
import pandas as pd
import streamlit as st
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

data= pd.read_csv("bankprod.csv")
df = data.pivot_table(index="product", columns="email", values="rating").fillna(0)
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
        st.write("Hello Welcome to Online Banking")
        st.write(data[["email","product","rating"]].head())
    user= st.text_input("Enter your Email")
    if st.button("Enter"):
        if user in list(data["email"].unique()):
            st.write(f"Welcome back! {user[4:9].upper()}")
            index = data[data["email"]==user].index[0]
            print(index)
            distances, indices = model_knn.kneighbors(df.iloc[index,:].values.reshape(1,-1), n_neighbors=6)
            product, rec = recom_system(distances, indices, index)
            print(product)
            st.write(f"your current product : ' __{product}__ '")
            st.write("#### Products you may like ")
            col1, col2, col3, col4, col5  = st.columns(5)
            with col1:
                st.write(f"__{rec[0]}__")
            with col2:
                st.write(f"__{rec[1]}__")
            with col3:
                st.write(f"__{rec[2]}__")
            with col4:
                st.write(f"__{rec[3]}__")
            with col5:
                st.write(f"__{rec[4]}__")
            st.button("home")
        else:
            st.error("Invalid Username")
            

if __name__ == "__main__":
    main()