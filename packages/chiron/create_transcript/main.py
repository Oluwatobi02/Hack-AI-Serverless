
import boto3
import time
client = boto3.client(
    service_name='transcribe',
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name='us-east-2'
    )

s3 = boto3.client(
    service_name = 's3',
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name='us-east-2'
)

def create_transcript(data):
    client.start_transcription_job(
        TranscriptionJobName=data.get('jobName'),
        LanguageCode='en-US',
        Media={
            'MediaFileUri': data.get('mediaFileUri'),
        },
        OutputBucketName=data.get('outputBucketName'),
    )

    s3.put_object_acl(
        Bucket=data.get('outputBucketName'),
        Key=data.get('mediaFileUri').split('/')[-1],
        ACL='public-read'
    )
    
    return data['jobName']




def main(args):
    example = {'jobName': 'chiron2',
    'mediaFileUri': 's3://cosmos-bucket1/videoplayback.m4a',
    'outputBucketName': 'cosmos-bucket1'}
    res = create_transcript(example)
    print(res)
    return {'body': {
        'result': res,
        'success': 'True'
    }}