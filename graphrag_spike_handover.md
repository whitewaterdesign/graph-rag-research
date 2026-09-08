# GraphRAG Spike Handover

## Purpose

This handover captures the GraphRAG investigation discussed around the
paper **"Retrieval-Augmented Generation with Graphs (GraphRAG)" by Han
et al.**, with particular focus on how an existing Neo4j + LLM spike
maps onto the GraphRAG taxonomy and where to investigate next for
multi-hop retrieval.

## Existing Spike

The spike used an **LLM to query a Neo4j graph database** through tools
exposed to the model.

The model had access to tools that allowed it to:

-   retrieve/download the Neo4j database schema;
-   use the schema to understand available node types, relationships and
    properties;
-   formulate Cypher queries from natural-language questions; and
-   execute **read-only Cypher queries** against Neo4j.

Conceptually:

``` text
User question
    ↓
LLM
    ↓
Retrieve Neo4j schema
    ↓
Interpret schema
    ↓
Generate Cypher
    ↓
Read-only query tool
    ↓
Neo4j
    ↓
Query results
    ↓
LLM answer
```

The approach performed well for relatively simple queries and graph
traversals of approximately one or two hops.

The main limitation observed was **multi-hop reasoning/query
construction**. As the number of relationships required to answer a
question increased, the LLM became less reliable at constructing the
complete Cypher query.

## Mapping the Spike to the GraphRAG Paper

The paper presents GraphRAG as a pipeline containing five major
components:

``` text
Query
  ↓
Query Processor
  ↓
Retriever
  ↓
Graph Data Source
  ↓
Organizer
  ↓
Generator
```

The Neo4j spike primarily maps to **Query Structuration** within the
**Query Processor**.

The LLM converts a natural-language question into a structured graph
query---in this case **Cypher**---which is then executed against Neo4j.

MCP/tooling should therefore not itself be considered the retrieval
algorithm. It provides the interface through which the LLM discovers and
invokes capabilities. The GraphRAG mechanism of interest is the
transformation of the user's question into Cypher and the subsequent
graph retrieval.

## Query Processor Mechanisms

The paper identifies five main query-processing mechanisms.

### 1. Entity Recognition

Identifies entities mentioned in the user's question and connects them
to entities/nodes represented in the graph.

Example:

``` text
"Who works for Acme?"

Entity:
Acme
```

This can establish seed nodes for subsequent retrieval.

### 2. Relational Extraction

Identifies relationships expressed in the natural-language question and
maps them to relationships/edges represented in the graph.

Example:

``` text
"Who reports to Alice?"

Entity:
Alice

Relationship:
REPORTS_TO
```

### 3. Query Structuration

Transforms natural-language questions into structured queries suitable
for the underlying graph/database.

Examples discussed by the paper include:

-   Cypher
-   SPARQL
-   GraphQL / graph query languages

This is the mechanism that most closely describes the existing Neo4j
spike.

``` text
Natural language
    ↓
LLM
    ↓
Cypher
    ↓
Neo4j
```

### 4. Query Decomposition

Splits a complex question into multiple logically connected subqueries.

Instead of requiring the LLM to construct one large multi-hop Cypher
query, the system can solve smaller parts of the question independently
and combine the results.

Conceptually:

``` text
Complex question
    ↓
Subquery 1
Subquery 2
Subquery 3
    ↓
Retrieve intermediate results
    ↓
Combine evidence
    ↓
Answer
```

This is particularly relevant to the limitation identified in the spike.

### 5. Query Expansion

Enriches the original query with additional concepts or relationships
that may improve retrieval.

In GraphRAG this can use relational knowledge from the graph---for
example, neighbouring nodes or predefined relational templates---rather
than relying only on semantically similar terms.

## Main Retriever Mechanisms

The paper separately identifies the following representative retrieval
mechanisms.

### Entity Linking

Maps an entity mention in the query to the corresponding graph node.

### Relational Matching

Matches relationships expressed in the query to graph edges.

### Graph Traversal

Expands from seed nodes/edges through the graph.

Examples include:

-   BFS;
-   DFS;
-   path retrieval; and
-   k-hop neighbourhood retrieval.

Graph traversal is highly relevant to multi-hop GraphRAG because
traversal logic can retrieve candidate paths without requiring the LLM
to correctly construct the entire path upfront.

### Graph Kernels

Compare structural similarity between graphs or subgraphs.

Examples discussed include random-walk and Weisfeiler--Leman kernels.

This appears less directly relevant to the current Neo4j spike.

### Shallow Embeddings

Represent graph structure using learned embeddings.

Examples include:

-   DeepWalk;
-   Node2Vec;
-   Role2Vec; and
-   GraphWave.

These can retrieve nodes based on proximity or structural role.

### Deep Embeddings

Use graph-aware deep-learning models, particularly **Graph Neural
Networks (GNNs)**, to encode nodes, edges and subgraphs for retrieval.

### Domain Expertise / Rule-Based Retrieval

Uses predefined rules or domain-specific knowledge to guide which nodes,
relationships or subgraphs should be retrieved.

## Advanced Retrieval Strategies

The paper also describes higher-level strategies that combine or
orchestrate retrieval mechanisms.

### Integrated Retrieval

Combines multiple retrieval mechanisms.

A particularly important example is **neural-symbolic retrieval**, which
combines symbolic graph operations with learned/neural relevance
signals.

Example:

``` text
Question
    ↓
Identify candidate entities
    ↓
Symbolic graph expansion
    ↓
Candidate paths/subgraphs
    ↓
Neural relevance ranking
    ↓
Relevant evidence
```

### Iterative Retrieval

