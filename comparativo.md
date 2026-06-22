# DSatur — Algoritmo de Coloração de Grafos por Grau de Saturação

> Documentação técnica e comparativo com outros algoritmos de coloração de grafos.

---

## 1. Introdução

### O que é coloração de grafos?

A **coloração de vértices** é um problema clássico da Teoria dos Grafos que consiste em atribuir uma "cor" (rótulo inteiro) a cada vértice de um grafo de forma que **nenhum par de vértices adjacentes compartilhe a mesma cor**. O menor número de cores necessário para colorir um grafo é chamado de **número cromático**, denotado por χ(G).

### O problema que a coloração resolve

Formalmente, dado um grafo G = (V, E), deseja-se encontrar uma função `c: V → {1, 2, …, k}` tal que:

```
∀ (u, v) ∈ E : c(u) ≠ c(v)
```

O objetivo é minimizar k — ou seja, usar o menor número possível de cores distintas.

### Aplicações práticas

| Domínio | Aplicação |
|---|---|
| Redes Wi-Fi | Alocação de frequências/canais a roteadores vizinhos |
| Compiladores | Alocação de registradores de CPU em análise de interferência |
| Escalonamento | Atribuição de horários a tarefas ou provas sem conflito |
| Mapas geográficos | Coloração de regiões adjacentes |
| Telecomunicações | Divisão de espectro entre antenas próximas |
| Sistemas distribuídos | Controle de acesso a recursos compartilhados |

Coloração de grafos é um problema **NP-difícil** no caso geral — não existe algoritmo polinomial conhecido que resolva todas as instâncias de forma ótima (a menos que P = NP). Por isso, heurísticas eficientes como o DSatur têm grande importância prática.

---

## 2. Explicação do Algoritmo DSatur

### O que é o DSatur?

O **DSatur** (*Degree of Saturation*) é uma heurística gulosa de coloração de grafos proposta por **Daniel Brélaz em 1979**. Ele aprimora os algoritmos gulosos tradicionais substituindo a ordem estática de processamento dos vértices por uma **seleção dinâmica baseada na saturação** — uma medida que captura a pressão de coloração sofrida por cada vértice ao longo da execução.

### O que é o grau de saturação?

O **grau de saturação** (ou saturação) de um vértice `v` é o **número de cores distintas** presentes na vizinhança de `v` entre os vértices já coloridos.

```
sat(v) = |{c(u) : u ∈ N(v), u já colorido}|
```

Quanto maior a saturação, mais restrito é o vértice — ele possui menos opções de cor disponíveis. Processar esses vértices mais cedo reduz o risco de conflitos e desperdício de cores.

### Como o algoritmo escolhe o próximo vértice?

A cada iteração, o DSatur seleciona o vértice não colorido que satisfaz, em ordem de prioridade:

1. **Maior saturação** — maior número de cores distintas na vizinhança já colorida.
2. **Maior grau** (desempate) — entre vértices com mesma saturação, escolhe o de maior grau no grafo original.
3. **Menor índice** (segundo desempate) — critério determinístico para garantir reprodutibilidade.

### Como ocorre a atribuição de cores?

Selecionado o vértice `v`, atribui-se a ele a **menor cor inteira positiva** que não esteja em uso por nenhum vizinho já colorido:

```
c(v) = min({1, 2, 3, …} \ {c(u) : u ∈ N(v), u já colorido})
```

Após a atribuição, a saturação de todos os vizinhos não coloridos de `v` é atualizada.

### Passo a passo resumido

```
1. Inicializar: todos os vértices sem cor; sat(v) = 0 para todo v.
2. Repetir até todos os vértices estarem coloridos:
   a. Selecionar v* = argmax_{v não colorido} sat(v)
                       (desempate: maior grau; segundo desempate: menor índice)
   b. Atribuir c(v*) = menor cor não usada por vizinhos de v*.
   c. Atualizar sat(u) para todo u ∈ N(v*) não colorido:
      se c(v*) ∉ cores_vizinhos(u) → sat(u) += 1.
3. Retornar a coloração c e o número total de cores k usadas.
```

