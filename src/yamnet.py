import io
import csv
import numpy as np
import librosa
import tensorflow as tf
import tensorflow_hub as hub

model = hub.load('https://tfhub.dev/google/yamnet/1')

# Load class map to get human-readable labels
class_map_path = model.class_map_path().numpy().decode('utf-8')
class_names = []
with tf.io.gfile.GFile(class_map_path) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        class_names.append(row['display_name'])

def process_audio(file_bytes: bytes) -> tuple[list[float], list[dict]]:
    """
    Processes audio bytes, returns the averaged 1024-d embedding
    and the top 3 classes with their scores.
    """
    # Load audio using librosa (forces 16kHz mono as required by YAMNet)
    wav, _ = librosa.load(io.BytesIO(file_bytes), sr=16000, mono=True)

    # Run YAMNet
    scores, embeddings, spectrogram = model(wav)

    # Average the embeddings over all frames to get a single file-level vector
    file_embedding = np.mean(embeddings.numpy(), axis=0).tolist()

    # Calculate average scores across all frames to find top overall classes
    mean_scores = np.mean(scores.numpy(), axis=0)
    top_3_indices = np.argsort(mean_scores)[::-1][:3]

    top_classes = [
        {
            "index": int(i),
            "name": class_names[i],
            "score": round(float(mean_scores[i]), 4)
        }
        for i in top_3_indices
    ]

    return file_embedding, top_classes