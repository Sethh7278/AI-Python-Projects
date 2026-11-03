# RAG Practice

A small practice project for learning retrieval-augmented generation (RAG). It answers questions about travelling in Thailand by finding the most relevant chunk of travel info and passing it to an LLM to write the answer.

This is a learning exercise, not a finished product.

## How it works

1. **Chunks**: travel info is split into small named chunks, e.g. `bike_rental`, `grand_palace`, `currency`.
2. **Retrieval**: the user's question is matched against the chunks to find the most relevant one.
3. **Generation**: the best chunk is given to the LLM along with the question, so the answer is based on that info rather than the model's general knowledge.

## Retrieval: keyword search vs embeddings

I built retrieval in two stages:

- **Step 4b, keyword search**: ranks chunks by how many of the question's words they contain.
- **Step 4c, embedding search**: turns the question and each chunk into vectors and picks the chunk with the closest meaning (cosine similarity).

The difference matters for questions that use different words from the source text. For example, "how much does a scooter cost" should find `bike_rental` even though the word "scooter" may not appear in it. Keyword search tends to miss these; embeddings are designed to catch them. Keyword search can still do better on exact names and rare terms.

Example test questions:

| Question | Should find |
|---|---|
| "how much does a scooter cost" | bike_rental |
| "what should I wear at the temple" | grand_palace |
| "how much money do I need" | currency |

## What I learned

- How a basic RAG pipeline fits together: chunk → retrieve → generate.
- Why embedding search handles paraphrased questions better than plain keyword matching.

## Next steps

- Measure both methods on a set of test questions and compare scores.
- Try returning the top 3 chunks instead of only the best one.
- Try combining keyword and embedding search (hybrid search).