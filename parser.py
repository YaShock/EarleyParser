import copy

class Variable(object):
    """docstring for Variable"""
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        if not isinstance(other, Variable):
            return False
        return self.name == other.name
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash(self.name)

class Rule(object):
    """docstring for Rule"""
    def __init__(self, variable, production):
        self.variable = variable
        self.production = production
    def __repr__(self):
        return "%s -> %s" % (self.variable.name, repr(self.production))
    def __eq__(self, other):
        return (self.variable, self.production) == (other.variable, other.production)
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash((self.variable, self.production))


class Production(object):
    """docstring for Production"""
    def __init__(self, *terms):
        #terms are variables or terminals
        self.terms = terms
    def __repr__(self):
        return " ".join(str(t) for t in self.terms)
    def __eq__(self, other):
        if not isinstance(other, Production):
            return False
        return self.terms == other.terms
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash(self.terms)
    def __len__(self):
        return len(self.terms)
    def __iter__(self):
        return iter(self.terms)
    def __getitem__(self, index):
        return self.terms[index]

class FloatTerm(object):
    index = 0
    def __init__(self):
        self.val = None
        FloatTerm.index = FloatTerm.index + 1
    def __eq__(self, other):
        if isinstance(other, str):
            try:
                self.val = float(other)
                return True
            except ValueError:
                return False
        elif isinstance(other, FloatTerm):
            return self.index == other.index
        return False
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash(__class__.__name__)
    def __repr__(self):
        if self.val:
            return str(self.val)
        else:
            return __class__.__name__

class StringTerm(object):
    index = 0
    def __init__(self):
        self.val = None
        StringTerm.index = StringTerm.index + 1
        self.index = StringTerm.index
    def __eq__(self, other):
        if isinstance(other, str):
            try:
                float(other)
                return False
            except ValueError:
                self.val = str(other)
                return True
        elif isinstance(other, StringTerm):
            return self.index == other.index
        return False
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash((__class__.__name__, self.index))
    def __repr__(self):
        if self.val:
            return str(self.val)
        else:
            return __class__.__name__

class State(object):
    """docstring for State"""
    num = 0
    def __init__(self, rule, dotPos, orig_pos, end_pos, back_pointers=[]):
        self.index = State.num
        State.num += 1
        self.rule = rule
        self.dotPos = dotPos
        self.orig_pos = orig_pos
        self.end_pos = end_pos
        self.back_pointers = list(back_pointers)
    def __repr__(self):
        terms = [str(p) for p in self.rule.production]
        terms.insert(self.dotPos, u"$")
        pointers = " ".join(str(i.index) for i in self.back_pointers)
        return "%d %-1s -> %-8s [%s-%s] [%-s]" % (self.index, self.rule.variable, " ".join(terms), self.orig_pos, self.end_pos, pointers)
    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return (self.rule, self.dotPos, self.orig_pos, self.back_pointers) == (other.rule, other.dotPos, other.orig_pos, other.back_pointers)
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash((self.rule, self.dotPos, self.orig_pos))
    def finished(self):
        return self.dotPos >= len(self.rule.production)
    def next(self):
        if self.finished():
            return None
        return self.rule.production[self.dotPos]

class Tree(object):
    def __init__(self, data=None, children=None):
        self.children = []
        if children is not None:
            self.children.extend(children)
        self.data = data
    def add(self, child):
        self.children.append(child)
    def print(self, level=0):
        if level == 9:
            return
        text = "\t"*level+str(self.data)
        print(text)
        for child in self.children:
            child.print(level+1)

class EarleyParser(object):
    """docstring for EarleyParser"""
    def __init__(self, topRule):
        self.topRule = topRule
        self.grammar = set()
        self.terminals = set()

    def add(self, rule):
        self.grammar.add(rule)
        for term in rule.production.terms:
            if not isinstance(term, Variable):
                self.terminals.add(term)

    def __init_states(self, text):
        self.state_list = []
        self.text = text
        for k in range(len(self.tokens)+1):
            self.state_list.append(set())

    def tokenize(self, text):
        self.tokens = text.split(' ')

    def parse(self, text):
        self.tokenize(text)
        self.__init_states(text)
        self.state_list[0].add(State(self.topRule, 0, 0, 0))
        for k in range(len(self.tokens)+1):
            print("\nk = %d" % k)
            active = set(self.state_list[k])
            seen = set(self.state_list[k])
            while active:
                for state in active:
                    if not state.finished():
                        if not self.is_terminal(state.next()):
                            self.predict(state, k)
                        else:
                            self.scan(state, k)
                    else:
                        self.complete(state, k)
                seen |= active
                active = self.state_list[k]-seen
            print()
            for state in self.state_list[k]:
                print(state)
        result = []
        for st in self.state_list[-1]:
            if st.rule == self.topRule:
                result.append(self.construct_tree(st))
        return result

    def is_terminal(self, token):
        return token in self.terminals

    def predict(self, state, k):
        for rule in self.grammar:
            if state.next() == rule.variable:
                self.state_list[k].add(State(rule, 0, k, k))

    def scan(self, state, k):
        if k >= len(self.tokens):
            return
        if state.next() == self.tokens[k]:
            self.state_list[k+1].add(State(copy.deepcopy(state.rule), state.dotPos+1, state.orig_pos, k+1, state.back_pointers))

    def complete(self, state, k):
        for s in self.state_list[state.orig_pos]:
            if s.next() == state.rule.variable:
                newState = State(s.rule, s.dotPos+1, s.orig_pos, k, s.back_pointers)
                newState.back_pointers.append(state)
                self.state_list[k].add(newState)

    def read_file(self, file):
        for line in file:
            print(line)

    def __parse_rule(self, line):
        l = line.split('->')


    def construct_tree(self, state, level=0):
        tree = Tree()
        tree.data = repr(state.rule.variable)
        j = 0
        for i in range(len(state.rule.production)):
            node = Tree()
            if state.back_pointers:
                if not self.is_terminal(state.rule.production[i]):
                    node = self.construct_tree(state.back_pointers[j], level+1)
                    j += 1
            node.data = repr(state.rule.production[i])
            tree.add(node)
        return tree


