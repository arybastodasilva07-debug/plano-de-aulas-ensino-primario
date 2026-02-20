import streamlit as st
from openai import OpenAI
from docx import Document
from docx.shared import Inches
import io
import os

# ---------------- CONFIGURAÇÃO ----------------
st.set_page_config(page_title="Plano de Aula - INIDE Angola", layout="wide")
st.title("🇦🇴 SISTEMA PROFISSIONAL DE PLANO DE AULA")
st.subheader("Ensino Primário (Iniciação à 6ª Classe)")

# ---------------- OPENAI CLIENT ----------------
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("❌ API Key não configurada. Vá em Settings → Secrets e adicione OPENAI_API_KEY.")
    st.stop()

client = OpenAI(api_key=api_key)

# ---------------- CURRÍCULO COMPLETO ----------------
curriculo = {
    "Iniciação": {
        "Língua Portuguesa": {
            "Alfabetização": ["Letras e Sons", "Palavras Simples"],
            "Leitura Inicial": ["Compreensão de pequenas histórias", "Identificação de personagens"]
        },
        "Matemática": {
            "Números": ["Contagem até 10", "Comparação de quantidades", "Sequências numéricas"],
            "Formas e Medidas": ["Formas básicas", "Tamanho e comprimento", "Noções de tempo"]
        },
        "Estudo do Meio": {
            "O Meu Corpo": ["Partes do corpo", "Sentidos"],
            "Família e Escola": ["Família", "Regras da Escola", "Amigos e colegas"]
        },
        "Educação Visual e Plástica": {
            "Desenho e Pintura": ["Cores primárias", "Formas geométricas simples"],
            "Modelagem": ["Massinha", "Argila simples"]
        },
        "Educação Física": {
            "Movimento": ["Correr", "Pular", "Equilíbrio"],
            "Jogos Simples": ["Brincadeiras de roda", "Cooperação em grupo"]
        }
    },

    # ----------------- 1ª Classe -----------------
    "1ª Classe": {
        "Língua Portuguesa": {
            "TEMA 1 - QUEM SOU EU?": [
                "Eu sou",
                "Eu chamo-me",
                "Identificar pessoas",
                "Expressões de delicadeza",
                "Grafismos",
                "História: O Sapo e o Ovo"
        ],
            "TEMA 2 – A MINHA FAMÍLIA E EU": [
                "A família da Ana",
                "O alfabeto",
                "Estudo da letra I",
                "Estudo da letra O",
                "Estudo da letra U",
                "Estudo da letra E",
                "Estudo da letra A",
                "Vogais nasais",
                "Ditongos orais",
                "Ditongos nasais"
        ],
            "TEMA 3 – EU VOU À ESCOLA": [
                "Estudo da letra P",
                "Estudo da letra B",
                "Estudo da letra M",
                "Estudo da letra T",
                "Estudo da letra D",
                "Estudo da letra Ç",
                "Estudo da letra S",
                "Estudo da letra Z"
        ],
            "TEMA 4 – O MEU CORPO E EU": [
                "Estudo da letra N",
                "Estudo da letra L",
                "Estudo da letra X",
                "Estudo da letra F",
                "Higiene corporal",
                "Estudo da letra V",
                "Estudo da letra G",
                "Estudo da letra J",
                "Estudo da letra C",
                "Estudo da letra Q",
                "Estudo da letra R"
            ],
            "TEMA 5 – OS ANIMAIS QUE EU CONHEÇO": [
                "Estudo da letra H",
                "Estudo da letra Y",
                "Estudo da letra W",
                "Som NH",
                "Som LH",
                "Som CH",
                "Som AR",
                "Som OL",
                "Som AM",
                "Som UM"
            ]
    },

        "Estudo do Meio": {
            "TEMA 1 - A DESCOBERTA DE SI PRÓPRIO": [
                "A minha identificação",
                "O meu corpo",
                "Órgãos dos sentidos",
                "Saúde do corpo",
                "Higiene do corpo",
                "Higiene alimentar",
                "Posturas correctas, repouso e sono",
                "Vacinas"
            ],
            "TEMA 2 - A FAMÍLIA": [
                "Membros da família",
                "Convivência com outras pessoas"
            ],
            "TEMA 3 - A HABITAÇÃO": [
                "Habitação",
                "Localização da habitação",
                "Compartimentos da habitação",
                "Habitação como lugar de convivência",
                "Cuidados com a casa"
            ],
            "TEMA 4 - A ESCOLA": [
                "A minha escola",
                "Localização da escola",
                "Compartimentos da escola",
                "Sala de aula",
                "Cuidados com a escola",
                "Material escolar",
                "Comunidade escolar"
            ],
            "TEMA 5 - ALIMENTAÇÃO": [
                "Necessidade de alimentação",
                "Alimentação rica e variada",
                "O que devemos comer",
                "Alimentos na nossa dieta",
                "Fonte dos alimentos",
                "Cuidados com os alimentos"
            ],
            "TEMA 6 - O VESTUÁRIO": [
                "Tipos de vestuário",
                "Materiais têxteis",
                "Higiene do vestuário"
            ],
            "TEMA 7 - A SEGURANÇA": [
                "Itinerários",
                "Sinais de trânsito",
                "Regras de trânsito",
                "Cuidados com líquidos inflamáveis e objectos perigosos"
            ],
            "TEMA 8 – AS PLANTAS": [
                "Estrutura das plantas",
                "Importância das plantas",
                "Cuidados com as plantas"
            ],
            "TEMA 9 – OS ANIMAIS": [
                "Animais domésticos e selvagens",
                "Estrutura dos animais",
                "Importância dos animais"
            ]
        },
    
        "Matemática": {
            "TEMA 1 – GEOMETRIA": [
                "Relações espaciais",
                "Sólidos geométricos",
                "Figuras geométricas planas",
                "Linhas rectas, curvas e quebradas",
                "Linhas abertas e fechadas"
            ],
            "TEMA 2 – NÚMEROS, CONJUNTOS E OPERAÇÕES": [
                "Números naturais até 10",
                "Números naturais até 20",
                "Conjuntos",
                "Números naturais até 50",
                "Números naturais até 100",
                "Adição",
                "Subtracção",
                "Multiplicação por 2, 3 e 4",
                "Divisão por 2, 3 e 4"
            ],
            "TEMA 3 – GRANDEZAS E MEDIDAS": [
                "Comprimento",
                "Massa",
                "Capacidade",
                "Relações temporais",
                "Dias da semana",
                "Dinheiro e moeda angolana"
            ]
        },
    
        "Educação Manual e Plástica": {
            "TEMA 1 – O DESENHO": [
                "Risco",
                "Traço e tracejo",
                "Pontos",
                "Rasgagem e colagem"
            ],
            "TEMA 2 – A PINTURA": [
                "Impressão e estampagem",
                "Digitintas",
                "Recorte e colagem"
            ],
            "TEMA 3 – A MODELAGEM": [
                "Preparar e amassar barro",
                "Separar e enrolar",
                "Modelagem com barro e plasticina"
            ],
            "TEMA 4 – AS CONSTRUÇÕES": [
                "Dobragem",
                "Recorte e embrulho",
                "Composição e colagem",
                "Construção com materiais diversos"
            ]
        },
    
        "Educação Musical": {
            "TEMA 1 – A VOZ": [
                "Pequenas canções",
                "Sons naturais e artificiais",
                "Canções populares"
            ],
            "TEMA 2 – O CORPO": [
                "Percussão corporal",
                "Reprodução de batimentos"
            ],
            "TEMA 3 – INICIAÇÃO À TEORIA DA MÚSICA": [
                "Pauta musical",
                "Notas Ré e Mi"
            ],
            "TEMA 4 – OS INSTRUMENTOS MUSICAIS": [
                "Instrumentos de percussão",
                "Audição de sons",
                "Jogos musicais"
            ],
            "TEMA 5 – INICIAÇÃO À TEORIA DA MÚSICA II": [
                "Notas Fá e Sol"
            ]
        },
    
        "Educação Física": {
            "TEMA 1 – Ginástica básica": [
                "Deslocamento",
                "Salto",
                "Lançamento",
                "Trepar",
                "Equilíbrio"
            ],
            "TEMA 2 – Ginástica rítmica": [
                "Ritmo"
            ],
            "TEMA 3 – Atletismo": [
                "Corrida de velocidade",
                "Corrida de resistência"
            ],
            "TEMA 4 – Jogos": [
                "Jogos com bola",
                "Jogos de correr",
                "Jogos de saltar",
                "Jogos sensoriais"]
        }
    },
    # ----------------- 2ª Classe -----------------
    "2ª Classe": {
        "Língua Portuguesa": {
            "Leitura": ["Compreensão de textos curtos", "Identificação de personagens e enredo"],
            "Escrita": ["Frases curtas", "Ditado de palavras e frases"],
            "Gramática": ["Substantivos, adjetivos", "Artigos e pronomes"]
        },
        "Matemática": {
            "Números e Operações": ["Adição e subtração com reagrupamento", "Multiplicação inicial"],
            "Geometria": ["Formas planas", "Medidas de comprimento e capacidade"]
        },
        "Estudo do Meio": {
            "Sociedade": ["Família, Escola e Comunidade", "Regras de convivência"],
            "Meio Natural": ["Animais, plantas e ambiente"]
        },
        "Educação Visual e Plástica": {
            "Desenho e Pintura": ["Cores, linhas e formas", "Pintura de objetos simples"],
            "Modelagem": ["Massinha, argila"]
        },
        "Educação Física": {
            "Movimento": ["Corrida, saltos, equilíbrio"],
            "Jogos": ["Cooperação e regras simples"]
        }
    },

    # ----------------- 3ª Classe -----------------
    "3ª Classe": {
        "Língua Portuguesa": {
            "Leitura e Compreensão": ["Textos curtos e pequenos contos", "Personagens e enredo"],
            "Escrita": ["Frases completas", "Dictados curtos"],
            "Gramática": ["Substantivos, adjetivos e pronomes", "Verbos no presente"]
        },
        "Matemática": {
            "Operações": ["Adição e subtração com dezenas", "Multiplicação inicial"],
            "Geometria e Medidas": ["Figuras planas e sólidas", "Medidas de comprimento e peso"]
        },
        "Estudo do Meio": {
            "Comunidade e Sociedade": ["Regras, profissões e funções", "Cooperação e cidadania"],
            "Meio Natural": ["Animais, plantas e ciclos da natureza"]
        },
        "Educação Visual e Plástica": {
            "Desenho e Pintura": ["Cores, linhas e formas mais complexas"],
            "Modelagem": ["Criação de formas e objetos simples"]
        },
        "Educação Física": {
            "Movimento": ["Coordenação, força e equilíbrio"],
            "Jogos e Brincadeiras": ["Trabalho em equipe e regras"]
        }
    },

    # ----------------- 4ª Classe -----------------
    "4ª Classe": {
        "Língua Portuguesa": {
            "Leitura": ["Textos narrativos e informativos", "Compreensão de enredo"],
            "Escrita": ["Redação curta", "Dictados intermediários"],
            "Gramática": ["Substantivos, adjetivos, pronomes e verbos"]
        },
        "Matemática": {
            "Números e Operações": ["Adição, subtração, multiplicação e divisão"],
            "Geometria": ["Figuras planas e sólidas", "Perímetro e área simples"]
        },
        "Estudo do Meio": {
            "Sociedade": ["Regras de convivência", "Cidadania"],
            "Meio Natural": ["Animais, plantas, água e solo"]
        },
        "Educação Visual e Plástica": {
            "Desenho e Pintura": ["Projetos de desenho detalhado", "Pintura de objetos e paisagens"],
            "Modelagem": ["Criação de figuras e esculturas simples"]
        },
        "Educação Física": {
            "Movimento": ["Força, coordenação e resistência"],
            "Jogos": ["Competição saudável e cooperação"]
        }
    },

    # ----------------- 5ª Classe -----------------
    "5ª Classe": {
        "Língua Portuguesa": {
            "Leitura": ["Textos literários e informativos", "Compreensão de personagens e enredo"],
            "Escrita": ["Redação média", "Dictado intermediário"],
            "Gramática": ["Classes de palavras, tempos verbais e pontuação"]
        },
        "Matemática": {
            "Números e Operações": ["Adição, subtração, multiplicação, divisão e frações"],
            "Geometria e Medidas": ["Figuras geométricas, perímetro, área e volume"]
        },
        "Estudo do Meio": {
            "Sociedade e Cidadania": ["Responsabilidade, regras e cidadania"],
            "Meio Natural": ["Ciclo da água, animais e plantas"]
        },
        "Educação Visual e Plástica": {
            "Desenho e Pintura": ["Projetos mais complexos", "Representação de paisagens"],
            "Modelagem": ["Esculturas simples e criativas"]
        },
        "Educação Física": {
            "Movimento": ["Coordenação avançada, resistência"],
            "Jogos": ["Cooperação, estratégia e regras"]
        }
    },

    # ----------------- 6ª Classe -----------------
    "6ª Classe": {
        "Língua Portuguesa": {
            "Leitura": ["Textos literários e científicos", "Compreensão crítica"],
            "Escrita": ["Redação avançada", "Resumo e ditado avançado"],
            "Gramática": ["Classes de palavras, tempos verbais e sintaxe"]
        },
        "Matemática": {
            "Números e Operações": ["Todas as operações, frações, decimais"],
            "Geometria e Medidas": ["Perímetro, área, volume e ângulos"]
        },
        "Estudo do Meio": {
            "Sociedade e Cidadania": ["Regras, ética e cidadania"],
            "Meio Natural": ["Ciclos da natureza, ecologia, sustentabilidade"]
        },
        "Educação Visual e Plástica": {
            "Desenho e Pintura": ["Projetos detalhados e criativos"],
            "Modelagem": ["Esculturas e criações tridimensionais"]
        },
        "Educação Física": {
            "Movimento": ["Coordenação, força, resistência e agilidade"],
            "Jogos": ["Estratégia, competição saudável e trabalho em grupo"]
        }
    }
}

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("🏫 Identificação")
    nome_escola = st.text_input("Nome da Escola")
    nome_professor = st.text_input("Nome do Professor")
    trimestre = st.selectbox("Trimestre", ["1º Trimestre", "2º Trimestre", "3º Trimestre"])
    logotipo = st.file_uploader("Logotipo da Escola (opcional)", type=["png","jpg","jpeg"])

    st.header("📚 Dados da Aula")
    classe = st.selectbox("Classe", list(curriculo.keys()))
    disciplinas = list(curriculo[classe].keys())
    disciplina = st.selectbox("Disciplina", disciplinas)
    temas = list(curriculo[classe][disciplina].keys())
    tema = st.selectbox("Tema", temas)
    subtemas = curriculo[classe][disciplina][tema]
    subtema = st.selectbox("Subtema", subtemas)
    aula_numero = st.number_input("Aula nº", min_value=1, step=1)
    tempo = "45 minutos"

    gerar = st.button("🧠 Gerar Plano de Aula")

