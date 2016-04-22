import json
import time

import metapy
import pytoml

from json_tree_visitor import JSONTreeVisitor

class NLP:
    """
    Wraps the MeTA tagger and parser.
    """
    json_tree_visitor = JSONTreeVisitor()

    def __init__(self, cfg):
        """
        Load MeTA's filter chain, tagger, and parser.
        """
        toml = pytoml.loads(open(cfg).read())
        self.tgr = metapy.sequence.PerceptronTagger(toml['sequence']['prefix'])
        self.psr = metapy.parser.Parser(toml['parser']['prefix'])
        self.stream = metapy.analyzers.ICUTokenizer()
        self.stream = metapy.analyzers.PennTreebankNormalizer(self.stream)

    def run(self, request):
        """
        Run MeTA's NLP tools on the request text.
        """
        start = time.time()
        text = request['text']
        response = {'text': text, 'sentences': []}
        self.stream.set_content(text)
        sequences = []
        seq = metapy.sequence.Sequence()
        for token in self.stream:
            if token == '<s>':
                seq = metapy.sequence.Sequence()
            elif token == '</s>':
                self.tgr.tag(seq)
                tree = self.psr.parse(seq)
                response['sentences'].append(self.to_obj(seq, tree))
            else:
                seq.add_symbol(token)

        response['elapsed_time'] = time.time() - start
        return json.dumps(response, indent=2)

    @classmethod
    def to_obj(cls, seq, tree):
        """
        Convert MeTA's NLP objects to JSON objects.
        """
        obj = {'tagged': [], 'tokenized': ''}
        for elem in seq:
            obj['tokenized'] += elem.symbol + ' '
            obj['tagged'].append({'word': elem.symbol, 'tag': elem.tag})
        obj['json-tree'] = tree.visit(cls.json_tree_visitor)
        return obj
