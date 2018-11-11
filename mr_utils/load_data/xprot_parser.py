import ply.lex as lex
import ply.yacc as yacc
import json

class XProtLexer(object):

    tokens = (
        'RANGLE','LANGLE','LBRACE','RBRACE','PERIOD',

        'XPROT','NAME','ID','USERVERSION','EVASTRTAB','PARAMCARDLAYOUT','REPR',
        'CONTROL','PARAM','POS','DEPENDENCY','DLL','CONTEXT','VISIBLE',
        'PROTOCOLCOMPOSER','INFILE','PARAMMAP','PARAMSTRING','PARAMLONG',
        'PARAMBOOL','PARAMCHOICE','PARAMDOUBLE','PARAMARRAY',

        'LIMITRANGE','DEFAULT','MINSIZE','MAXSIZE','LIMIT','PRECISION',

        'QUOTED_STRING','INTEGER','FLOAT',

        # 'ID',
        # '',
        # '',
        #
        # 'OPEN_PARAM_MAP',
        #
        # 'INTEGER',
        # 'REST_OF_LINE',

    )

    # Regular expression rules for simple tokens
    t_LANGLE = r'<'
    t_RANGLE = r'>'
    t_LBRACE = r'{'
    t_RBRACE = r'}'
    t_PERIOD = r'\.'

    t_XPROT = r'XProtocol'
    t_NAME = r'Name'
    t_ID = r'ID'
    t_USERVERSION = r'Userversion'
    t_EVASTRTAB = r'EVAStringTable'
    t_PARAMCARDLAYOUT = r'ParamCardLayout'
    t_REPR = r'Repr'
    t_CONTROL = r'Control'
    t_PARAM = r'Param'
    t_POS = r'Pos'
    t_DEPENDENCY = r'Dependency'
    t_DLL = r'Dll'
    t_CONTEXT = r'Context'
    t_VISIBLE = r'Visible'
    t_PROTOCOLCOMPOSER = r'ProtocolComposer'
    t_INFILE = r'InFile'
    t_PARAMMAP = r'ParamMap'
    t_PARAMSTRING = r'ParamString'
    t_PARAMLONG = r'ParamLong'
    t_PARAMBOOL = r'ParamBool'
    t_PARAMCHOICE = r'ParamChoice'
    t_PARAMDOUBLE = r'ParamDouble'
    t_PARAMARRAY = r'ParamArray'

    t_LIMITRANGE = r'LimitRange'
    t_DEFAULT = r'Default'
    t_MINSIZE = r'MinSize'
    t_MAXSIZE = r'MaxSize'
    t_LIMIT = r'Limit'
    t_PRECISION = r'Precision'

    t_QUOTED_STRING = r'\"(.|\n)*?\"'
    t_INTEGER = r'-?\d+'
    t_FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'

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
        # print('Illegal character %s on line %s' % (t.value[0],t.lexer.lineno))
        t.lexer.skip(1)

    # Build the lexer
    lexer = lex.lex()



