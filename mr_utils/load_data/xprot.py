import ply.lex as lex
import ply.yacc as yacc
import xml.etree.ElementTree as ET

class XProtLex(object):
    # List of token names
    tokens = (
        'RANGLE',
        'LANGLE',
        'PERIOD',
        'RBRACE',
        'LBRACE',
        'STRING',
        'INTEGER',
        'FLOAT',
        'HEX',
        'SCINOT',

        'XPROT',
        'PMAP',
        'PSTR',
        'PLNG',
        'PDBL',
        'PBOOL',
        'PARRAY',
        'PFUNCT',
        'PCHOICE',
        'PCARDLAYOUT',
        'PIPE',
        'PIPESERVICE',
        'EVENT',
        'CONN',
        'METHOD',
        'DEPEND',
        'PROTCOMP',
        'NAME',
        'EVASTRTAB',
        'COMMENT',

        # modifiers
        'DEFAULT',
        'CLASS',
        'PRECISION',
        'MINSIZE',
        'MAXSIZE',
        'LABEL',
        'TOOLTIP',
        'LIMRANGE',
        'LIMIT',
        'REPR',
        'POS',
        'PARAM',
        'CONTROL',
        'LINE',
        'DLL',
        'CONTEXT',
        'ID',
        'USERVERSION',
        'INFILE',
        'VISIBLE',
        'COM',
        'UNIT',

        # There are major divisions, we achieve this with modifiers
        'DICOM',
        'MEAS',
        'MEASYAPS',
        'PHOENIX',
        'SPICE',

        # one liners
        'LEFTHAND'
    )


    # Regular expression rules for simple tokens
    t_LANGLE = r'<'
    t_RANGLE = r'>'
    t_PERIOD = r'\.'
    t_LBRACE = r'{'
    t_RBRACE = r'}'
    t_XPROT = r'XProtocol'
    t_PMAP = r'ParamMap'
    t_PSTR = r'ParamString'
    t_PLNG = r'ParamLong'
    t_PDBL = r'ParamDouble'
    t_PBOOL = r'ParamBool'
    t_PARRAY = r'ParamArray'
    t_PFUNCT = r'ParamFunctor'
    t_PCHOICE = r'ParamChoice'
    t_PCARDLAYOUT = r'ParamCardLayout'
    t_PIPE = r'Pipe'
    t_PIPESERVICE = r'PipeService'
    t_EVENT = r'Event'
    t_CONN = r'Connection'
    t_METHOD = r'Method'
    t_DEPEND = r'Dependency'
    t_PROTCOMP = r'ProtocolComposer'
    t_NAME = r'Name'
    t_EVASTRTAB = r'EVAStringTable'
    t_STRING = r'\"(.|\n)*?\"'
    t_INTEGER = r'-?\d+'
    t_FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
    t_HEX = r'0x[\dabcdef]+'
    t_SCINOT = r'([+-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+))'
    t_DEFAULT = r'Default'
    t_CLASS = r'Class'
    t_PRECISION = r'Precision'
    t_MINSIZE = r'MinSize'
    t_MAXSIZE = r'MaxSize'
    t_LABEL = r'Label'
    t_TOOLTIP = r'Tooltip'
    t_LIMRANGE = r'LimitRange'
    t_LIMIT = r'Limit'
    t_POS = r'Pos'
    t_PARAM = r'Param'
    t_REPR = r'Repr'
    t_CONTROL = r'Control'
    t_LINE = r'Line'
    t_DLL = r'Dll'
    t_CONTEXT = r'Context'
    t_ID = r'ID'
    t_USERVERSION = r'Userversion'
    t_INFILE = r'InFile'
    t_VISIBLE = r'Visible'
    t_COM = r'Comment'
    t_UNIT = r'Unit'

    t_DICOM = r'Dicom'
    t_MEAS = r'Meas'
    t_MEASYAPS = r'MeasYaps'
    t_PHOENIX = r'Phoenix'
    t_SPICE = r'Spice'

    def t_LEFTHAND(t):
         r'[a-zA-Z\[\]0-9\. _]+='
         # remove the equal sign at the end
         t.value = t.value[:-1].rstrip()
         return(t)

    # Comments are ignored
    def t_COMMENT(t):
        r'\#.*'
        pass

    # Define a rule so we can track line numbers
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters
    t_ignore = ' \t'

    # Error handling rule
    def t_error(t):
        print('Illegal character %s on line %s' % (t.value[0],t.lexer.lineno))
        t.lexer.skip(1)

    # Build the lexer
    lexer = lex.lex()


