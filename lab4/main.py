from keras.utils import to_categorical

from dataloader import load_dataset, dataset2dataloader
from models import SimpleNMT
from torch import optim
import torch.nn as nn
import torch
import numpy as np
from pprint import pprint
from tqdm import tqdm

if __name__ == "__main__":
    epoch = 500
    learning_rate = 0.001
    hidden_size = 64
    batch_size = 10

    train_iter, val_iter, source_vocab, target_vocab = dataset2dataloader(dataset_path=r"../dataset/date-normalization",
                                                                          batch_size=batch_size, dataset_size=10000, debug=True)
    source_vocab_size = len(source_vocab.stoi)
    target_vocab_size = len(target_vocab.stoi)

    Tx, Ty = 25, 10  

    model = SimpleNMT(in_vocab_size=source_vocab_size, out_vocab_size=target_vocab_size, in_hidden_size=hidden_size,
                      out_hidden_size=hidden_size, output_size=target_vocab_size, with_attention=True)

    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    criterion = nn.CrossEntropyLoss()

    embed_layer1 = nn.Embedding(source_vocab_size, source_vocab_size,
                                _weight=torch.from_numpy(np.eye(source_vocab_size)))
    embed_layer2 = nn.Embedding(target_vocab_size, target_vocab_size,
                                _weight=torch.from_numpy(np.eye(target_vocab_size)))

    model.train()
    for ep in range(epoch):
        epoch_loss = 0
        for batch in train_iter:
            optimizer.zero_grad()
            Xin, Yin, Yout = batch.source.t().long(), batch.target.t()[:, :-1].long(), batch.target.t()[:, 1:]
            batch_size = len(Xin)
            init_hidden = torch.zeros(1, batch_size, hidden_size)
            Xin = embed_layer1(Xin).float()
            Yin = embed_layer2(Yin).float()
            logits = model(Xin, init_hidden, Yin)
            loss = criterion(logits.view(-1, logits.shape[-1]), Yout.flatten())
            epoch_loss += loss.item()
            loss.backward()
            optimizer.step()
        if ep % (epoch // 10) == 0:
            print("loss", epoch_loss)

    sents_for_large = ["monday may 7 1983", "19 march 1998", "18 jul 2008", "9/10/70", "thursday january 1 1981",
                       "thursday january 26 2015", "saturday april 18 1990", "sunday may 12 1988"]
    sents = ["monday march 7 1983", "9 may 1998", "thursday january 26 1995", "9/10/70"]


    def translate(model, sents):
        X = []
        for sent in sents:
            X.append(list(map(lambda x: source_vocab[x], list(sent))) + [source_vocab["<pad>"]] * (Tx - len(sent)))
        Xoh = torch.from_numpy(np.array(list(map(lambda x: to_categorical(x, num_classes=source_vocab_size), X))))
        encoder_init_hidden = torch.zeros(1, len(X), hidden_size)
        preds = model(Xoh, encoder_init_hidden, decoder_input=None, out_word2index=target_vocab.stoi,
                      out_index2word=target_vocab.itos, max_len=Ty, out_size=target_vocab_size)
        for gold, pred in zip(sents, preds):
            print(gold, "-->", "".join(pred))


    translate(model, sents)