Retrieval occurs over multiple steps rather than requiring the complete
retrieval plan to be generated upfront.

Conceptually:

``` text
Question
    ↓
Identify seed entity
    ↓
Retrieve neighbours
    ↓
Reason about results
    ↓
Select promising relationship/path
    ↓
Retrieve again
    ↓
Reason
    ↓
...
    ↓
Sufficient evidence
    ↓
Answer
```

The paper discusses systems such as **ToG**, which iteratively expands
reasoning paths, and **StructGPT**, where an LLM repeatedly invokes
graph interfaces until enough information has been gathered.

This is particularly relevant to the existing tool-based architecture.

### Adaptive Retrieval

Dynamically determines how much retrieval or traversal is necessary.

For graph retrieval this includes choosing an appropriate traversal
depth. Too few hops may omit required evidence, while too many hops can
introduce large amounts of irrelevant information.

## Why the Existing Approach Struggles With Multi-Hop Questions

The current architecture effectively requires the LLM to infer the
complete graph path before executing the query.

For a simple question this might require:

``` text
A → B
```

or:

``` text
A → B → C
```

For a more complex question it may require the model to correctly infer:

``` text
A → B → C → D → E
```

and then encode the entire path correctly in Cypher.

This requires the LLM to simultaneously:

1.  understand the user's question;
2.  understand the database schema;
3.  identify the correct starting entities;
4.  identify each required relationship;
5.  determine relationship directions;
6.  determine the correct traversal depth; and
7.  generate syntactically and semantically correct Cypher.

Errors therefore compound as path complexity increases.

## Potential Direction for the Next Spike

The most directly relevant next experiment is to compare **one-shot
query structuration** with **iterative graph retrieval**.

### Current approach

``` text
Question
    ↓
Schema
    ↓
LLM generates complete Cypher
    ↓
Neo4j
    ↓
Answer
```

### Candidate approach

``` text
Question
    ↓
Entity recognition/linking
    ↓
Retrieve local graph structure
    ↓
LLM evaluates candidates
    ↓
Traverse promising relationship
    ↓
Evaluate intermediate result
    ↓
Continue traversal if necessary
    ↓
Answer
```

Rather than exposing only something equivalent to:

``` text
get_schema()
run_cypher(query)
```

a future tool interface could experiment with more constrained graph
operations such as:

``` text
find_entity(...)
get_node(...)
get_relationships(...)
get_neighbours(...)
get_paths(...)
traverse(...)
run_readonly_cypher(...)
```

The intention would be to determine whether allowing the model to
**reason → retrieve → inspect → retrieve again** improves multi-hop
accuracy compared with asking it to generate a complex Cypher query in a
single step.

## Key Distinction

The terminology should remain clear:

``` text
MCP / tool interface
        │
        └── How the LLM accesses capabilities

Query Structuration
        │
        └── How natural language becomes Cypher

Retriever
        │
        └── How relevant graph information is selected

Graph Traversal
        │
        └── How connected graph information is explored

Iterative Retrieval
        │
        └── How retrieval and reasoning are repeated over multiple steps
```

Therefore, the existing spike is best described as an **LLM-driven
query-structuration approach over Neo4j, exposed through an MCP/tool
interface**, rather than "MCP retrieval".

## Questions for Further Investigation

-   Does query decomposition improve multi-hop Cypher generation?
-   Does iterative retrieval outperform one-shot Cypher generation as
    hop count increases?
-   Should graph traversal be performed deterministically by the
    retrieval layer rather than planned entirely by the LLM?
-   How should candidate paths be ranked or pruned to prevent
    neighbourhood explosion?
-   Would a hybrid neural-symbolic retriever improve relevance over pure
    traversal?
-   What is the optimal division of responsibility between the LLM and
    Neo4j?
-   Should the LLM generate arbitrary Cypher or operate through
    constrained graph-retrieval tools?
-   How should retrieval quality be evaluated separately from
    final-answer quality?
-   How does performance change at 1, 2, 3, 4+ hops?

## Suggested Evaluation

A useful follow-up benchmark would contain questions grouped by required
graph depth:

  Category   Required reasoning
  ---------- -------------------------------
  1-hop      Direct relationship
  2-hop      Two connected relationships
  3-hop      Three connected relationships
  4+ hop     Complex graph reasoning

Compare at least:

1.  one-shot LLM-generated Cypher;
2.  decomposed Cypher queries;
3.  iterative graph retrieval; and
4.  optionally hybrid/neural-symbolic retrieval.

Measure:

-   correct answer rate;
-   valid Cypher rate;
-   correct entity selection;
-   correct relationship/path selection;
-   retrieval precision;
-   number of tool/database calls;
-   latency; and
-   token/cost overhead.

This would turn the initial observation---**"one or two hops work well;
multi-hop queries degrade"**---into a measurable GraphRAG retrieval
experiment.

## Source

Primary source used in the discussion:

**Han, H. et al. --- *Retrieval-Augmented Generation with Graphs
(GraphRAG)***, arXiv:2501.00309v2 (2025).

Relevant sections discussed:

-   Section 2 --- Holistic Framework of GraphRAG
-   Section 2.3 --- Query Processor
-   Section 2.3.1 --- Named Entity Recognition
-   Section 2.3.2 --- Relational Extraction
-   Section 2.3.3 --- Query Structuration
-   Section 2.3.4 --- Query Decomposition
-   Section 2.3.5 --- Query Expansion
-   Section 2.4 --- Retriever
-   Section 2.4.1 --- Heuristic-based Retriever
-   Section 2.4.2 --- Learning-based Retriever
-   Section 2.4.3 --- Advanced Retrieval Strategies
