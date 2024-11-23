import streamlit as st # Web sitesindeki ayarlamaları ve tasarımları oluşturmak için kullanılır.

import plotly.express as px # seaborn kütüphanesi yerine bu kütüphaneyi kullanıyoruz web sitesi için. İnteraktif görseller yaratmamızı sağlar.

import pandas as pd
import os # Operating System 
import matplotlib.pyplot as plt 


# Streamlit sayfası için yapılandırma ayarlarını yükleyeceğiz
st.set_page_config('SuperStore!!!',page_icon='bar_chart_', layout='wide')


 # Uygulama Başlığını Belirtelim
st.title('Örnek Bir SuperStore EDA Analizi')

# Sayfanının üst kısmında boşluk miktarını arttırmak için css stili ekleyelim

st.markdown("<style>div.block-container{padding-top:2rem;}</style>",unsafe_allow_html=True)

# Kullanıcıya Dosya yükleme seçeneği sunucağız
f1 = st.file_uploader('Dosya Klasörü: Dosyayı Yükle', type=(['csv','txt','xlsx','xls']))


if f1 is not None:
    filename = f1.name # Yüklenen dosyanın adını aldık
    st.write(filename) # dosyanın ismini ekrana yazdırdık
    pd.read_csv(filename, encoding='utf-8') # Yüklenen dosyayı csv olarak okuduk
else:
    # Eğer kullanıcı dosya yüklemediyse yerel dosyadaki SuperStore.csv dosyasını alıcağız ve onu okuyacağız.
    os.chdir('/Users/yunusemrekayis/Desktop/superstore_project') # Bulunduğumuz dizini Superstore.csv klasörünün içinde olduğumuzdan emin olmak için yazdık
    df = pd.read_csv('Superstore.csv',encoding = 'utf-8')

# Sayfa düzenini 2 sütun olacak şekilde ayarlıyoruz
col1, col2 = st.columns(2)

# 'Order Date' sütununu tarih formatına çevirdik
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Verilerin başladığı ve bittiği tarhihler arasındaki aralığı hesaplıyoruz
baslangic_tarih = pd.to_datetime(df['Order Date']).min()
bitis_tarih = pd.to_datetime(df['Order Date']).max()

# Kullanıcıdan başlangıc ve bitil tarihini alıyoruz
with col1: # web sitenin sol kısmına yapmak istediğimiz işlemi with bloğunda yazıcaz
    tarih1 = pd.to_datetime(st.date_input('Sipariş başlangıç tarih',baslangic_tarih)) # kullanıcın seçmesi için başlangıç tarihi girdim

with col2:
    tarih2 = pd.to_datetime(st.date_input('Sipariş bitiş tarih',bitis_tarih)) # kullanıcının sipariş bitiş tarihini girmesini istedik

# Kullanicinin sectigi tarihleri kisitlayalim
df = df[(df['Order Date'] >= tarih1) & (df['Order Date'] <= tarih2)].copy() # hic bir zaman orijinal veri setini degistirmiyoruz. Kopyalariyla calisiyoruz.


# Kenar cubugu ekleyelim
st.sidebar.header('Filtreni Sec')

# bölge secengei ekleyelim kullanici bir ya da birden fazla bölge secebilir.
bölge = st.sidebar.multiselect('Bölgeni Sec', df['Region'].unique()) # Tüm bölgeleri 1 kere görüntülemesini sagladik

if not bölge:
    df2 = df.copy() # veri setinin tamamini kullaniyorum. ama orijinal veri setinde dokunmadan kopyasi ile islem yapiyorum
else:
    df2 = df[df['Region'].isin(bölge)]

# eyalet secengei ekleyelim kullanici bir ya da birden fazla eyalet secebilir.
eyalet = st.sidebar.multiselect('Eyaletini Sec', df['State'].unique()) # Tüm eyaletleri 1 kere görüntülemesini sagladik

if not eyalet:
    df3 = df2.copy() # veri setinin tamamini kullaniyorum. ama orijinal veri setinde dokunmadan kopyasi ile islem yapiyorum
else:
    df3 = df2[df2['State'].isin(eyalet)]