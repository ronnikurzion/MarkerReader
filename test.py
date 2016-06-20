import os, sys, cPickle
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from ddlite import *

class PubMedAbstractReader(HTMLReader):
    def _cleaner(self, s):
        return (s.parent.name == 'abstracttext')

dp = DocParser('examples/gene_tag_example/data/', PubMedAbstractReader())

docs = list(dp.readDocs())
docs = None


pkl_f = 'examples/gene_tag_example/gene_tag_saved_sents_v5.pkl'

try:

    with open(pkl_f, 'rb') as f:

        sents = cPickle.load(f)
except:

    sents = dp.parseDocSentences()
    with open(pkl_f, 'w+') as f:

        cPickle.dump(sents, f)

# Schema is: ENSEMBL_ID | NAME | TYPE (refseq, canonical, non-canonical)
genes = [line.rstrip().split('\t')[1] for line in open('examples/gene_tag_example/dicts/ensembl_genes.tsv')]
genes = filter(lambda g : len(g) > 2, genes)

gene_dm = DictionaryMatch(label='GeneName', dictionary=genes, ignore_case=False)
noun_regex = RegexNgramMatch(label='Nouns', regex_pattern=r'[A-Z]?NN[A-Z]?', ignore_case=True, match_attrib='poses')
up_regex = RegexFilterAll(noun_regex, label='Upper', regex_pattern=r'[A-Z]+([0-9]+)?([A-Z]+)?([0-9]+)?$', ignore_case=False, match_attrib='words')
multi_regex = RegexFilterAll(up_regex, label='Multi', regex_pattern=r'[a-z0-9]{3,}', ignore_case=True)
CE = Union(gene_dm, multi_regex)
E = Entities(sents, CE)
E[0].render()
E.dump_candidates('examples/gene_tag_example/gene_tag_saved_entities_v6.pkl')

print sents[0]