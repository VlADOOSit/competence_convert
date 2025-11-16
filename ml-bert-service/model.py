import numpy as np
import torch
from transformers import BertTokenizer, BertModel, AutoModelForSequenceClassification
from preprocess import preprocess_text

class BertEmbeddingModel:
    def __init__(self, model_name: str = "bert-base-uncased", device: str = None):
        self.device = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()

    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output.last_hidden_state  
        mask = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        summed = torch.sum(token_embeddings * mask, dim=1)
        counts = torch.clamp(mask.sum(dim=1), min=1e-9)
        return summed / counts

    def embed(self, text: str):
        text = preprocess_text(text)
        encoded = self.tokenizer(text, padding=True, truncation=True, max_length=256, return_tensors="pt")
        encoded = {k: v.to(self.device) for k, v in encoded.items()}
        with torch.no_grad():
            output = self.model(**encoded)
        emb = self.mean_pooling(output, encoded["attention_mask"]) 
        return emb.cpu().numpy().reshape(-1)  

    def embed_batch(self, texts):
        processed = [preprocess_text(t) for t in texts]
        encoded = self.tokenizer(processed, padding=True, truncation=True, max_length=256, return_tensors="pt")
        encoded = {k: v.to(self.device) for k, v in encoded.items()}
        with torch.no_grad():
            output = self.model(**encoded)
        emb = self.mean_pooling(output, encoded["attention_mask"])  # (n, dim)
        return emb.cpu().numpy()
    
    def load_finetuned(self, path: str = "models/fine_tuned_bert"):
        try:
            self.classifier_tokenizer = BertTokenizer.from_pretrained(path)
            self.classifier = AutoModelForSequenceClassification.from_pretrained(path)
            self.classifier.to(self.device)
            self.classifier.eval()
            return True
        except Exception as e:
            print(f"[WARN] Cannot load fine-tuned model from {path}: {e}")
            return False

    def predict_with_classifier(self, texts):
        if self.classifier is None or self.classifier_tokenizer is None:
            raise RuntimeError("Fine-tuned classifier is not loaded")

        processed = [preprocess_text(t) for t in texts]
        enc = self.classifier_tokenizer(
            processed,
            padding=True,
            truncation=True,
            max_length=256,
            return_tensors="pt"
        )
        enc = {k: v.to(self.device) for k, v in enc.items()}
        with torch.no_grad():
            out = self.classifier(**enc)
        logits = out.logits.cpu().numpy()  # shape (N, 1)
        return logits