**Complexidade:** O(V²) no pior caso para a seleção do máximo a cada iteração. Com uma fila de prioridade otimizada, variantes chegam a O((V + E) log V).

---

## 3. Comparativo com Outros Algoritmos

### 3.1 Greedy Coloring (Coloração Gulosa Simples)

**Ideia principal:**
Percorre os vértices em uma ordem fixa (geralmente a ordem natural dos índices) e atribui a cada vértice a menor cor disponível que não conflite com nenhum vizinho já colorido. Não há nenhum critério inteligente de priorização — a ordem de entrada determina o resultado.

**Estratégia de escolha dos vértices:**
Ordem de inserção ou ordem natural dos índices. A sequência é definida antes da execução e não se altera durante o algoritmo.

**Forma de coloração:**
Para cada vértice `v` na ordem pré-definida:
```
c(v) = min({1, 2, 3, …} \ {c(u) : u ∈ N(v), u já colorido})
```

**Vantagens:**
- Implementação trivial — menos de 15 linhas de código.
- Complexidade O(V + E) — o mais rápido entre os comparados.
- Adequado para aplicações onde a qualidade da coloração não é crítica.
- Funciona bem em grafos com estrutura regular ou muito esparsos.

**Desvantagens:**
- Extremamente sensível à ordem dos vértices: a mesma instância pode gerar colorações muito piores dependendo da permutação de entrada.
- Pode usar até Δ + 1 cores (onde Δ é o grau máximo do grafo), longe do ótimo.
- Sem qualquer garantia de qualidade.

**Complexidade:** O(V + E) em tempo; O(V) em espaço auxiliar.

**Qualidade da solução:** Geralmente fraca. No pior caso, produz colorações com o dobro (ou mais) do número cromático.

---

### 3.2 Welsh-Powell

**Ideia principal:**
Aprimora o Greedy Coloring adotando uma ordem inicial mais inteligente: os vértices são ordenados por **grau decrescente** antes de iniciar a coloração. A intuição é que vértices com mais vizinhos devem ser coloridos cedo, quando ainda há mais liberdade de escolha.

**Estratégia de escolha dos vértices:**
Ordena todos os vértices por grau (decrescente) uma única vez, antes da execução. A ordem é **estática** — não se atualiza com o progresso da coloração.

**Forma de coloração:**
Idêntica ao Greedy: para cada vértice na ordem pré-definida, atribui a menor cor não usada por nenhum vizinho já colorido.

**Vantagens:**
- Simples de implementar — é o Greedy com uma etapa de ordenação.
- Produz resultados consistentemente melhores que o Greedy puro.
- Custo adicional mínimo: apenas O(V log V) para a ordenação inicial.
- Bom desempenho em grafos com distribuição de graus irregular (vértices hubs).

**Desvantagens:**
- A ordenação é estática: ignora como a coloração evolui. Um vértice de alto grau pode ter poucos conflitos reais quando chega sua vez, e vice-versa.
- Não garante o número cromático.
- Em grafos densos ou regulares (todos os vértices com o mesmo grau), o ganho sobre o Greedy simples é praticamente nulo.

**Complexidade:** O(V log V + E) em tempo.

**Qualidade da solução:** Moderada — melhor que o Greedy puro, mas inferior ao DSatur, especialmente em grafos com estrutura irregular.

---

### 3.3 DSatur *(algoritmo implementado neste projeto)*

**Ideia principal:**
Substitui a ordem estática do Welsh-Powell por uma prioridade **dinâmica**: a cada iteração seleciona o vértice não colorido com maior saturação. Como a saturação mede a pressão real de cor sobre cada vértice (quantas cores distintas já aparecem na vizinhança), o DSatur reage ao estado corrente da coloração em vez de seguir um plano fixo.

**Estratégia de escolha dos vértices:**
Seleção dinâmica a cada iteração:
1. Maior saturação (número de cores distintas na vizinhança já colorida).
2. Empate resolvido pelo maior grau.
3. Segundo empate resolvido pelo menor índice.

