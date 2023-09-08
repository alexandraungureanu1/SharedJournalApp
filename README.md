# Shared Journal - Emotion Detection and Insult Classification

## Introduction

 Application designed for creating journals with posts containing text, images, or audio files. Users can interact with the platform to create and share content while benefiting from automated features such as emotion detection in images and audio files and insult classification in comments.

## Architecture

Built around the concept of user-generated journals with the following features:

- **Text Posts**: Users can create textual posts, both public and private.
- **Comment Analysis**: Comments are analyzed for insults before being posted.
- **Image Posts**: Users can upload or capture images directly on the platform, and these images are analyzed to identify one of seven supported emotions using facial detection and sentiment recognition.
- **Audio Posts**: Similar to image posts, users can upload or record audio files directly on the platform, and the audio content is analyzed to identify one of six supported emotions.

## Application Implementation and Deployment

Implemented using the Django framework and deployed on Google Cloud App Engine. Data storage is managed through Google Cloud services:

- **Google Buckets**: Used for storing images, audio files, and models.
- **Cloud SQL**: Stores user information, comments, and journal data.
- **Secret Manager**: Safely stores keys and environment variables.
- **Google Cloud Function**: Utilized for all three final detection models.

## Automatic Emotion Detection from Image Content

Uses FER2013 dataset. Images are augmented and pre-processed through cropping, pixel filling, rotation, translation, zooming, normalization, and centering. Machine learning models for emotion detection include:

- Convolutional Neural Network (CNN) - 69.13% accuracy.
- Attentional CNN - 65.72% accuracy.
- ResNet-based architecture - 66.53% accuracy.
- Transfer Learning with VGG-16 - 64.10% accuracy.
- Transfer Learning with MobileNet - 62.43% accuracy.
- Transfer Learning with Xception - 58.28% accuracy.

## Text Insult Detection

Utilizes a dataset available at [link](https://www.kaggle.com/competitions/jigsaw-toxic-comment-classification-challenge/code) for insult detection in text comments. The process includes synonym replacement for comments classified as insults and extensive pre-processing steps like emoji transformation, URL removal, punctuation and digit removal, lowercase transformation, contraction removal, stop-word removal, and stemming. The following models are employed:

- Supervised Learning Models with feature extraction using TF-IDF vectorizer (1, 2, 3-grams) and algorithms such as KNN, SVM, Logistic Regression, Naive Bayes, and Random Forest with hyperparameter tuning using GridSearch.
- Unsupervised Learning Model with vocabulary creation using Word2Vec and tokenization, resulting in an embedding layer combined with LSTM layers, achieving 96% accuracy.

## Emotion Detection from Audio Content

Emotion detection from audio content is supported by a dataset available at [link](https://www.kaggle.com/datasets/uwrfkaggler/ravdess-emotional-speech-audio). The audio files undergo augmentation through white noise addition, audio signal shifting, stretching, and pitch shifting. Feature extraction involves zero-crossing rate, Mel-Frequency Cepstral Coefficients, root mean square, and mel spectrogram. The following models are employed:

- Architecture with Transformer Blocks - 85.32% accuracy.
- Long Short-Term Memory (LSTM) - 81.48% accuracy.
- Feedforward Neural Network (FNN) - 81.48% accuracy.

## Screenshots

<img width="1122" alt="Screenshot 2023-09-08 at 18 14 20" src="https://github.com/alexandraungureanu1/SharedJournalApp/assets/79217352/1c84aad4-b0d8-4965-a720-d9eedfd79f38">

<img width="1123" alt="Screenshot 2023-09-08 at 18 16 03" src="https://github.com/alexandraungureanu1/SharedJournalApp/assets/79217352/9af29c5e-2719-4fd5-ae70-c7c6b4144807">



