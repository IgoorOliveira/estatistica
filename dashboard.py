import pandas as pd
import streamlit as st
import plotly.express as px

# Função para carregar os dados do arquivo Excel
def load_data(file):
    df = pd.read_excel(file)
    return df

def plot_pie_chart(df):
    # Definindo os intervalos de altura
    intervalos = pd.cut(df['Alt'], bins=[0, 1.50, 1.60, 1.70, 1.80, float('inf')], labels=['<150', '150-160', '160-170', '170-180', '>=180'])
    
    # Contagem de valores em cada intervalo
    contagem_intervalos = intervalos.value_counts()
    
    # Calculando a porcentagem de cada intervalo em relação ao total
    porcentagem_intervalos = (contagem_intervalos / contagem_intervalos.sum()) * 100
    
    # Criando o DataFrame com os dados para o gráfico de pizza
    df_pizza = pd.DataFrame({'Intervalo de Altura': porcentagem_intervalos.index, 'Porcentagem': porcentagem_intervalos.values})
    
    # Criando o gráfico de pizza
    fig_pizza = px.pie(df_pizza, values='Porcentagem', names='Intervalo de Altura', title='Porcentagem entre intervalos de altura')
    
    return fig_pizza

# Função para criar gráficos e estatísticas
def generate_stats_and_plots(df):
    stats = df['Alt'].describe()
    median = stats['50%']
    mean = stats['mean']
    min_val = stats['min']
    max_val = stats['max']
    
    fig_hist = px.histogram(df, x='Alt', title='Histograma da Coluna "Alt"')
    fig_box = px.box(df, y='Alt', title='Boxplot da Coluna "Alt"')
    
    return median, mean, min_val, max_val, fig_hist, fig_box

# Configuração da página Streamlit
def main():
    st.title('Dashboard de Análise')
    
    # Carregar dados
    file = st.file_uploader("Carregar arquivo Excel", type=["xlsx"])
    if file is not None:
        df = load_data(file)
        
        # Mostrar os primeiros registros
        st.subheader('Dados Carregados:')
        st.write(df.head())
        
        # Gerar estatísticas e gráficos se a coluna 'Alt' estiver presente
        if 'Alt' in df.columns:
            median, mean, min_val, max_val, fig_hist, fig_box = generate_stats_and_plots(df)
            
            # Mostrar estatísticas
            st.subheader('Estatísticas da Coluna "Alt"')
            st.write(f"Mediana: {median}")
            st.write(f"Média: {mean}")
            st.write(f"Mínimo: {min_val}")
            st.write(f"Máximo: {max_val}")
            
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