# ---------------- FUNÇÃO PARA GERAR PLANO ----------------
def gerar_plano():
    prompt = f"""
Gere um plano de aula completo baseado no currículo oficial do INIDE (Angola).

Escola: {nome_escola}
Professor: {nome_professor}
Disciplina: {disciplina}
Classe: {classe}
Trimestre: {trimestre}
Tempo: {tempo}
Aula nº: {aula_numero}
Unidade temática: {tema}
Subtema: {subtema}

Se o subtema for amplo, divida em mais de uma aula de 45 minutos.

Estrutura obrigatória:
1. Objetivo Geral
2. Objetivos da Aula
3. Conteúdo
4. Material Didáctico
5. Metodologia
6. Actividades Chave
7. Tipo de Avaliação
8. Procedimentos:
    - Introdução
    - Desenvolvimento
    - Consolidação
    - Avaliação
    - Tarefa para Casa

Linguagem formal pedagógica.
Contexto angolano.
"""
    try:
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"Especialista em planos de aula do ensino primário angolano."},
                {"role":"user","content":prompt}
            ],
            temperature=0.5,
            max_tokens=1500
        )
        return resposta.choices[0].message.content
    except Exception as e:
        st.error(f"❌ Não foi possível gerar o plano. Motivo: {e}")
        st.stop()

