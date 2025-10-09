import torch.nn as nn

class TextClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, num_classes):
        super(TextClassifier, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)  #turns vocab id into dense vector
        #self.embedding = nn.Embedding.from_pretrained(embedding_matrix, freeze=False)
        self.fc = nn.Linear(embed_dim, num_classes) # input is average embedding of a sentence and output is num_classes(2)cwhich is buy or sell
    
    def forward(self, x):
        # x = (batch size, seq len)
        embedded = self.embedding(x) # gives us original output and embed_dim
        pooling = embedded.mean(dim = 1) # average embedding across all words in teh sentence, used to get one vec per sentence
        output = self.fc(pooling) # passes vector into classifier
        return output