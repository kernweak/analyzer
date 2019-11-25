__version__G__ = "(G)bd249ce4"

from ..logger.logger import logstring,verbose,verbose_flag
from ..mics.qprogressbar import progressbar
from ..mics.funcs import iptolong,getentropyfloatret
from itertools import chain,takewhile
from re import I, compile, findall, search

@progressbar(True,"Starting QBDGA")
class QBDGA:
    def __init__(self):
        '''
        initialize class
        '''
    @verbose(verbose_flag)
    @progressbar(True,"DGA-Find repeated patterns")
    def seqstongrams(self,data,domains):
        '''
        loop sequences, converts sequences to ngrams. map all of them and get thier intersection
        then, return the max item

        Args:
            data: dict object
            domains: list of domains
        '''
        try:
            allngrams = []
            l = []
            for domain in domains:
                if len(domain) > 2: 
                    for length in range(2,len(domain)+1):
                        l.extend([domain[i: i + length] for i in range(len(domain) - length + 1)])
                    allngrams.append(l)
                    l = []
            common_items = set.intersection(*map(set, allngrams))
            if common_items:
                sortedlist = sorted(common_items, key=lambda i: len(i), reverse=True)
                maxvalues = list(takewhile(lambda e: len(e) == len(sortedlist[0]), sortedlist))
                for x in maxvalues:
                    data.append({"Length":len(x),"Repeated":x})
        except:
            pass

    @verbose(verbose_flag)
    @progressbar(True,"DGA-Find low frequency letters")
    def findlowfreqletters(self,data,domains):
        '''
        loop sequences, find low frequency letters 

        Args:
            data: dict object
            domains: list of domains
        '''
        lowfreq = compile(r"[vkjxqz]")
        for domain in domains:
            x = findall(lowfreq,domain)
            if len(x) > 4:
                data.append({"Count":len(x),"Letters":''.join(x),"URL":domain})

    @verbose(verbose_flag)
    @progressbar(True,"DGA-Find consonants letters in row")
    def findconsonantslettersinrow(self,data,domains):
        '''
        loop sequences, find consonants in row

        Args:
            data: dict object
            domains: list of domains
        '''
        consonants = compile(r"[bcdfghjklmnpqrstvwxyz]{4,}")
        for domain in domains:
            x = findall(consonants,domain)
            if len(x) > 2:
                data.append({"Groups":"{} > 2 groups".format(len(x)),"Row":','.join(x),"URL":domain})

    @verbose(verbose_flag)
    @progressbar(True,"DGA-Find consonants letters")
    def findconsonantsletters(self,data,domains):
        '''
        loop sequences, find consonants 

        Args:
            data: dict object
            domains: list of domains
        '''
        consonants = compile(r"[bcdfghjklmnpqrstvwxyz]")
        for domain in domains:
            x = findall(consonants,domain)
            if len(x) > 8:
                data.append({"Count":"{} > 8".format(len(x)),"Letters":''.join(x),"URL":domain})

    @verbose(verbose_flag)
    @progressbar(True,"DGA-Find encryptions")
    def findencryptionpatterns(self,data,domains):
        '''
        loop sequences, find encryptions 

        Args:
            data: dict object
            domains: list of domains
        '''
        _hex = compile(r'([0-9a-fA-F]{4,})',I)
        for domain in domains:
            detection = search(_hex, domain)
            if detection is not None:
                temp = ""
                if len(detection.group()) == 32:
                    temp = "md5"
                elif len(detection.group()) == 40:
                    temp = "sha1"
                elif len(detection.group()) == 64:
                    temp = "sha256"
                elif len(detection.group()) == 128:
                    temp = "sha512"
                else:
                    temp = "HEX"

                data.append({"Type":temp,"Detected":detection.group(),"URL":domain})

    @verbose(verbose_flag)
    @progressbar(True,"DGA-Find symbols")
    def findallsymbols(self,data,domains):
        '''
        loop sequences, find symbols 

        Args:
            data: dict object
            domains: list of domains
        '''
        detection = compile(r'[_\-~]',I)
        for domain in domains:
            x = findall(detection,domain)
            #group them
            if len(x) > 2:
                data.append({"Count":"{} > 2".format(len(x)),"Symbols":''.join(x),"URL":domain})

    @verbose(verbose_flag)
    @progressbar(True,"DGA-Find numbers")
    def findallnumbers(self,data,domains):
        '''
        loop sequences, find numbers 

        Args:
            data: dict object
            domains: list of domains
        '''
        detection = compile(r'[\d]',I)
        for domain in domains:
            x = findall(detection,domain)
            if len(x) > 5:
                data.append({"Count":"{} > 5".format(len(x)),"Numbers":''.join(x),"URL":domain})

    @verbose(verbose_flag)
    @progressbar(True,"DGA-Find long domains")
    def URLlength(self,data,domains):
        '''
        loop sequences, find long domains 

        Args:
            data: dict object
            domains: list of domains
        '''
        for domain in domains:
            if len(domain) > 13:
                data.append({"Length":"{} > 13".format(len(domain)),"URL":domain})

    @verbose(verbose_flag)
    @progressbar(True,"DGA-Get entropies of domains")
    def checkentropy(self,data,domains):
        '''
        loop sequences, get entropy

        Args:
            data: dict object
            domains: list of domains
        '''
        for domain in domains:
            entropy = getentropyfloatret(domain)
            if entropy > 3.7:
                data.append({"Entropy":"{0:.15f}".format(entropy),"URL":domain})

    @progressbar(True,"Finding Domain Generational Algorithm patterns")
    def checkdga(self,data):
        data["DGA"] = {  "Repeated":[],
                         "LowFreqLetters":[],
                         "ConsonantsRow":[],
                         "Consonants":[],
                         "Encryption":[],
                         "Symbols":[],
                         "Numbers":[],
                         "Long":[],
                         "Entropy":[],
                         "_Repeated":["Length","Repeated"],
                         "_LowFreqLetters":["Count","Letters","URL"],
                         "_ConsonantsRow":["Groups","Row","URL"],
                         "_Consonants":["Count","Letters","URL"],
                         "_Encryption":["Type","Detected","URL"],
                         "_Symbols":["Count","Symbols","URL"],
                         "_Numbers":["Count","Numbers","URL"],
                         "_Long":["Length","URL"],
                         "_Entropy":["Entropy","URL"]}

        self.seqstongrams(data["DGA"]["Repeated"],data["PCAP"]["Domains"])
        self.findlowfreqletters(data["DGA"]["LowFreqLetters"],data["PCAP"]["Domains"])
        self.findconsonantslettersinrow(data["DGA"]["ConsonantsRow"],data["PCAP"]["Domains"])
        self.findconsonantsletters(data["DGA"]["Consonants"],data["PCAP"]["Domains"])
        self.findencryptionpatterns(data["DGA"]["Encryption"],data["PCAP"]["Domains"])
        self.findallsymbols(data["DGA"]["Symbols"],data["PCAP"]["Domains"])
        self.findallnumbers(data["DGA"]["Numbers"],data["PCAP"]["Domains"])
        self.URLlength(data["DGA"]["Long"],data["PCAP"]["Domains"])
        self.checkentropy(data["DGA"]["Entropy"],data["PCAP"]["Domains"])