GAMMA = Variable("GAMMA")
Command = Variable("Command")
Transform = Variable("Transform")
Generate = Variable("Generate")
LoadFile = Variable("LoadFile")
Modify = Variable("Modify")
Request = Variable("Request")
TextObject = Variable("TextObject")
ModTerm = Variable("ModTerm")
DelTerm = Variable("DelTerm")
ReqTerm = Variable("ReqTerm")
TrasformFunction = Variable("TrasformFunction")
FunctionLower = Variable("FunctionLower")
FunctionUpper = Variable("FunctionUpper")
Delete = Variable("Delete")
Object = Variable("Object")
WordList = Variable("WordList")
W = Variable("W")
SparseWords = Variable("SparseWords")
FreqWords = Variable("FreqWords")
Stopwords = Variable("Stopwords")
Language = Variable("Language")
WordTerm = Variable("WordTerm")
GenerateTerm = Variable("GenerateTerm")
WhiteSpaces = Variable("WhiteSpaces")

parser = EarleyParser(Rule(GAMMA, Production(Command)))

parser.add(Rule(Command, Production(Transform)))
parser.add(Rule(Command, Production(Generate)))
parser.add(Rule(Command, Production(Request)))
parser.add(Rule(Command, Production(LoadFile)))

parser.add(Rule(LoadFile, Production('load', StringTerm())))
parser.add(Rule(Generate, Production(GenerateTerm, 'word', 'cloud')))

parser.add(Rule(Transform, Production(Modify)))
parser.add(Rule(Transform, Production(Delete)))

parser.add(Rule(Modify, Production(ModTerm, TextObject, "to", TrasformFunction)))
parser.add(Rule(Modify, Production(ModTerm, "to", TrasformFunction)))
parser.add(Rule(TrasformFunction, Production(FunctionLower)))
parser.add(Rule(TrasformFunction, Production(FunctionUpper)))
parser.add(Rule(FunctionLower, Production("lower", "case")))
parser.add(Rule(FunctionLower, Production("lower")))
parser.add(Rule(FunctionUpper, Production("upper", "case")))
parser.add(Rule(FunctionUpper, Production("upper")))

parser.add(Rule(Delete, Production(DelTerm, Object)))
parser.add(Rule(Request, Production(ReqTerm, Object)))

parser.add(Rule(Object, Production("numbers")))
parser.add(Rule(Object, Production("punctuation")))
parser.add(Rule(Object, Production(Stopwords)))
parser.add(Rule(Object, Production(WordList)))
parser.add(Rule(Object, Production(WhiteSpaces)))
parser.add(Rule(Object, Production(SparseWords)))
parser.add(Rule(Object, Production(FreqWords)))
parser.add(Rule(SparseWords, Production(WordTerm, "sparsity", FloatTerm())))
parser.add(Rule(FreqWords, Production(WordTerm, "frequency", "between", FloatTerm(), "and", FloatTerm())))
parser.add(Rule(Stopwords, Production(Language, "stopwords")))
parser.add(Rule(Stopwords, Production(Language, "stop", "words")))
parser.add(Rule(Language, Production("english")))
parser.add(Rule(Language, Production("german")))
parser.add(Rule(Language, Production("hungarian")))
parser.add(Rule(TextObject, Production("text")))
parser.add(Rule(TextObject, Production("document")))
parser.add(Rule(ModTerm, Production('modify')))
parser.add(Rule(ModTerm, Production('transform')))
parser.add(Rule(ModTerm, Production('convert')))
parser.add(Rule(DelTerm, Production('delete')))
parser.add(Rule(DelTerm, Production('remove')))
parser.add(Rule(DelTerm, Production('strip')))
parser.add(Rule(DelTerm, Production('take', 'out')))
parser.add(Rule(ReqTerm, Production('get')))
parser.add(Rule(ReqTerm, Production('find')))
parser.add(Rule(ReqTerm, Production('what', 'are')))
parser.add(Rule(ReqTerm, Production('what', 'is')))
parser.add(Rule(WordTerm, Production('words')))
parser.add(Rule(WordTerm, Production('terms')))
parser.add(Rule(GenerateTerm, Production('create')))
parser.add(Rule(GenerateTerm, Production('generate')))
parser.add(Rule(GenerateTerm, Production('make')))
parser.add(Rule(WhiteSpaces, Production('white', 'space')))
parser.add(Rule(WhiteSpaces, Production('whitespace')))
parser.add(Rule(WordList, Production(WordTerm, W)))
parser.add(Rule(W, Production(W, W)))
parser.add(Rule(W, Production(StringTerm())))

lst = parser.parse("convert to upper case")
for t in lst:
    t.print()

file = open('cf.txt')
parser.read_file(file)