class documento:
    def __init__(self):  # ,rg,nome,pai,mae,naturalidade,expedicao,nascimento,cpf)
        self.rg = ""
        self.nome = ""
        self.pai = ""
        self.mae = ""
        self.naturalidade = ""
        self.uf = ""
        self.expedicao = ""
        self.nascimento = ""
        self.cpf = ""

    def setRg(self, rg):
        self.rg = rg

    def setNome(self, nome):
        self.nome = self.nome + " " + nome

    def setPai(self, pai):
        self.pai = pai

    def setMae(self, mae):
        self.mae = mae

    def setNaturalidade(self, naturalidade):
        self.naturalidade = naturalidade

    def setUf(self, uf):
        self.uf = uf

    def setExpedicao(self, expedicao):
        self.expedicao = expedicao

    def setNascimento(self, nascimento):
        self.nascimento = nascimento

    def setCpf(self, cpf):
        self.cpf = cpf

    def getRg(self):
        return self.rg

    def getNome(self):
        return self.nome

    def getPai(self):
        return self.pai

    def getMae(self):
        return self.mae

    def getNaturalidade(self):
        return self.naturalidade

    def getUf(self):
        return self.uf

    def getEExpedicao(self):
        return self.expedicao

    def getNascimento(self):
        return self.nascimento

    def getCpf(self):
        return self.cpf
