'''Make a parser using regex.

Let's see how this goes...
'''

import re

class Parser(object):
    '''Parse XProtocol.'''

    def __init__(self):
        self.cur_token = ''
        self.cur_rule = []
        self.pstack = []

        # Regex for tokens
        self.rtoks = {}
        self.rtoks['TAG'] = re.compile(r'<(\w)*.?\"?(\w)*\"?>')
        self.rtoks['STRING'] = re.compile(r'\"(.*)\"')

        self.tokens = [
            'TAG', 'STRING'
        ]
        self.grammar = {
            'TAG': ['TAG'],
            # 'TAG': ['TAG', 'STRING']
        }
        self.inverse_grammar = dict(
            ('.'.join(v), k) for k, v in self.grammar.items())

    def istoken(self):
        '''Check to see if cur_token is a token.'''
        for tok in self.tokens:
            match = self.rtoks[tok].match(self.cur_token)
            if match:
                return tok
        return False

    def isrule(self):
        '''Check to see if cur_rule is a rule.'''
        return '.'.join(self.cur_rule) in self.inverse_grammar

    def isconsistent(self):
        '''Make sure cur_rule is a subset of some rule.'''
        # Doesn't do anything right now
        return True

    def parse(self, buf):
        '''Parse buffer into dictionary.'''
        config = dict()

        self.cur_token = ''
        self.cur_rule = []
        for c in buf:

            # Check to see if cur_token is a token
            tok = self.istoken()
            if tok:
                self.cur_rule.append(tok)
                print(self.cur_token)
                self.cur_token = ''

                # Check to see if cur_rule is a rule
                # print(self.cur_rule)
                if self.isrule():
                    self.cur_rule = []

                # At least make sure we're being consistent
            elif not self.isconsistent():
                raise ValueError('XProtocol does not conform to grammar!')

            # Skip whitespace
            if c.isspace():
                continue

            # If we get an open brace, then we need to go up a level in the
            # dictionary, if close, then step back down
            if c == '{':
                self.pstack.append('{')
                continue
            elif c == '}':
                # print(self.pstack)
                self.pstack.pop()
                continue

            # Continue building token
            self.cur_token += c

        return config


config = dict()
cur_token = ''
valid_toks = []
with open('mr_utils/tests/load_data/config_buffer.xprot') as f:
    buf = f.read()
    parser = Parser()
    config = parser.parse(buf)