**Forma de coloração:**
Atribui a menor cor que não conflite com nenhum vizinho já colorido — igual ao Greedy, mas a *ordem* de processamento é o diferencial.

**Vantagens:**
- Produz colorações muito próximas do número cromático na maioria dos grafos práticos.
- Adaptativo: reage ao estado corrente da coloração.
- Aplicações diretas em alocação de frequências (Wi-Fi), registradores de compiladores e escalonamento.
- Complexidade polinomial O(V²) — viável para grafos de médio porte.
- Garante coloração ótima em grafos bipartidos e diversas classes especiais.

**Desvantagens:**
- Mais complexo de implementar que Greedy e Welsh-Powell.
- O(V²) pode ser lento para grafos com centenas de milhares de vértices.
- Ainda é heurístico — não garante χ(G) no caso geral.

**Complexidade:** O(V²) no pior caso; O(V + E) em espaço.

**Qualidade da solução:** Boa — frequentemente encontra colorações ótimas ou com apenas uma cor a mais que o ótimo.

---

### 3.4 Backtracking / Branch and Bound

**Ideia principal:**
Abordagem **exata**: explora recursivamente todas as atribuições de cor possíveis, garantindo encontrar o número cromático χ(G). O Backtracking puro retrocede ao encontrar conflito; o Branch and Bound acrescenta **podas por limite inferior/superior** para descartar ramos que não podem melhorar a melhor solução já encontrada.

**Estratégia de escolha dos vértices:**
Tipicamente ordem fixa (ex: índice crescente). Variantes avançadas usam heurísticas de *fail-first* (escolher o vértice com mais restrições ativas) para reduzir o espaço de busca.

**Forma de coloração:**
Para cada vértice, tenta atribuir cada cor de 1 a k:
- Se a atribuição é válida, avança para o próximo vértice.
- Caso contrário, tenta a próxima cor.
- Se nenhuma cor funciona, retrocede (backtrack).
- Repete reduzindo k até provar que k−1 cores são insuficientes.

**Vantagens:**
- Garante a solução ótima (número cromático exato).
- Necessário quando o custo de uma cor extra é inaceitável (ex: alocação regulatória de espectro).
- Com boas heurísticas de poda, resolve instâncias pequenas/médias em tempo razoável.

**Desvantagens:**
- Complexidade exponencial — inviável para grafos grandes.
- O problema é NP-difícil; não existe solução polinomial conhecida.
- Implementação complexa, especialmente com podas eficientes.
- Consumo de memória pode ser proibitivo.

**Complexidade:** O(k^V · E) no pior caso sem poda; com poda, intratável na prática para grafos com V > 50–100 vértices dependendo da estrutura.

**Qualidade da solução:** Perfeita — encontra exatamente χ(G). É o padrão de referência (*gold standard*) para avaliar heurísticas.

---

## 4. Tabela Comparativa

| Critério                    | Greedy Coloring       | Welsh-Powell          | DSatur                      | Backtracking / B&B           |
|-----------------------------|-----------------------|-----------------------|-----------------------------|------------------------------|
| **Tipo de abordagem**       | Heurística gulosa     | Heurística gulosa     | Heurística gulosa adaptativa| Exato                        |
| **Complexidade**            | O(V + E)              | O(V log V + E)        | O(V²)                       | O(k^V · E) pior caso         |
| **Qualidade da solução**    | Fraca                 | Moderada              | Boa                         | Ótima (χ(G) garantido)       |
| **Facilidade de implementação** | Muito fácil       | Fácil                 | Moderada                    | Difícil                      |
| **Desempenho prático**      | Muito rápido          | Rápido                | Rápido (grafos médios)      | Lento / inviável para V > 100|
| **Ordem dos vértices**      | Estática / arbitrária | Estática (grau ↓)     | Dinâmica (saturação ↓)      | Estática ou heurística       |
| **Garante ótimo?**          | Não                   | Não                   | Não (mas próximo)           | Sim                          |
| **Uso indicado**            | Grafos regulares / prototipagem | Grafos esparsos irregulares | Redes reais, alocação de frequências | Instâncias pequenas / benchmarks |

---

## 5. Exemplo Prático

