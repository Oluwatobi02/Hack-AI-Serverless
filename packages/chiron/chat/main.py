
import concurrent.futures
import requests
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
pc = Pinecone(api_key='')
client = OpenAI(api_key='')


def get_embeddings(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding


def search(index,text, k):
    pc_index = pc.Index(index)

    query_embedding = get_embeddings(text)
    result = pc_index.query(
        top_k=k,
        vector=query_embedding
    )
    return result['matches']

def feed_model(chunks, prompt, history, style):
    history = ' '.join(history)
    text_chunks = ' '.join([chunk['sentence'] for chunk in chunks])
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
    {"role": "system", "content": "you have context of this history, which will be passed into you, answer this or respond to this text with the style, which you will be giving, using this prompt you'll be giving"},
    {"role": "user", "content": f"text_chunks: {text_chunks}, prompt: {prompt}, style: {style}"}
  ]
)
    return {
        'response': completion.choices[0].message['content'],
        'timestamp': chunks[0]['timestamp'],
    }

def main(args):
    prompt = args.get('prompt', '')
    history = args.get('history', [])
    style = args.get('style', '')
    index = args.get('index', '')
    if not (index and prompt):
        return {
            'body': {
                'success': False
            }
        }
    chunks = search(index, prompt, 10)
    response = feed_model(chunks, prompt, history, style)
    return response
    

