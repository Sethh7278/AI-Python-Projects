# RAG Practice

A practice project for learning retrieval-augmented generation (RAG). It answers questions about travelling in Thailand using my own travel notes, cites the notes it used, and says when its notes don't cover a question.

This is a learning exercise, not a finished product.

## How it works

1. **Notes:** 9 short Markdown notes I wrote, one topic each (e.g. `bike_rental`, `grand_palace`, `currency`).
2. **Embedding:** each note is turned into an embedding with `text-embedding-3-small`.
3. **Retrieval:** the question is embedded and compared with every note using a dot product (equivalent to cosine similarity, since OpenAI embeddings are normalised). The top 3 notes scoring above **0.25** are kept.
4. **Generation:** the kept notes and the question are sent to `gpt-4o-mini`, which answers only from the notes and cites its sources.
5. **No match:** if no note scores above 0.25, it replies "My notes don't cover that" without calling the model.

## Retrieval: keyword search vs embeddings

I built retrieval in two stages:

- **Keyword search (4b):** ranks notes by how many of the question's words they contain.
- **Embedding search (4c):** ranks notes by how close their meaning is to the question.

Embeddings help when the question uses different words from the note. For example, "what should I wear at the temple" should find `grand_palace`, even though the note talks about covering your shoulders rather than what to "wear". Keyword search can still do well on exact names and rare terms.

| Question | Should find | Keyword search | Embedding search |
|---|---|---|---|
| "how much does a scooter cost" | bike_rental | <result> | <result> |
| "what should I wear at the temple" | grand_palace | <result> | <result> |
| "how much money do I need" | currency | <result> | <result> |
| "what visa do I need for Japan" | nothing | <result> | <result> |

## Choosing the 0.25 cut-off

Similarity scores are almost never 0, so I needed a cut-off. 0.25 kept relevant notes, such as for the scooter question, and filtered out unrelated ones, such as for the Japan visa question.

## Error handling

- No relevant notes → "My notes don't cover that", without calling the model
- Empty question → asks for a valid question
- API failure → a friendly message instead of a crash

## What I learned

- How a basic RAG pipeline fits together: load notes → embed → retrieve → generate.
- When the bot gives a bad answer, check retrieval and generation separately: were the right notes found, and did the model use them well?
- Why embeddings handle reworded questions better than keyword matching.
- Prompts work better when the notes and the question are clearly labelled and separated.

## Limitations

- Only as accurate as the notes; some figures are approximate.
- Time-sensitive notes, like visa rules, need re-checking.
- Notes are re-embedded every time the script starts.

## Next steps

- Turn the test questions into an automated evaluation (Rung 5).
- Try combining keyword and embedding search (hybrid search).

## How to run

```bash
cd task4
python RAG.py
```