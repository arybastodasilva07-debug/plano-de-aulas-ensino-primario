import streamlit as st
st.set_page_config(page_title="Plano de Aula Angola", layout="wide")
st.title("SISTEMA DE PLANO DE AULA")
st.subheader("Ensino Primario - Padrao INIDI")
# Menu Lateral (Sidebar)
with st.sidebar:
	st.header("Dados da Aula")
	classe = st.selectbox("Classe", ["Iniciacao", "1 Classe", "2 Classe", "3 Classe", "4 Classe", "5 Classe", "6 Classe"])
	disciplina = st.selectbox("Disciplina", ["Lingua Portuguesa", "Matematica", "Estudo do Meio", "Educacao Moral e Civica", "Desenho", "Musica", "Educacao Fisica"])
	tempo = st.text_input("Tempo", "45 min")
	aula_no = st.number_input("Aula Numero", min_value=1)
# Corpo Principal
col1, col2 = st.columns(2)
with col1:
	tema = st.text_input("Tema Geral")
	sumario = st.text_input("Sumario")
	obj_geral = st.text_area("Objetivos Gerais")
with col2:
	obj_aula = st.text_area("Objetivos da Aula")
	conteudo = st.text_area("Conteudo Teorico")
	material = st.text_input("Material Didactico")
if st.button("Sugerir Atividades Locais"):
	st.info("Sugestao: Use materiais da comunidade (pedras, sementes) e exemplos de mercados locais.")
st.divider()
st.subheader("Fases da Aula")
f1, f2 = st.columns(2)
with f1:
	f_intro = st.text_area("1. Introducao", placeholder="Revisao")
	f_med = st.text_area("2. Mediacao", placeholder="Explicacao")
with f2:
	f_dom = st.text_area("3. Dominio", placeholder="Exercicios")
	f_cont = st.text_area("4. Controle", placeholder="Avaliacao")
if st.button("Gerar Plano Final"):
	st.success("Plano pronto!")
	st.write(f"Diciplina: {disciplina} | Classe: {classe}")
	st.write(f"Tema: {tema}")
	st.write(f"Metodologia: {f_intro}, {f_med}, {f_dom}, {f_cont}"