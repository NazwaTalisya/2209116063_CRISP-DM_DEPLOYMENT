import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

def load_data():
    data = pd.read_csv("clothes_price_prediction_data.csv")
    return data

def load_data1():
    data1 = pd.read_csv("data_cleaned.csv")
    return data1

def load_data2():
    data2 = pd.read_csv("data_before_mapping.csv")
    return data2

def distribusi_piechart():
    st.title('Brand Counts Pie Chart')
    # Load dataframe
    df = load_data()
    # Check if 'Brand' column exists in the dataframe
    if 'Brand' not in df.columns:
        st.error("Dataframe doesn't have 'Brand' column!")
        return
    brand_counts = df['Brand'].value_counts()
    # Plotting the pie chart
    fig, ax = plt.subplots()
    ax.pie(brand_counts, labels=brand_counts.index, autopct='%1.1f%%', startangle=360)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)
    st.write('Ini adalah diagram lingkaran yang menunjukkan proporsi jumlah merek sepatu dalam dataset, di mana masing-masing bagian mencerminkan persentase dari total jumlah merek yang ada. Merek "Under Armour" memiliki proporsi tertinggi dengan 17.9%, diikuti oleh "Puma" dengan 16.8%, "Adidas" dengan 16.6%, "Nike" dengan 16.5%, "New Balance" dengan 16.4%, dan "Reebok" dengan 15.8%.')
    
def distribusi_barchart():
    # st.title('Distribusi Sepatu & Baju Berdasarkan Brand')
    # Load dataframe
    df = load_data()
    # Check if the dataframe is not empty
    if df.empty:
        st.error("Dataframe is empty!")
        return
    # Plotting the distribution
    fig, ax = plt.subplots()
    sns.histplot(df['Brand'].dropna(), bins=50, kde=True, ax=ax)
    plt.title('Distribusi Sepatu & Baju Berdasarkan Brand')
    plt.xlabel('Brand Sepatu & Baju')
    plt.ylabel('Jumlah')
    st.pyplot(fig)
    st.write('Visualisasi diatas adalah sebuah bar chart yang menunjukkan distribusi jumlah sepatu dan pakaian berdasarkan brand. Dari grafik tersebut, terlihat bahwa brand dengan jumlah tertinggi adalah "Under Armour", sementara "Reebok" memiliki jumlah terendah. Garis biru yang melengkung di atas bar chart menunjukkan trend perubahan jumlah secara keseluruhan.')
    
def relation(data2):
    # Load dataframe
    df = load_data2()
    # st.title('Hubungan Relasi Antara Variabel Kategori')    
    # Check if the dataframe is not empty
    if df.empty:
        st.error("Dataframe is empty!")
        return
    # Encoding categorical variables
    df_encoded = df.apply(lambda x: pd.factorize(x)[0])  # Menggunakan factorize untuk encoding
    # Plotting heatmap
    fig, ax = plt.subplots()
    sns.heatmap(df_encoded.corr(), annot=True, cmap='coolwarm', ax=ax)
    plt.title('Hubungan Relasi Antara Variabel Kategori')
    st.pyplot(fig)
    st.write('Tampilan diatas adalah sebuah heatmap yang menunjukkan korelasi antara variabel kategori dalam dataset. Pada tampilan diatas yang berwana merah menunjukkan korelasi positif, sedangkan warna biru menunjukkan korelasi negatif. Dari heatmap ini, dapat disimpulkan bahwa tidak ada korelasi yang signifikan antara variabel kategori dalam dataset tersebut.')

def encode_labels(value, options):
    return options.index(value)

def predict():
    # Daftar pilihan untuk setiap fitur
    brand_options = ['Nike', 'Puma', 'Reebok', 'New Balance', 'Under Armour', 'Adidas']
    category_options = ['Dress', 'Jeans', 'Shoes', 'Sweater', 'Jacket', 'T-shirt']
    color_options = ['White', 'Black', 'Green', 'Red', 'Yellow', 'Blue']
    size_options = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
    material_options = ['Wool', 'Nylon', 'Silk', 'Cotton', 'Polyester', 'Denim']
    
    # Pilihan untuk setiap fitur dalam bentuk angka (label encoded)
    Brand = st.selectbox('Pilih Brand:', brand_options)
    Category = st.selectbox('Pilih Category:', category_options)
    Color = st.selectbox('Pilih Color:', color_options)
    Size = st.selectbox('Pilih Size:', size_options)
    Material = st.selectbox('Pilih Bahan:', material_options)
    Price = st.number_input('Masukan Harga:', 0,200)
    
    # Mengonversi pilihan menjadi angka menggunakan label encoding
    Brand_encoded = encode_labels(Brand, brand_options)
    Category_encoded = encode_labels(Category, category_options)
    Color_encoded = encode_labels(Color, color_options)
    Size_encoded = encode_labels(Size, size_options)
    Material_encoded = encode_labels(Material, material_options)
    
    button = st.button('Predict')
    if button:
        data = pd.DataFrame({
            'Brand' : [Brand_encoded],
            'Category' : [Category_encoded],
            'Color' : [Color_encoded],
            'Size' : [Size_encoded],
            'Material' : [Material_encoded],
            'Price' : [Price],
        })
        with open('gnb.pkl', 'rb') as file:
            loaded_model = pickle.load(file)
        predicted = loaded_model.predict(data)

        if (predicted == 0):
            st.write('Cheap')
        elif (predicted == 1):
            st.write('Affordable')
        else :
            st.error('Not Defined')
    