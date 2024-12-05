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


def add_embeddings(index, parsed_data):
    pc.create_index(name=index, dimension=1536, metric='euclidean', spec=ServerlessSpec(cloud='aws', region='us-east-1'))
    pc_index = pc.Index(index)

    def process_sentence(sentence_data):
        sentence_text, (start_time, end_time) = sentence_data
        try:
            text_embeddings = get_embeddings(sentence_text)

            index_data = {
                'id': f"{start_time}-{end_time}",
                "timestamp": [start_time, end_time],
                "sentence": sentence_text,
                'values': text_embeddings,
            }

            pc_index.upsert([index_data])
            return f"Success: {sentence_text}"

        except Exception as e:
            return f"Error processing '{sentence_text}': {e}"

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(process_sentence, parsed_data))
    





def parse_data(data):
    sentences = []
    sentence = []
    timestamps = []
    
    sentence_start = None
    sentence_end = None

    for item in data:
        if item["type"] == "pronunciation":
            word = item["alternatives"][0]["content"]
            start_time = float(item["start_time"])
            end_time = float(item["end_time"])

            if sentence_start is None:
                sentence_start = start_time

            sentence.append(word)
            sentence_end = end_time

        elif item["type"] == "punctuation" and item["alternatives"][0]["content"] == ".":
            sentences.append(" ".join(sentence))
            timestamps.append((sentence_start, sentence_end))
            sentence = [] 
            sentence_start = None
            sentence_end = None

    if sentence:
        sentences.append(" ".join(sentence))
        timestamps.append((sentence_start, sentence_end))

    return sentences, timestamps

def main(args):
    res = requests.get(args.get('url', 'https://cosmos-bucket1.s3.us-east-2.amazonaws.com/chiron2.json'))
    data = res.json()
    result = parse_data(data)
    add_embeddings('chiron2', result)
    return {'body': {
        'success': 'True'
    }}