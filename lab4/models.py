import torch.nn as nn
import torch
import numpy as np
import torch.nn.functional as F


class EncoderRNN(nn.Module):
    def __init__(self, vocab_size, hidden_size, dropout=0.5):
        super().__init__()
        self.hidden_size = hidden_size
        self.gru = nn.GRU(vocab_size, hidden_size, dropout=dropout, batch_first=True)

    def forward(self, x, init_hidden):
        seq_output, last_state = self.gru(x, init_hidden)
        return seq_output, last_state


class DecoderRNN(nn.Module):
    def __init__(self, vocab_size, hidden_size, output_size, dropout=0.5):
        super().__init__()
        self.hidden_size = hidden_size
        self.gru = nn.GRU(vocab_size, hidden_size, dropout=dropout, batch_first=True)
        self.hidden2index = nn.Linear(hidden_size, output_size)

    def forward(self, x, init_state):
        seq_output, last_state = self.gru(x, init_state)
        seq_output = self.hidden2index(seq_output)
        return seq_output, last_state


class DecoderAttenRNN(nn.Module):
    def __init__(self, vocab_size, hidden_size, output_size, dropout=0.5):
        super().__init__()
        self.hidden_size = hidden_size
        self.gru = nn.GRU(vocab_size, hidden_size, dropout=dropout, batch_first=True)
        self.hidden2label = nn.Linear(hidden_size, output_size)
        self.atten_affine = nn.Linear(hidden_size*2, hidden_size)

    def get_alpha(self, hi, encoder_output):
        hi = hi.permute(1, 2, 0)  
        e = torch.bmm(encoder_output, hi).squeeze(2)  
        e = F.softmax(e, dim=1).unsqueeze(2)       
        alpha = (e * encoder_output).sum(dim=1)   

        return alpha

    def forward(self, x, init_state, seq_encoder_output):
        batch_size, max_len, _ = x.shape 
        hi = init_state
        seq_decoder_output = []
        for i in range(max_len):
            alpha = self.get_alpha(hi, seq_encoder_output) 
            hi = torch.cat([alpha.unsqueeze(0), hi], dim=2)
            hi = self.atten_affine(hi)
            output, hi = self.gru(x[:, i, :].unsqueeze(1), hi)
            seq_output = self.hidden2label(output.squeeze(1))
            seq_decoder_output.append(seq_output.squeeze(1))
        seq_decoder_output = torch.stack(seq_decoder_output, dim=1)
        return seq_decoder_output, hi


class SimpleNMT(nn.Module):
    def __init__(self, in_vocab_size, out_vocab_size, in_hidden_size, out_hidden_size, output_size, with_attention=False):
        super().__init__()
        self.with_attention = with_attention
        self.encoder = EncoderRNN(in_vocab_size, in_hidden_size)
        if self.with_attention:
            self.decoder = DecoderAttenRNN(out_vocab_size, out_hidden_size, output_size)
        else:
            self.decoder = DecoderRNN(out_vocab_size, out_hidden_size, output_size)

    def forward(self, encoder_input, encoder_init_hidden, decoder_input=None, out_word2index=None, out_index2word=None,
                max_len=None, out_size=None):
        encoder_seq_output, encoder_last_state = self.encoder(encoder_input, encoder_init_hidden)
        if decoder_input is not None:
            if self.with_attention:
                logits, _ = self.decoder(decoder_input, encoder_last_state, encoder_seq_output)
            else:
                logits, _ = self.decoder(decoder_input, encoder_last_state)
            return logits
        else:
            decoded_sents = []
            for i in range(len(encoder_input)):
                sent = []
                decoder_input = torch.FloatTensor(np.eye(out_size)[[out_word2index["<start>"]]]).unsqueeze(0)
                hi = encoder_last_state[:, i, :].unsqueeze(1)
                for di in range(max_len):
                    if self.with_attention:
                        decoder_output, hdi = self.decoder(decoder_input, hi, encoder_seq_output[i, :, :].unsqueeze(0))
                    else:
                        decoder_output, hdi = self.decoder(decoder_input, hi)
                    topv, topi = decoder_output.data.topk(1)
                    topi = topi.item()
                    if topi == out_word2index["<end>"]:
                        break
                    else:
                        sent.append(out_index2word[topi])
                    decoder_input = torch.FloatTensor([np.eye(out_size)[topi]]).unsqueeze(0)
                    hi = hdi
                decoded_sents.append(sent)
            return decoded_sents