### Grafo de exemplo

Considere o grafo G com 5 vértices e 7 arestas:

```
Vértices: {0, 1, 2, 3, 4}
Arestas:  {(0,1), (0,2), (0,3), (1,2), (1,4), (2,3), (3,4)}

Adjacências:
  0: [1, 2, 3]   grau = 3
  1: [0, 2, 4]   grau = 3
  2: [0, 1, 3]   grau = 3
  3: [0, 2, 4]   grau = 3
  4: [1, 3]      grau = 2
```

Representação visual:

```
    0
   /|\
  1 2 3
  |/  |
  *   4
  \ /
   (1--4, 3--4)
```

### Execução passo a passo do DSatur

**Estado inicial:**
| Vértice | Cor | Saturação | Grau |
|---------|-----|-----------|------|
| 0       | —   | 0         | 3    |
| 1       | —   | 0         | 3    |
| 2       | —   | 0         | 3    |
| 3       | —   | 0         | 3    |
| 4       | —   | 0         | 2    |

---

**Iteração 1:**
- Todos os vértices têm saturação 0. Desempate pelo maior grau: {0, 1, 2, 3} empatam com grau 3. Segundo desempate pelo menor índice: **vértice 0**.
- Menor cor disponível (nenhum vizinho colorido): **cor 1**.
- Atualiza saturação dos vizinhos de 0: sat(1) = 1, sat(2) = 1, sat(3) = 1.

| Vértice | Cor | Saturação | Grau |
|---------|-----|-----------|------|
| 0       | **1** | —       | 3    |
| 1       | —   | 1         | 3    |
| 2       | —   | 1         | 3    |
| 3       | —   | 1         | 3    |
| 4       | —   | 0         | 2    |

---

**Iteração 2:**
- Vértices {1, 2, 3} têm saturação 1 (máxima). Desempate pelo grau (todos 3). Segundo desempate pelo menor índice: **vértice 1**.
- Vizinhos coloridos de 1: {0 → cor 1}. Menor cor disponível: **cor 2**.
- Atualiza: sat(2) += 1 → sat(2) = 2; sat(4) += 1 → sat(4) = 1.

| Vértice | Cor | Saturação | Grau |
|---------|-----|-----------|------|
| 2       | —   | **2**     | 3    |
| 3       | —   | 1         | 3    |
| 4       | —   | 1         | 2    |

---

**Iteração 3:**
- Vértice 2 tem saturação 2 (máxima). **Vértice 2** selecionado.
- Vizinhos coloridos de 2: {0 → cor 1, 1 → cor 2}. Menor cor disponível: **cor 3**.
- Atualiza: sat(3) += 1 → sat(3) = 2.

| Vértice | Cor | Saturação | Grau |
|---------|-----|-----------|------|
| 3       | —   | **2**     | 3    |
| 4       | —   | 1         | 2    |

---

**Iteração 4:**
- Vértice 3 tem saturação 2 (máxima). **Vértice 3** selecionado.
- Vizinhos coloridos de 3: {0 → cor 1, 2 → cor 3}. Menor cor disponível: **cor 2**.
- Atualiza: sat(4) += 1 → sat(4) = 2.

| Vértice | Cor | Saturação | Grau |
|---------|-----|-----------|------|
| 4       | —   | **2**     | 2    |

---

**Iteração 5:**
- Único vértice restante: **vértice 4**.
- Vizinhos coloridos de 4: {1 → cor 2, 3 → cor 2}. Ambos têm a mesma cor. Menor cor disponível: **cor 1**.

---

**Resultado final:**

| Vértice | Cor Atribuída |
|---------|---------------|
| 0       | 1             |
| 1       | 2             |
| 2       | 3             |
| 3       | 2             |
| 4       | 1             |

**Número de cores usadas: 3** (número cromático χ(G) = 3 — solução ótima ✓)

**Ordem de processamento:** 0 → 1 → 2 → 3 → 4

---

## 6. Vantagens do DSatur

### Por que ele costuma gerar boas soluções?

