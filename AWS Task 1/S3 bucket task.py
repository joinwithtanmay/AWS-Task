from flask import Flask, jsonify
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

app = Flask(__name__)

# Initialize the S3 client
s3_client = boto3.client('s3')

# Configuration: replace with your bucket name
BUCKET_NAME = "my-bucket"

@app.route('/list-bucket-content/<path:path>', methods=['GET'])
@app.route('/list-bucket-content/', defaults={'path': ''}, methods=['GET'])
def list_bucket_content(path):
    try:
        # Ensure the path ends with a slash to list "folders" correctly
        if path and not path.endswith('/'):
            path += '/'

        # List objects in the bucket with the specified prefix
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=path, Delimiter='/')

        # Collect folders and files
        folders = response.get('CommonPrefixes', [])
        files = response.get('Contents', [])

        content = []

        # Add folder names
        for folder in folders:
            content.append(folder['Prefix'].rstrip('/').split('/')[-1])

        # Add file names
        for file in files:
            if file['Key'] != path:  # Exclude the directory itself
                content.append(file['Key'].split('/')[-1])

        return jsonify({"content": content}), 200

    except NoCredentialsError:
        return jsonify({"error": "AWS credentials not found."}), 500
    except PartialCredentialsError:
        return jsonify({"error": "Incomplete AWS credentials."}), 500
    except ClientError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