# ---------------- FUNÇÃO PARA GERAR WORD ----------------
def gerar_word(plano_texto):
    doc = Document()
    doc.add_heading("REPÚBLICA DE ANGOLA", level=1)
    doc.add_paragraph(f"Escola: {nome_escola}")
    doc.add_paragraph(f"Professor: {nome_professor}")
    doc.add_paragraph(f"Disciplina: {disciplina}")
    doc.add_paragraph(f"Classe: {classe}")
    doc.add_paragraph(f"Trimestre: {trimestre}")
    doc.add_paragraph(f"Aula nº: {aula_numero}")
    doc.add_paragraph(f"Tempo: {tempo}\n")
    doc.add_heading("PLANO DE AULA", level=2)
    doc.add_paragraph(plano_texto)
    if logotipo is not None:
        doc.add_picture(logotipo, width=Inches(1.5))
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ---------------- EXECUÇÃO ----------------
if gerar:
    if not nome_escola or not nome_professor:
        st.warning("⚠️ Preencha Nome da Escola e Nome do Professor.")
    else:
        with st.spinner("Gerando plano profissional..."):
            plano = gerar_plano()
        st.success("✅ Plano gerado com sucesso!")
        st.markdown(plano)
        # Download TXT
        st.download_button("📥 Baixar em TXT", plano, "plano_de_aula.txt")
        # Download Word
        word_file = gerar_word(plano)
        st.download_button("📄 Baixar em Word (.docx)", word_file, "plano_de_aula.docx")



