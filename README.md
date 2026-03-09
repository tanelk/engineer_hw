To start the server simply run
```bash
docker-compose up --build
```

Using the wav files from https://www.tensorflow.org/hub/tutorials/yamnet

### embeddings

It wasn't explicitly stated what this API should return, so I went with the yamnet classifications - more meaningful than the embeddings arrays. 
```
$ curl -X 'POST' localhost:8000/embeddings -F files=@miaow_16k.wav -F files=@speech_whistling2.wav
{
  "miaow_16k.wav": [
    {
      "index": 67,
      "name": "Animal",
      "score": 0.7132
    },
    {
      "index": 68,
      "name": "Domestic animals, pets",
      "score": 0.5123
    },
    {
      "index": 76,
      "name": "Cat",
      "score": 0.4236
    }
  ],
  "speech_whistling2.wav": [
    {
      "index": 396,
      "name": "Whistle",
      "score": 0.4235
    },
    {
      "index": 382,
      "name": "Alarm",
      "score": 0.3635
    },
    {
      "index": 35,
      "name": "Whistling",
      "score": 0.3431
    }
  ]
}
```

### search
```commandline
$ curl -X 'POST' localhost:8000/search -F file=@miaow_16k.wav
{
  "results": [
    {
      "filename": "miaow_16k.wav",
      "similarity": 1
    },
    {
      "filename": "speech_whistling2.wav",
      "similarity": 0.3599
    }
  ]
}
```