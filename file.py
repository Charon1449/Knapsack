from vega_datasets import data
import streamlit as st
import altair as alt
import os
import glob
import pandas as pd
import time
from DP import unboundedKnapsack_DP2
from DP import backtracking
import matplotlib.pyplot as plt
import plotly.express as px
from bokeh.plotting import figure

from BranchAndBound import knapsack_BB ,unboundedKnapsack

def csv_to_items(filename):
    capacity = filename.split('/')[-1].split('_')[-1].split('.')[0]
    data = pd.read_csv(filename)
    volumes =data['volumes'].tolist()
    gains =data['gains'].tolist()
    items = list()
    for item in range(0,len(volumes)):items.append([volumes[item] ,gains[item]])
    return items ,int(capacity)

def main():

    page1 = st.sidebar.selectbox("choisir une méthode exacte", ["Branch & Bound", "Programmation dynamique"])
    page2 = st.sidebar.selectbox("choisir une heuristique",["Order density","...." ])
    page3 = st.sidebar.selectbox("choisir une méthaheuristique", ["Algorithme Génétique", "Récuit Simulé"])

    if page1 =="":
        st.title("home")
    if page1 == "Branch & Bound":
        st.header("Branch & Bound")
      
        filename = file_selector()
        st.write('Vous avez choisi le fichier: `%s`' % filename)
        data = pd.read_csv(filename)
        st.write(data)
        #print(data)
        
        data = pd.read_csv(filename)
        wt = data['volumes'].tolist()
        val = data['gains'].tolist()
        a = filename.split('\\')[-1].split('_')[0]
        W = int(filename.split('\\')[-1].split('_')[1].split('.')[0])  # la capacité
        n = int(filename.split('\\')[-1].split('_')[0])
                
        
        if (n > 65) :
            start = time.time()
            unboundedKnapsack(W, n, val, wt)
            end = time.time()
            st.write("le poid du sack est: " ,W)
            st.write("le gain maximal est: " ,unboundedKnapsack(W, n, val, wt))
            st.write("le temps de calcul est: " ,(end-start)*1000 ,"ms")
            
            
        else:
            items, capacity = csv_to_items(filename)
            sol = knapsack_BB(items, capacity)
            start = time.time()
            unboundedKnapsack(W, n, val, wt)
            end = time.time()
            st.write("le poid du sack est: " ,sol[1])
            st.write("le gain maximal est: " ,sol[0])
            for elem in sol[2]:
                st.write(elem[1]," de l'element avec le volume: " ,elem[0])
            st.write("le temps de calcul est: " ,(end-start)*1000 ,"ms")
        
        


    elif page1 == "Programmation dynamique":
        st.title("Programmation Dynamique DP")
        st.write("entrer manuellement les données:")
        poids,gain,capa=st.beta_columns([2, 2,2])
        poids = poids.text_input("volume")
        gain = gain.text_input("gain")
        capa=capa.number_input("capacité")
        capa=int(capa)

        if st.button("Add row"):
            get_data().append({"volumes": poids, "gains": gain})

        df = pd.DataFrame(get_data())
        st.write(df)

        if st.button("Add csv file"):
            df.to_csv('myFile.csv', columns=["volumes", "gains"], index=False)


        ########################################################################
        filename = file_selector()
        st.write('Vous avez choisi le fichier: `%s`' % filename)
        data = pd.read_csv(filename)
        st.write(data)
        tps3 = time.time()
        wt = data['volumes'].tolist()
        val = data['gains'].tolist()
        if (filename==r"C:\Users\eugenes\Desktop\tp_optim_project\myFile.csv"):
            W=capa
        else:
            a = filename.split('\\')
            d = a[2].split('_')
            h = d[1].split('.')
            W = int(h[0])  # la capacité

        st.write(W)

        n = len(val)
        elements = []
        listpoids = []
        listvaleurs = []

        sol = unboundedKnapsack_DP2(W, n, val, wt)
        elements = backtracking(sol, W, n, val, wt)

        for i in range(len(elements)):
            listpoids.append(wt[elements[i]])
            listvaleurs.append(val[elements[i]])

        st.write("Solution optimale:",sol[W])
        st.write("Poids total: ",sum(listpoids))
        #st.write("Items:",elements)
        #st.write("Poids des items:", listpoids)
        #st.write("Valeurs des items:", listvaleurs)
        tps4 = time.time()
        st.write("Execution time:", tps4 - tps3)

        st.title("Fichier de taille entre 5 et 205 objets ")
        # '1000_591952.csv'
        a = ['205_129.csv', '200_180.csv', '195_410.csv', '190_841.csv', '185_659.csv', '180_997.csv', '175_523.csv',
             '170_951.csv', '165_703.csv', '160_580.csv', '155_752.csv', '150_143.csv', '145_531.csv', '140_208.csv',
             '135_578.csv', '130_969.csv', '125_765.csv', '120_371.csv', '115_777.csv', '110_571.csv', '105_436.csv',
             '100_468.csv', '95_629.csv', '90_859.csv', '85_850.csv', '80_348.csv', '75_618.csv', '70_510.csv',
             '65_666.csv', '60_655.csv', '55_704.csv', '50_490.csv', '45_788.csv', '40_362.csv', '35_247.csv',
             '30_493.csv', '25_484.csv', '20_718.csv', '15_216.csv', '10_154.csv']
        tmp = []
        instances = []
        for g in range(len(a)):
            tps1 = time.time()
            data = pd.read_csv(a[g])
            wt = data['volumes'].tolist()
            val = data['gains'].tolist()
            w = a[g].split('_')
            h = w[1].split('.')
            W = int(h[0])  # la capacité
            n = len(val)
            instances.append(n)
            elements = []
            listpoids = []
            listvaleurs = []

            sol = unboundedKnapsack_DP2(W, n, val, wt)
            elements = backtracking(sol, W, n, val, wt)

            for i in range(len(elements)):
                listpoids.append(wt[elements[i]])
                listvaleurs.append(val[elements[i]])

            #     print("Solution optimale:",sol[W])
            #     print("Items:",elements)
            #     print("Poids des items:",listpoids)
            #     print("Valeurs des items:",listvaleurs)
            tps2 = time.time()
            tmp.append(tps2 - tps1)

        #st.write("tailles des instaces",instances)
        #st.write("temps d'exécution",tmp)

        fig=plt.figure(figsize=(10, 8), dpi=80)
        plt.plot(instances, tmp, color="forestgreen", label="DP")
        plt.xlabel("taille des instances (objets)")
        plt.ylabel("temps d'exécution (s)")
        plt.legend()
        st.pyplot(fig)

    elif page2== "Order density":
        st.header("This is your data explorer.")
        st.write("Please select a page on the left.")
    elif page2==".....":
        st.header("This is your data explorer.")
        st.write("Please select a page on the left.")
    elif page3=="Algorithme Génétique":
        st.header("This is your data explorer.")
        st.write("Please select a page on the left.")
    elif page3=="Récuit Simulé":
        st.header("This is your data explorer.")
        st.write("Please select a page on the left.")

@st.cache(allow_output_mutation=True)
def get_data():
    return []
@st.cache
def load_data():
    df = data.cars()
    return df

def file_selector(folder_path='.'):
    filenames = glob.glob(r"C:\Users\eugenes\Desktop\tp_optim_project\*.csv")
    selected_filename = st.selectbox('Select a file', filenames)
    return selected_filename


def visualize_data(df, x_axis, y_axis):
    graph = alt.Chart(df).mark_circle(size=60).encode(
        x=x_axis,
        y=y_axis,
        color='Origin',
        tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
    ).interactive()

    st.write(graph)

if __name__ == "__main__":
    main()