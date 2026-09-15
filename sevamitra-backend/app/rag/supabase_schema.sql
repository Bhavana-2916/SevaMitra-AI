-- Run this once in Supabase: Dashboard > SQL Editor > New query > paste > Run

-- 1. Enable the vector extension (Supabase already ships this, just turns it on)
create extension if not exists vector;

-- 2. Table to store each PDF chunk + its embedding
create table if not exists document_chunks (
    id bigserial primary key,
    filename text not null,
    chunk_index int not null,
    content text not null,
    embedding extensions.vector(384)  -- 384 matches the all-MiniLM-L6-v2 model
);

-- 3. Function to find the most similar chunks to a given query embedding
create or replace function match_document_chunks (
    query_embedding extensions.vector(384),
    match_threshold float default 0.55,
    match_count int default 4
)
returns table (
    id bigint,
    filename text,
    content text,
    similarity float
)
language sql stable
as $$
    select
        document_chunks.id,
        document_chunks.filename,
        document_chunks.content,
        1 - (document_chunks.embedding <=> query_embedding) as similarity
    from document_chunks
    where 1 - (document_chunks.embedding <=> query_embedding) >= match_threshold
    order by document_chunks.embedding <=> query_embedding
    limit match_count;
$$;
