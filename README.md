# Dataset Card — MQD-1209

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19209391.svg)](https://doi.org/10.5281/zenodo.19209391)

> **Como citar:**
> Feitosa, A. R.; Silva, G. G. P. (2026). *MQD-1209: Dataset de Análise de Sentimentos em Português Brasileiro com Anotação Pareada por Gênero*. Zenodo. https://doi.org/10.5281/zenodo.19209391

---

## 1. Contextualização

O MQD-1209 é um dataset de **Análise de Sentimentos (AS) em português brasileiro** construído para investigar divergências interpretativas associadas ao gênero do anotador em tarefas de Classificação de Textos (CT). Trata-se do primeiro recurso público que combina, para o português brasileiro: (i) anotação pareada por grupos de gênero equilibrados, (ii) metadados de tempo de resposta preservados no nível do julgamento individual, e (iii) protocolo controlado de quatro anotadores por grupo por instância.

O corpus textual é derivado do **MQD-1465**, conjunto de frases extraídas do portal [Meu Querido Diário](http://www.meuqueridodiario.com.br) — plataforma pública de diários pessoais em português brasileiro. Os textos preservam sua forma original, incluindo variações ortográficas e expressões coloquiais, o que os torna representativos da escrita informal espontânea em redes sociais.

O dataset foi produzido no âmbito da dissertação de mestrado *"Do Anotador ao Classificador: Identificação e Mensuração de Viés de Gênero em Análise de Sentimentos para o Português Brasileiro"* (CEFET/RJ, 2026) e é um dos componentes da **Metodologia de Identificação de Viés (MIV)**. O estudo foi aprovado por Comitê de Ética em Pesquisa sob o protocolo CAAE nº 82267824.8.0000.5289.

---

## 2. Metodologia de Coleta

### 2.1 Origem e pré-processamento do corpus

O corpus de partida (MQD-1465, n = 1.465) passou pelo seguinte pipeline em Python antes da anotação:

- Remoção de dois registros duplicados (IDs 476 e 953), resultando em **1.463 frases únicas**
- Randomização com semente fixa (`seed = 42`) para reprodutibilidade
- Padronização textual: remoção de espaços e aspas redundantes
- Particionamento em **10 blocos sequenciais de até 150 frases** (bloco 10 com 113 frases)

### 2.2 Plataforma e protocolo de anotação

A coleta foi realizada na plataforma **PCIbex Farm** ([farm.pcibex.net](https://farm.pcibex.net)), que permite experimentos psicolinguísticos online com registro automático de tempo de resposta.

- **Período de coleta:** `[PREENCHER: mês/ano início] a [PREENCHER: mês/ano fim]`
- **Tarefa:** Classificar cada frase em uma de três classes de sentimento — *negativa*, *neutra* ou *positiva*
- **Protocolo:** Cada participante acessou um bloco distinto e realizou a anotação de forma autônoma e assíncrona, sem acesso às avaliações dos demais
- **Registro:** Para cada julgamento foram registrados o identificador anonimizado do participante (hash MD5 do endereço IP), o rótulo atribuído e o tempo de evento (usado para calcular duração em segundos)

### 2.3 Participantes

| | Masculino | Feminino | Total |
|---|---|---|---|
| Anotadores únicos | 26 | 20 | **46** |
| Anotações individuais | 7.015 | 6.302 | **13.317** |
| Anotações por pessoa: mediana | 150 | 150 | — |
| Anotações por pessoa: máx | 1.463 | 900 | — |

O gênero foi **autodeclarado** pelos participantes no início de cada sessão e utilizado exclusivamente como critério de estratificação analítica, sem associação a qualquer outro dado pessoal identificável.

### 2.4 Consolidação do dataset final

Para cada instância e cada grupo de gênero, o rótulo majoritário foi determinado por **voto de pluralidade** entre os quatro julgamentos utilizados (em ordem de chegada):

- Configurações válidas: unanimidade (4-0-0), maioria qualificada (3-1-0) e pluralidade simples (2-1-1)
- Configurações de empate (2-2-0): instância descartada
- O dataset final (**MQD-1209**) contém apenas instâncias com pluralidade válida em **ambos** os grupos simultaneamente (*inner join*)

| Etapa | n |
|---|---|
| Corpus após deduplicação (MQD-1463) | 1.463 |
| Anotações individuais coletadas | 13.317 |
| Frases com pluralidade válida — masculino | 1.388 |
| Frases com pluralidade válida — feminino | 1.263 |
| **Dataset final (MQD-1209)** | **1.209** |

---

## 3. Descrição dos Dados

### 3.1 Estrutura do arquivo

`MQD-1209_majoritarias.csv` — separado por tabulação, codificação UTF-8, 1.209 linhas de dados + 1 linha de cabeçalho.

| Coluna | Tipo | Descrição |
|---|---|---|
| `frase` | string | Texto original da instância |
| `duracao_media_masculino` | float | Duração média dos julgamentos do grupo masculino (s) |
| `total_classificacoes_masculino` | int | Total de votos utilizados no grupo masculino (sempre 4) |
| `classificacao_majoritaria_masculino` | string | Rótulo majoritário do grupo masculino |
| `votos_maioria_masculino` | int | Votos na classe majoritária — masculino |
| `total_positiva_masculino` | int | Votos em *positiva* — masculino |
| `total_negativa_masculino` | int | Votos em *negativa* — masculino |
| `total_neutra_masculino` | int | Votos em *neutra* — masculino |
| `duracao_media_feminino` | float | Duração média dos julgamentos do grupo feminino (s) |
| `total_classificacoes_feminino` | int | Total de votos utilizados no grupo feminino (sempre 4) |
| `classificacao_majoritaria_feminino` | string | Rótulo majoritário do grupo feminino |
| `votos_maioria_feminino` | int | Votos na classe majoritária — feminino |
| `total_positiva_feminino` | int | Votos em *positiva* — feminino |
| `total_negativa_feminino` | int | Votos em *negativa* — feminino |
| `total_neutra_feminino` | int | Votos em *neutra* — feminino |
| `concordancia_grupos` | int | 1 = grupos concordaram; 0 = discordaram |

### 3.2 Estatísticas descritivas por atributo numérico

| Atributo | Média | Mediana | DP | Mín | Máx |
|---|---|---|---|---|---|
| `duracao_media_masculino` (s) | 10,19 | 5,56 | 35,57 | 1,52 | 786,77 |
| `duracao_media_feminino` (s) | 10,92 | 6,62 | 35,02 | 2,04 | 917,63 |
| `votos_maioria_masculino` | 3,41 | 4,00 | 0,67 | 2 | 4 |
| `votos_maioria_feminino` | 3,32 | 3,00 | 0,64 | 2 | 4 |
| `total_positiva_masculino` | 1,54 | 1,00 | 1,62 | 0 | 4 |
| `total_negativa_masculino` | 1,44 | 1,00 | 1,67 | 0 | 4 |
| `total_neutra_masculino` | 1,01 | 0,00 | 1,32 | 0 | 4 |
| `total_positiva_feminino` | 1,23 | 0,00 | 1,48 | 0 | 4 |
| `total_negativa_feminino` | 1,41 | 1,00 | 1,63 | 0 | 4 |
| `total_neutra_feminino` | 1,35 | 1,00 | 1,37 | 0 | 4 |
| `concordancia_grupos` | 0,84 | 1,00 | 0,36 | 0 | 1 |

### 3.3 Comprimento das frases

| Métrica | Média | Mediana | DP | Mín | Máx | P25 | P75 |
|---|---|---|---|---|---|---|---|
| Tokens (palavras) | 18,16 | 16,00 | 9,94 | 3 | 77 | 11 | 24 |
| Caracteres | 97,25 | 85,00 | 52,95 | 16 | 411 | 57 | 127 |

Distribuição por faixa de tokens:

| Faixa | n | % |
|---|---|---|
| 1–5 palavras | 41 | 3,4% |
| 6–10 palavras | 254 | 21,0% |
| 11–20 palavras | 508 | 42,0% |
| 21–40 palavras | 369 | 30,5% |
| 41+ palavras | 37 | 3,1% |

### 3.4 Distribuição de classes por grupo

| Classe | Masculino n | Masculino % | Feminino n | Feminino % |
|---|---|---|---|---|
| Negativa | 444 | 36,7% | 440 | 36,4% |
| Neutra | 290 | 24,0% | 363 | 30,0% |
| Positiva | 475 | 39,3% | 406 | 33,6% |

O grupo feminino empregou a classe *neutra* com frequência 25,2% superior ao grupo masculino (363 vs 290 instâncias), evidenciando maior cautela interpretativa diante de conteúdos de polaridade atenuada.

### 3.5 Qualidade da anotação e concordância entre grupos

| Métrica | Valor |
|---|---|
| Instâncias concordantes | 1.021 (84,4%) |
| Instâncias discordantes | 188 (15,6%) |
| Cohen's κ (κ_inicial) | **0,7652** — faixa *Substantial* (Landis & Koch, 1977) |
| IC 95% bootstrap (κ) | [0,7352 ; 0,7962] |
| Cramér's V | 0,7669 |
| χ² de independência | 1422,18 (p ≈ 0) |

### 3.6 Padrões de discordância entre grupos (n = 188)

| Masculino → Feminino | n | % das discordâncias |
|---|---|---|
| positiva → neutra | 76 | 40,4% |
| negativa → neutra | 43 | 22,9% |
| neutra → negativa | 28 | 14,9% |
| neutra → positiva | 18 | 9,6% |
| positiva → negativa | 17 | 9,0% |
| negativa → positiva | 6 | 3,2% |

Os dois padrões dominantes (positiva→neutra e negativa→neutra) respondem por **63,3%** das discordâncias, indicando que o grupo feminino tende a atenuar julgamentos polares, e não a inverter a polaridade.

### 3.7 Certeza intragrupo

| Grupo | Certeza média (votos_maioria / 4) | Mediana | DP | Unanimidade (4-0-0) |
|---|---|---|---|---|
| Masculino | 0,8515 | 1,00 | 0,169 | 620 (51,3%) |
| Feminino | 0,8288 | 0,75 | 0,159 | 496 (41,0%) |

O grupo masculino apresenta maior taxa de unanimidade interna (+10,3 p.p.), o que é consistente com o padrão de menor uso da classe neutra observado na distribuição de rótulos.

### 3.8 Duração dos julgamentos por concordância

| Condição | Grupo | Mediana (s) | Média (s) | DP (s) |
|---|---|---|---|---|
| Concordante (n = 1.021) | Masculino | 5,44 | 9,51 | 30,55 |
| Concordante (n = 1.021) | Feminino | 6,39 | 10,66 | 36,14 |
| Discordante (n = 188) | Masculino | 6,03 | 13,84 | 55,38 |
| Discordante (n = 188) | Feminino | 7,53 | 12,36 | 28,25 |

Em ambos os grupos, os julgamentos sobre instâncias discordantes levaram mais tempo (mediana ~10–25% superior), sugerindo que maior dificuldade interpretativa se manifesta tanto no tempo de resposta quanto na divergência entre grupos.

---

## 4. Correlações Relevantes

Correlações de Spearman calculadas sobre os 1.209 pares de julgamentos (outliers de duração > percentil 99 excluídos nas correlações com duração):

| Par de variáveis | ρ de Spearman | p-valor | Interpretação |
|---|---|---|---|
| Duração × certeza — masculino | −0,156 | < 0,001 | Julgamentos mais rápidos tendem a ser mais unânimes |
| Duração × certeza — feminino | −0,043 | 0,135 | **Não significativo** — tempo não prediz certeza no grupo feminino |
| Certeza masculino × certeza feminino | +0,265 | < 0,001 | Concordância moderada de certeza entre grupos |
| Concordância × duração masculino | −0,086 | 0,003 | Instâncias discordantes levam mais tempo |
| Concordância × duração feminino | −0,100 | < 0,001 | Idem, efeito ligeiramente maior no grupo feminino |

A assimetria na correlação duração × certeza entre os grupos é um achado de interesse para estudos futuros sobre estilos de deliberação por gênero em tarefas de rotulagem.

---

## 5. Trabalhos Baseados neste Dataset

- Feitosa, A. R.; Silva, G. G. P. (2026). *Do Anotador ao Classificador: Identificação e Mensuração de Viés de Gênero em Análise de Sentimentos para o Português Brasileiro*. Dissertação de Mestrado, CEFET/RJ. [principal trabalho de origem]

---

## 6. Possibilidades de Uso

- **Análise de viés de anotação por gênero** em tarefas de AS para português brasileiro
- **Treinamento e avaliação de classificadores de sentimento** com rótulos estratificados por grupo demográfico, permitindo análise de impacto da fonte de supervisão
- **Benchmark de concordância interanotador** em contextos de língua portuguesa
- **Estudos de tempo de decisão em crowdsourcing** — os metadados de duração preservados são raros em datasets públicos de NLP
- **Validação de metodologias de detecção de viés amplificado** — o dataset foi desenhado para ser instância empírica da MIV, mas pode ser reutilizado em frameworks alternativos
- **Investigação de características linguísticas correlacionadas com dificuldade interpretativa** — instâncias discordantes constituem subconjunto de interesse para análise qualitativa

---

## 7. Considerações Éticas e Limitações

- Estudo aprovado pelo CEP sob protocolo CAAE nº 82267824.8.0000.5289
- Participação voluntária com consentimento informado
- Dados anonimizados: participantes identificados apenas por hash MD5, sem associação a qualquer informação pessoal identificável
- O gênero é autodeclarado e tratado como variável binária (m/f) — limitação reconhecida; estudos futuros devem contemplar representações não binárias
- O corpus provém de um único domínio (diários pessoais informais); generalização para outros domínios requer investigação dedicada
- Os metadados de duração individual por anotador (antes da agregação por grupo) estão disponíveis nos arquivos intermediários (`MQD-13317_anotacoes_totais.csv`) para análises futuras

---

## 8. Licença

Este dataset é disponibilizado sob a licença **Creative Commons Attribution 4.0 International (CC BY 4.0)**.
Você pode compartilhar e adaptar o material para qualquer finalidade, incluindo comercial, desde que atribua crédito adequado.
Detalhes: https://creativecommons.org/licenses/by/4.0/

---

## 9. Contato

Alexander Ramos Feitosa — CEFET/RJ, Programa de Pós-graduação em Ciência da Computação
Orientador: Prof. D.Sc. Gustavo Guedes Paiva e Silva
