# RAG-on-scientific-papers
RAG system that runs on scientific papers, able to answer questions and explain complex ideas presented in the database of PDF scientifc papers. Also capable of returning the paragraphs that relates to the question and the citations mentioned in those passages.

Result Example:
```json
{"query":"how to learn bilingual mappings?"}
{
    "answer": "To learn bilingual mappings, one can utilize methods that involve creating a transformation that minimizes the distances between equivalent words in a bilingual dictionary. This approach allows for the application of the learned transformation to words that are not present in the dictionary, facilitating the induction of new translations. The process typically begins with a small bilingual dictionary, from which a mapping is learned, and this mapping can then be tested for accuracy in predicting translations of new words. Additionally, it is important to maintain monolingual invariance during the learning process to ensure the quality of both the bilingual mappings and the monolingual embeddings. Various experimental frameworks can be employed to evaluate the effectiveness of these mappings against related methods.",
    "source_passages": [
        "independently and then learn a mapping that mini-mizes the distances between equivalences listed in abilingual dictionary. The learned transformation canalso be applied to words missing in the dictionary,which can be used to induce new translations witha direct application in machine translation (Mikolovet al., 2013b; Zhao et al., 2015).The ﬁrst method to learn bilingual word em-bedding mappings was proposed by Mikolov et al.(2013b), who learn the linear transformation that",
        "tween both methods is that, while our model en-forces monolingual invariance, Faruqui and Dyer(2014) do change the monolingual embeddings tomeet this restriction. In this regard, we think thatthe restriction they add could have a negative im-pact on the learning of the bilingual mapping, andit could also degrade the quality of the monolingualembeddings. Our experiments (cf. Section 3) showempirical evidence supporting this idea.3 ExperimentsIn this section, we experimentally test the proposed",
        "also allow other applications such as sentence retrieval or cross-lingual document classiﬁcation (Kle-mentiev et al., 2012). In general, they are used as building blocks for various cross-lingual languageprocessing systems. More recently, several approaches have been proposed to learn bilingual dictio-naries mapping from the source to the target space (Mikolov et al., 2013b; Zou et al., 2013; Faruqui9Published as a conference paper at ICLR 2018",
        "In this section, we experimentally test the proposedframework and all its variants in comparison withrelated methods. For that purpose, we use the trans-lation induction task introduced by Mikolov et al.(2013b), which learns a bilingual mapping on asmall dictionary and measures its accuracy on pre-dicting the translation of new words. Unfortunately,the dataset they use is not public. For that reason,we use the English-Italian dataset on the same task",
        "10Published as a conference paper at ICLR 2018Mikel Artetxe, Gorka Labaka, and Eneko Agirre. Learning principled bilingual mappings of wordembeddings while preserving monolingual invariance. Proceedings ofEMNLP, 2016.Mikel Artetxe, Gorka Labaka, and Eneko Agirre. Learning bilingual word embeddings with (al-most) no bilingual data. In Proceedings ofthe55th Annual Meeting oftheAssociation forComputational Linguistics (V olume 1:Long Papers), pp. 451–462. Association for Computa-"
    ],
    "cited_works": [
        "Zhao et al., 2015",
        "Faruqui and Dyer(2014)",
        "Kle-mentiev et al., 2012",
        "Mikolov et al., 2013",
        "Zou et al., 2013"
    ]
}
```

## Specifications
The REST API should provide the following functionalities:

Create index;

Remove single documents from the index;

Query the index.


An answer to a query should include:

The answer;

The source passage;

A list of cited works referenced in retrieved passage, e.g. [‘Vaswani et al, 2017’, ‘Tenney et al, 2019’] in the cases (e.g. NeurIPS style) where e.g ‘[int]’ references some more metadata given in the Bibliography.

The index is made persistent between restarts and loaded into memory on startup (if it exists). Any change to the index will be persisted.

## Solution Overview
**Parsing PDF:**
PDFs are read page per page using pypdf2 library, then passed to the the recursive text splitter from langchain to get divided into small chunks, for the chunking part, we leverage the use of overlapping to not lose the context between chunks. 
When saved into FAISS index, we add metadata that includes the source of the chunk (document) as it is important later to deleted a single paper (it can also be important in case we want to filter when doing the retrieval part)

**Indexing**: 

For the indexing part, we use the pre built function included in the langchain integration of FAISS, each time we index a new document, the index is saved again to get always an updated version of the index. To embed the documents, we use a simple model from sentence transformers "sentence-transformers/all-MiniLM-L6-v2", the model can be changed directly from the config file. 
The choice is made because the model is simple, efficient and fast on local machines and does not require necessarily GPU. From the documenation of the model:

"Our model is intended to be used as a sentence and short paragraph encoder. Given an input text, it outputs a vector which captures the semantic information. The sentence vector may be used for information retrieval, clustering or sentence similarity tasks. "
Which is exactly what we need in our case. 

**Retieval part:**

For retrieval part, we use the prebuilt function from langchain to get the topk paragraphs that are relevant to the query passed by the user. The paragrahs are extarcted according to the similarity score. 

**Generation**

The topk paragraphs retrieved are then passed with the question to "gpt-4o-mini", we use a simple prompt that push the model to use the passages extracted to generate an answer for the query, we use a low temperature as we want the model to be more confident rather than more creative.

**Citations** 

To extract the citations, we use regular expression that capture the pattern of the citation from the retrieved passages.

## How to run the code:
In the .env file, put your openapi key. 
In the config file, put the values for different config variables, in our case, we use the following configuration
INDEX_FILE = 'index.faiss' \
EMBEDDING_MODEL = "sentence-transformers/ \all-MiniLM-L6-v2"
FAISS_INDEX_DIM = 384

```
python3.9 -m venv env_name
source env_name/bin/activate
pip install -r requirements.txt
python main.py
```

To test the api, you can go to localhost:8000/docs. 

## Improvements
A RAG system could be very complex, for the POC scenaio, we tried to develop something that works, generate relevant answers and shows the principle mechanisms. In different contexts; a lot of improvements could be added. 

**Improving parsing part** \
PDF files are very complex and could be hard to parse as they contain structured and unstructured data, figures, tables, titles, subtitles, images etc. Relying only on the text leads to missing some information, to improve the parsing part, we can use an OCR system as it can be more efficient. 

**Improving inedxing part** \
To improve the indexing part, we can use different models that are more commplex than the one used in our case but guarantees better results for the retrieving part. 

**Improving generation part** \
Trying different prompts and setting an evaluation system for a set of questions could be interesting to push the generative llm to its limits. 

**Improving citation extraction part** \
Using only regular expression can be a bit tricky, to improve the extraction part, we can use more sophisticated solutions, we can think for example of using a QA model that extracts the 