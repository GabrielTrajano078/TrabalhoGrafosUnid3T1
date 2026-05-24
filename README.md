# TrabalhoGrafosUnid3T1

# Broken Minimum Spanning Tree

**Problema:** [Kattis – Broken Minimum Spanning Tree](https://open.kattis.com/problems/brokenminimumspanningtree)

---

## Integrantes do grupo

Gabriel Trajano - 2410361
Davi Lira Cysne - 2410372
Thiago Holanda
Lucas Bezerra
Artur da Ponte
---

## Linguagem utilizada

Python 3

---

## Como executar

```bash
python3 src/main.py < dados/entradas_do_problema.txt
```

Ou digitando a entrada manualmente:

```bash
python3 src/main.py
```

Não são necessárias bibliotecas externas; a solução usa apenas a biblioteca padrão do Python.

---

## Modelagem do problema como grafo ponderado

- **Vértices:** os `n` nós do grafo (numerados de 1 a n).
- **Arestas:** as `m` arestas ponderadas fornecidas na entrada.
- **Pesos:** os valores inteiros `w` de cada aresta.
- **Árvore de Ethan:** os primeiros `n-1` arestas da entrada formam uma árvore geradora, mas que pode não ser mínima.

O objetivo é transformar a árvore de Ethan em uma MST realizando o menor número possível de **trocas de arestas** (cada troca remove uma aresta da árvore atual e insere outra que não está na árvore, mantendo a propriedade de árvore geradora).

---

## Algoritmo utilizado

A solução é dividida em duas etapas:

### Etapa 1 – Encontrar uma MST que preserve o máximo de arestas da árvore de Ethan

Aplica-se o algoritmo de **Kruskal** com um critério de desempate: em caso de arestas com o mesmo peso, arestas que **já pertencem à árvore de Ethan** são priorizadas. Isso garante que a MST encontrada compartilhe o máximo possível de arestas com a árvore original, minimizando o número de trocas necessárias.

### Etapa 2 – Emparelhar as trocas

Após o Kruskal, identificam-se:
- `to_remove`: arestas da árvore de Ethan que **não** entraram na MST ótima (precisam ser removidas);
- `to_add`: arestas fora da árvore de Ethan que **entraram** na MST ótima (precisam ser inseridas).

Para cada aresta a adicionar (em ordem crescente de peso), percorre-se o caminho entre seus dois vértices na árvore atual. Nesse caminho, encontra-se a aresta marcada para remoção com **maior peso** e realiza-se a troca. A árvore é atualizada a cada passo.

O número mínimo de trocas é exatamente `|to_remove| = |to_add|`.

---

## Papel do Union-Find / DSU

O Union-Find (Disjoint Set Union) é utilizado no **Kruskal** para:
- verificar eficientemente se dois vértices já estão na mesma componente conexa (operação `find`);
- unir duas componentes ao aceitar uma aresta (operação `unite`).

A implementação usa **compressão de caminho** e **union by rank**, garantindo complexidade quase linear por operação — O(α(n)), onde α é a função inversa de Ackermann.

---

## Variação de MST usada

A variação consiste em encontrar uma **MST que maximize o número de arestas em comum** com a árvore fornecida. Isso é atingido pelo critério de desempate no Kruskal: entre arestas de mesmo peso, arestas da árvore inicial têm prioridade.

---

## Análise de complexidade

| Etapa | Complexidade |
|---|---|
| Ordenação das arestas (Kruskal) | O(m log m) |
| Kruskal com Union-Find | O(m · α(n)) |
| Reconstrução dos pais da árvore a cada troca | O(n) por troca |
| Busca do caminho na árvore a cada troca | O(n) por troca |
| Total de trocas | O(n) no pior caso |
| **Total** | **O(m log m + n²)** no pior caso |

**Memória:** O(n + m) para armazenar o grafo e a árvore.

---

## Casos especiais relevantes

- **Grafo com arestas de mesmo peso:** o critério de desempate garante que a MST preserve o máximo de arestas da árvore original.
- **Multigrafo:** o enunciado permite múltiplas arestas entre o mesmo par de vértices; cada aresta é identificada pelo seu índice, não pelo par de vértices.
- **Árvore de Ethan já é MST:** nenhuma troca é necessária; a saída é `0`.
- **Todas as arestas precisam ser trocadas:** no pior caso, todas as `n-1` arestas da árvore são substituídas.

---

## Evidência de submissão

![Accepted](evidencias/accepted.png)

---
