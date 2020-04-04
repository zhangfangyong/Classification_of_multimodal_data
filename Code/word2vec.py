import gensim
import numpy as np

def get_embedding_vector(sentences,embedding_model_path):
    print("loading word2vec model now...........")
    model=gensim.models.KeyedVectors.load_word2vec_format(embedding_model_path,binary=True)
    print("loading word2vec finished")
    all_sample_vector_lists=[]
    padding_embedding=np.array([0] * model.vector_size,dtype=np.float32)
    print("transform word to vector now.......")
    for sentence in sentences:
        sentence_vector = []
        for word in sentence:
            if word in model.vocab:
                sentence_vector.append(model[word])
            else:
                sentence_vector.append(padding_embedding)
        all_sample_vector_lists.append(sentence_vector)
        del sentence_vector
    print("transform word to vector finished")
    del sentences
    del model
    return all_sample_vector_lists