import os
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification
from torch.optim import AdamW

from .dataset_builder import build_training_pairs
from .schema import FineTuneSample


class RegressionDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        enc = {key: val[idx] for key, val in self.encodings.items()}
        enc["labels"] = torch.tensor(self.labels[idx], dtype=torch.float)
        return enc

    def __len__(self):
        return len(self.labels)


def run_finetuning(samples: list[FineTuneSample], output_dir="models/fine_tuned_bert"):
    texts, labels = build_training_pairs(samples)

    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    encodings = tokenizer(texts, truncation=True, padding=True)

    dataset = RegressionDataset(encodings, labels)
    dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

    model = BertForSequenceClassification.from_pretrained(
        "bert-base-uncased",
        num_labels=1   # regression
    )

    optim = AdamW(model.parameters(), lr=5e-5)

    model.train()
    for epoch in range(2):
        for batch in dataloader:
            optim.zero_grad()
            outputs = model(**batch)
            loss = outputs.loss
            loss.backward()
            optim.step()
            print("loss:", loss.item())

    os.makedirs(output_dir, exist_ok=True)
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)

    return {
        "status": "ok",
        "saved_to": output_dir
    }