class XProtParser(object):

    # make a stack of the brace state
    brace_state = []

    xml = ''
    node_label = ''
    name = ''
    mod = ''

    def raw2xml(self,xprot):
        class Node:
            def __init__(self):
                self.tag = ''
                self.attr = dict()

            def makeAttrs(self):
                innards = ''
                for key,val in self.attr.items():
                    innards += ' ' + key + '=' + val
                return(innards)

            def openString(self):
                return('<' + self.tag + self.makeAttrs() + '>')

            def closeString(self):
                return('</' + self.tag + '>')

        # escape invalid xml entities
        def xml_clean(string):
            return(string.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;'))


        def p_document(p):
            '''document : document line
                                | line'''

        def p_modifier(p):
            '''modifier : DEFAULT
                        | CLASS
                        | PRECISION
                        | MINSIZE
                        | MAXSIZE
                        | LABEL
                        | TOOLTIP
                        | LIMRANGE
                        | LIMIT
                        | REPR
                        | POS
                        | PARAM
                        | CONTROL
                        | LINE
                        | DLL
                        | CONTEXT
                        | NAME
                        | ID
                        | USERVERSION
                        | INFILE
                        | VISIBLE
                        | COM
                        | UNIT

                        | DICOM
                        | MEAS
                        | MEASYAPS
                        | PHOENIX
                        | SPICE'''

            self.mod = '"' + p[1] + '"'

        def p_line(p):
            '''line : tag LBRACE

                    | LANGLE modifier RANGLE tag LBRACE
                    | LANGLE modifier RANGLE LBRACE
                    | LBRACE
                    | RBRACE

                    | STRING
                    | INTEGER
                    | FLOAT

                    | LANGLE modifier RANGLE STRING
                    | LANGLE modifier RANGLE INTEGER
                    | LANGLE modifier RANGLE FLOAT

                    | LEFTHAND
                    | LANGLE modifier RANGLE LEFTHAND
                    | HEX
                    | SCINOT'''

            if len(p) is 3:
                # This means we have an open brace
                self.brace_state.append((p[2],self.node_label))

                n = Node()
                n.tag = self.node_label

                if self.name != '':
                    n.attr['name'] = self.name
                    self.name = ''
                if self.mod != '':
                    n.attr['mod'] = self.mod
                    self.mod = ''
                self.xml += n.openString()

            else:
                # This means we might have close brace
                if p[1] == '}':
                    try:
                        tag_name = self.brace_state.pop()
                        n = Node()
                        n.tag = tag_name[1]
                        self.xml += n.closeString()
                    except:
                        pass

                elif p[1] == '{':
                    # we got another open brace
                    self.brace_state.append((p[1],'InducedBrace'))

                    n = Node()
                    n.tag = 'InducedBrace'
                    self.xml += n.openString()
                else:
                    # This is the value of the tag
                    n = Node()
                    n.tag = 'value'

                    if p[1] == '<':
                        n.attr['mod'] = self.mod
                        self.mod = ''

                        if p[4] is None:
                            n.tag = self.node_label
                            self.brace_state.append((p[5],self.node_label))
                            self.xml += n.openString()
                        else:
                            self.xml += n.openString() + xml_clean(p[4]) + n.closeString()
                            # self.xml += n.openString() + p[4] + n.closeString()
                    else:
                        self.xml += n.openString() + xml_clean(p[1]) + n.closeString()
                        # self.xml += n.openString() + p[1] + n.closeString()


        def p_tag(p):
            '''tag : LANGLE tagtype PERIOD STRING RANGLE
                    | LANGLE tagtype RANGLE'''

            if len(p) > 4:
                if self.node_label != '':
                    self.name = p[4]


        def p_tagtype(p):
            '''tagtype : PMAP
                    | PSTR
                    | PLNG
                    | PDBL
                    | PBOOL
                    | PARRAY
                    | PFUNCT
                    | PCHOICE
                    | PCARDLAYOUT
                    | PIPE
                    | PIPESERVICE
                    | EVENT
                    | CONN
                    | METHOD
                    | DEPEND
                    | PROTCOMP
                    | EVASTRTAB
                    | XPROT'''

            self.node_label = p[1]

        # Error rule for syntax errors
        def p_error(p):
            print('Syntax error in input!')
            print(p)

        # get the lexer and token mappings to pass to yacc
        xprotLex = XProtLex()
        lexer = xprotLex.lexer
        tokens = xprotLex.tokens

        # Build the parser
        parser = yacc.yacc()

        # load in the data
        result = parser.parse(xprot)

        # Check to make sure all our braces matched up
        if len(self.brace_state) > 0:
            print('Mismatched Braces!')

        # Give xml document a common parent
        self.xml = '<doc_root>' + self.xml + '</doc_root>'


        # print('Found Version', self.xml.find('Version'))
        # print(self.xml.find('sWipMemBlock'))

        # Parse the string to make sure XML is well formed
        # try:
        # print(self.xml)
        root = ET.fromstring(self.xml)
        return(root)
        # except:
            # return(-1)