O DSatur toma decisões **localmente informadas**: em vez de seguir uma ordem cega, ele sempre prioriza o vértice que está sob maior pressão de coloração. Isso imita raciocínio humano — quando há uma restrição urgente, resolva-a primeiro antes que piore.

Formalmente, ao escolher vértices de alta saturação:
- Reduz a probabilidade de forçar o uso de uma cor nova desnecessariamente.
- Distribui as cores de forma mais equilibrada ao longo da execução.
- Evita situações onde vértices altamente conectados (com muitas restrições acumuladas) ficam para o final sem opções de cor acessíveis.

### Quando o DSatur supera o Greedy simples?

| Cenário | Greedy | DSatur |
|---|---|---|
| Grafo irregular com hubs de alto grau | Pode atribuir muitas cores desnecessárias | Prioriza hubs cedo, minimizando cores |
| Grafo com estrutura de cluster | Sensível à ordem: pode "desperdiçar" cores | Detecta saturação alta nas fronteiras dos clusters |
| Grafo denso (muitas arestas) | Alta chance de usar Δ + 1 cores | Frequentemente alcança χ(G) ou χ(G) + 1 |
| Grafos de interferência de rádio | Resultado depende do cadastro dos roteadores | Resultado consistente e próximo ao ótimo |

### Heurística e minimização do número de cores

O DSatur não garante χ(G) — é uma heurística. Mas a escolha do vértice mais saturado age como um **princípio de fail-first**: ao resolver primeiro as restrições mais difíceis, diminui a chance de criar conflitos irresolvíveis que forçariam o uso de uma cor extra no futuro.

Em testes empíricos com grafos aleatórios e grafos de Benchmark (DIMACS), o DSatur tipicamente produz colorações com **χ(G)** ou **χ(G) + 1** cores — desempenho muito superior ao Greedy e comparável ao Welsh-Powell, porém com maior robustez em grafos irregulares.

---

## 7. Conclusão

O **DSatur** representa o ponto ideal entre simplicidade e qualidade para o problema de coloração de grafos quando se busca uma solução prática e eficiente:

- **Ponto forte principal:** a seleção dinâmica por saturação adapta o algoritmo ao estado real da coloração, produzindo soluções consistentemente próximas do número cromático.
- **Quando escolher o DSatur:** em grafos de tamanho médio onde a qualidade da coloração importa (alocação de frequências, escalonamento, registradores de compiladores) e onde a solução exata é computacionalmente inviável.
- **Importância:** o DSatur é um marco histórico em coloração de grafos — publicado em 1979 por Brélaz, permanece relevante como referência de heurística eficiente, sendo estudado, implementado e aprimorado até hoje em pesquisas de otimização combinatória.

Embora não garanta o número cromático exato, o DSatur é, na prática, **uma das melhores heurísticas polinomiais de coloração de grafos disponíveis**, superando o Greedy simples e o Welsh-Powell na grande maioria dos casos, ao custo de uma implementação ligeiramente mais elaborada.

---

## Possíveis Melhorias

| Melhoria | Descrição | Benefício esperado |
|---|---|---|
| **Visualização do grafo** | Integrar uma biblioteca (ex: NetworkX + Matplotlib) para renderizar o grafo colorido | Facilita validação visual e uso educacional |
| **Análise de desempenho** | Medir o tempo de execução e o número de cores gerado em função de V e E | Valida a complexidade teórica O(V²) na prática |
| **Comparação experimental** | Executar todos os quatro algoritmos sobre as mesmas instâncias e comparar # cores e tempo | Quantifica empiricamente as diferenças de qualidade |
| **DSatur com heap** | Substituir a busca linear pelo máximo por uma fila de prioridade | Reduz complexidade para O((V + E) log V) |
| **Instâncias DIMACS** | Testar sobre benchmarks padronizados (grafos de coloração DIMACS) | Permite comparação com resultados publicados na literatura |
| **Geração de grafos aleatórios** | Adicionar gerador de grafos G(n, p) de Erdős-Rényi | Permite análise estatística do comportamento médio |

---

*Documentação elaborada como parte de projeto acadêmico em Teoria dos Grafos.*