class XProtParser(object):

    def __init__(self):
        self.structure = {}
        self.structure['XProtocol'] = {}
        self.structure['XProtocol']['EVAStringTable'] = []
        self.structure['XProtocol']['ParamCardLayout'] = []
        self.structure['XProtocol']['Dependency'] = {}
        self.structure['XProtocol']['ProtocolComposer'] = {}

        # Helpers
        self.control = None
        self.dependency = None
        self.dependency_key = None
        self.stringlist = []
        self.protcomposers = []

    def parse(self,xprot):

        def p_document(p):
            '''document : LANGLE XPROT RANGLE LBRACE xprotocol RBRACE'''

        def p_xprotocol(p):
            '''xprotocol : name id userversion evastringtable parammap paramcardlayout dependencies protocolcomposers'''

        def p_name(p):
            '''name : LANGLE NAME RANGLE QUOTED_STRING'''
            self.structure['XProtocol']['Name'] = p[4]

        def p_id(p):
            '''id : LANGLE ID RANGLE INTEGER'''
            self.structure['XProtocol']['ID'] = p[4]

        def p_userversion(p):
            '''userversion : LANGLE USERVERSION RANGLE FLOAT'''
            self.structure['XProtocol']['Userversion'] = p[4]

        def p_evastringtable(p):
            '''evastringtable : LANGLE EVASTRTAB RANGLE LBRACE evastrtablecontents RBRACE'''

        def p_evastrtablecontents(p):
            '''evastrtablecontents : evastrtableline evastrtablecontents
            | empty'''

        def p_evastrtableline(p):
            '''evastrtableline : INTEGER QUOTED_STRING
            | INTEGER'''
            if len(p) == 3:
                self.structure['XProtocol']['EVAStringTable'].append({ p[1]: p[2] })
            elif len(p) == 2:
                self.structure['XProtocol']['EVAStringTable'].append({ p[1]: None })

        def p_paramcardlayout(p):
            '''paramcardlayout : LANGLE PARAMCARDLAYOUT PERIOD QUOTED_STRING RANGLE LBRACE paramcardlayoutcontents RBRACE'''
            # Make the QUOTED_STRING the parent so we can look it up easily
            self.structure['XProtocol']['ParamCardLayout'] = { p[4]: self.structure['XProtocol']['ParamCardLayout'] }

        def p_paramcardlayoutcontents(p):
            '''paramcardlayoutcontents : paramcardlayoutline paramcardlayoutcontents
            | empty'''

        def p_paramcardlayoutline(p):
            '''paramcardlayoutline : LANGLE REPR RANGLE QUOTED_STRING
            | LANGLE CONTROL RANGLE LBRACE controlinnards RBRACE'''

            if self.control is not None:
                self.structure['XProtocol']['ParamCardLayout'].append(self.control)
                self.control = None
            else:
                self.structure['XProtocol']['ParamCardLayout'].append({'Repr': p[4]})

        def p_controlinnards(p):
            '''controlinnards : LANGLE PARAM RANGLE QUOTED_STRING LANGLE POS RANGLE INTEGER INTEGER LANGLE REPR RANGLE QUOTED_STRING
            | LANGLE PARAM RANGLE QUOTED_STRING LANGLE POS RANGLE INTEGER INTEGER'''
            if len(p) == 14:
                self.control = ('Control', { 'Param': p[4], 'Pos': (p[8],p[9]), 'Repr': p[13] })
            else:
                self.control = ('Control', { 'Param': p[4], 'Pos': (p[8],p[9]) })

        def p_dependencies(p):
            '''dependencies : dependencies dependency
            | empty'''
            if len(p) == 3:
                self.structure['XProtocol']['Dependency'][self.dependency_key] = self.dependency
                self.dependency_key = None
                self.dependency = None
                self.stringlist = []

        def p_dependency(p):
            '''dependency : LANGLE DEPENDENCY PERIOD QUOTED_STRING RANGLE LBRACE dependencyinnards RBRACE'''
            self.dependency_key = p[4]

        def p_dependencyinnards(p):
            '''dependencyinnards : listofquotedstrings LANGLE DLL RANGLE QUOTED_STRING LANGLE CONTEXT RANGLE QUOTED_STRING LANGLE CONTEXT RANGLE QUOTED_STRING
            | listofquotedstrings LANGLE DLL RANGLE QUOTED_STRING LANGLE CONTEXT RANGLE QUOTED_STRING
            | listofquotedstrings LANGLE DLL RANGLE QUOTED_STRING
            | listofquotedstrings LANGLE CONTEXT RANGLE QUOTED_STRING
            | listofquotedstrings LANGLE VISIBLE RANGLE QUOTED_STRING
            | listofquotedstrings'''
            if len(p) > 10:
                ## TODO: Seems like there could be multiple of each...
                self.dependency = { 'string_list': self.stringlist, 'Dll': p[5], 'Context': (p[9],p[13]) }
            elif len(p) == 10:
                self.dependency = { 'string_list': self.stringlist, 'Dll': p[5], 'Context': p[9] }
            elif len(p) == 6:
                # Either Context, DLL, or Visible, singly
                self.dependency = { 'string_list': self.stringlist, p[3]: p[5] }

        def p_listofquotedstrings(p):
            '''listofquotedstrings : QUOTED_STRING listofquotedstrings
            | empty'''
            if len(p) == 3:
                self.stringlist.append(p[1])

        def p_protocolcomposers(p):
            '''protocolcomposers : protocolcomposer protocolcomposers
            | empty'''

        def p_protocolcomposer(p):
            '''protocolcomposer : LANGLE PROTOCOLCOMPOSER PERIOD QUOTED_STRING RANGLE LBRACE protocolcomposercontents RBRACE'''
            self.structure['XProtocol']['ProtocolComposer'][p[4]] = self.protcomposers
            self.protcomposers = []

        def p_protocolcomposercontents(p):
            '''protocolcomposercontents : protocolcomposercontents LANGLE INFILE RANGLE QUOTED_STRING
            | protocolcomposercontents LANGLE DLL RANGLE QUOTED_STRING
            | empty'''
            if len(p) == 6:
                self.protcomposers.append({ p[3]: p[5] })

        def p_parammap(p):
            '''parammap : LANGLE PARAMMAP PERIOD QUOTED_STRING RANGLE LBRACE paramsorvalues RBRACE'''
            self.stringlist = []

        def p_paramstring(p):
            '''paramstring : LANGLE PARAMSTRING PERIOD QUOTED_STRING RANGLE LBRACE paramsorvalues RBRACE'''

        def p_paramlong(p):
            '''paramlong : LANGLE PARAMLONG PERIOD QUOTED_STRING RANGLE LBRACE paramsorvalues RBRACE'''

        def p_parambool(p):
            '''parambool : LANGLE PARAMBOOL PERIOD QUOTED_STRING RANGLE LBRACE paramsorvalues RBRACE'''

        def p_paramchoice(p):
            '''paramchoice : LANGLE PARAMCHOICE PERIOD QUOTED_STRING RANGLE LBRACE paramsorvalues RBRACE'''

        def p_paramdouble(p):
            '''paramdouble : LANGLE PARAMDOUBLE PERIOD QUOTED_STRING RANGLE LBRACE paramsorvalues RBRACE'''

        def p_paramarray(p):
            '''paramarray : LANGLE PARAMARRAY PERIOD QUOTED_STRING RANGLE LBRACE paramsorvalues RBRACE'''

        def p_paramsorvalues(p):
            '''paramsorvalues : tag param paramsorvalues
            | param paramsorvalues
            | value paramsorvalues
            | empty'''

        def p_param(p):
            '''param : parammap
            | paramstring
            | paramlong
            | parambool
            | paramchoice
            | paramdouble
            | paramarray'''

        def p_value(p):
            '''value : tag_empty INTEGER
            | tag_empty QUOTED_STRING
            | tag_empty LBRACE listofquotedstrings RBRACE
            | tag_empty FLOAT'''

        def p_tag(p):
            '''tag : LANGLE DEFAULT RANGLE
            | LANGLE LIMITRANGE RANGLE
            | LANGLE MINSIZE RANGLE
            | LANGLE MAXSIZE RANGLE
            | LANGLE LIMIT RANGLE
            | LANGLE PRECISION RANGLE'''

        def p_tag_empty(p):
            '''tag_empty : tag
            | empty'''


    	# param_array
    	# node
    	# param_generic
    	# quoted_string
    	# array_value
    	# burn_properties
    	# burn_param_card_layout
    	# burn_dependency
    	# burn_protocol_composer
    	# strict_double


        def p_empty(p):
            '''empty : '''
            pass

        # Error rule for syntax errors
        def p_error(p):
            print('Syntax error in input!')
            print(p)

        # get the lexer and token mappings to pass to yacc
        xprotLex = XProtLexer()
        lexer = xprotLex.lexer
        tokens = xprotLex.tokens

        # Build the parser
        parser = yacc.yacc()

        # load in the data
        result = parser.parse(xprot)
        # print(json.dumps(self.structure,indent=2))
