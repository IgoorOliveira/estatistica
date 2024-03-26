import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import base64
from io import BytesIO


# Função para converter o DataFrame em imagem PNG
def dataframe_to_png(df):
    plt.figure(figsize=(15, 10))
    plt.table(cellText=df.values, colLabels=df.columns, loc='center')
    plt.axis('off')
    
    # Salvar a imagem na memória
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    
    return img_buffer
    

def plot_pie_chart(df):
    # Definindo os intervalos de altura
    intervals = pd.cut(df['Alt'], bins=[0, 1.50, 1.60, 1.70, 1.80, float('inf')], labels=['<150', '150-160', '160-170', '170-180', '>=180'])
    
    # Contagem de valores em cada intervalo
    count_intervals = intervals.value_counts()
    
    # Calculando a porcentagem de cada intervalo em relação ao total
    porcentagem_intervals = (count_intervals / count_intervals.sum()) * 100
    
    # Criando o DataFrame com os dados para o gráfico de pizza
    df_pizza = pd.DataFrame({'Intervalo de Altura': porcentagem_intervals.index, 'Porcentagem': porcentagem_intervals.values})
    
    # Criando o gráfico de pizza
    fig_pizza = px.pie(df_pizza, values='Porcentagem', names='Intervalo de Altura', title='Porcentagem entre intervalos de altura')
    
    return fig_pizza

def get_image_download_link(img_buffer):
    # Codificar a imagem em base64
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}" download="dataframe.png">Baixar PNG</a>'
    return href

# Função para criar gráficos e estatísticas
def generate_stats_and_plots(df):
    stats = df['Alt'].describe()
    median = stats['50%']
    mean = stats['mean']
    min_val = stats['min']
    max_val = stats['max']
    mode = df['Alt'].mode()[0]
    
    custom_colors = {'A': 'rgb(255, 0, 0)', 'B': 'rgb(0, 255, 0)', 'C': 'rgb(0, 0, 255)'}

    # Criando o histograma com as cores personalizadas
    fig_hist = px.histogram(df, x='Alt', title='Histograma da Coluna "Alt"', color_discrete_map=custom_colors)

    # Criando o boxplot com as cores personalizadas
    fig_box = px.box(df, y='Alt', title='Boxplot da Coluna "Alt"',
                 color_discrete_map=custom_colors)
    
    return median, mean, min_val, max_val, mode, fig_hist, fig_box

# Configuração da página Streamlit
def main():
    st.title('Dashboard de Análise - Igor Ferreira de Oliveira')
    
    # Carregar dados
    file = pd.read_excel("questionario.xlsx")
    if file is not None:
        df = file
        
        # Mostrar os primeiros registros
        st.subheader('Dados Carregados:')
        st.dataframe(df)

        # Botão para fazer o download do DataFrame como PNG
        if st.button("Download DataFrame como PNG"):
            img_buffer = dataframe_to_png(df)
            st.markdown(get_image_download_link(img_buffer), unsafe_allow_html=True)
        
        # Gerar estatísticas e gráficos se a coluna 'Alt' estiver presente
        if 'Alt' in df.columns:
            median, mean, min_val, max_val, mode, fig_hist, fig_box = generate_stats_and_plots(df)
            
            # Mostrar estatísticas
            st.subheader('Estatísticas da Coluna "Alt"')
            st.write(f"Mediana: {median}")
            st.write(f"Média: {mean}")
            st.write(f"Mínimo: {min_val}")
            st.write(f"Máximo: {max_val}")
            st.write(f"Moda: {mode}")
            
            
            # Mostrar histograma
            st.subheader('Histograma da Coluna "Alt"')
            st.plotly_chart(fig_hist)
            
            # Mostrar boxplot
            st.subheader('Boxplot da Coluna "Alt"')
            st.plotly_chart(fig_box)

            fig_pizza = plot_pie_chart(df)
            st.plotly_chart(fig_pizza)
        else:
            st.error('A coluna "Alt" não foi encontrada no arquivo.')



if __name__ == "__main__":
    main()
