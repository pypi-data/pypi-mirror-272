import pysam
from collections import namedtuple
from functools import lru_cache
from enum import Enum,unique
import warnings
class CPRA():
    """
    descriptrion a mutation in cpra( eg: chr1, 100, A, T)
    and get some useful information with Bam or reference genome:
    """

    reference=None
    bam=None

    @classmethod
    def loadReference(cls,reference):
        """
        load reference genome
        param reference FilePath: eg: d:\Git_Repo\package_ngstools\data\hg19.fa
        """
        if cls.reference is None:
            cls.reference = pysam.FastaFile(reference)
        else:
            cls.reference = pysam.FastaFile(reference)
            print("reference has been loaded & reloaded")

    @classmethod
    def loadBam(cls,Bam):
        """
        load bam file
        param Bam FilePath : eg: d:\Git_Repo\package_ngstools\data\test.bam
        """
        cls.bam = pysam.AlignmentFile(Bam)

    def __init__(self,CHROM:str,POS:int,REF:str,ALT:str):
        """
        Init a mutation object,
        param chrom(str): eg: chr1
        param pos(int): eg: 100
        param REF(str):表示参考序列的字符串 eg: A
        param ALT(str):表示替代序列的字符串。 eg: T
        """
        self.chrom = CHROM
        self.pos =  int(POS)
        self.pos_fit =  int(POS)
        self.ref = REF
        self.alt = ALT

        if not self._is_valid_nucleotide_sequence(REF):
            warnings.warn(f"Invalid REF sequence '{REF}'; using empty string instead.")
            self.ref = ""

        if not self._is_valid_nucleotide_sequence(ALT):
            warnings.warn(f"Invalid ALT sequence '{ALT}'; using empty string instead.")
            self.alt = ""
        if hasattr(self,'bam'):
            self.get_suppot()

    @staticmethod
    def _is_valid_nucleotide_sequence(sequence: str) -> bool:
        valid_nucleotides = set('ATCGatcg')
        return all(nucleotide in valid_nucleotides for nucleotide in sequence)

    def _is_valid_ref_sequence(self)->int:
        try:
            if self.reference.fetch(self.chrom, self.pos, self.pos+len(self.ref)) == self.ref:
                return 0
            elif self.reference.fetch(self.chrom, self.pos+1, self.pos+1+len(self.ref))== self.ref:
                return 1
            else:
                raise ValueError("ref sequence do not match with the genome file, check your data")
        except AttributeError as e:
            raise e.add_note("reference genome is not set, set it with cpra.loadReference(referencePath)")

    @property
    def info(self):
        """
        return the information of the mutation
        """
        if hasattr(self,'support_readsID_list'):
            return f"{self.chrom}\t{self.pos}\t{self.ref}\t{self.alt}\t{self.muttype}\t{self.supportReadNum}\t{self.CoverReadNum}\t{self.ratio}"
        else:
            return f"{self.chrom}\t{self.pos}\t{self.ref}\t{self.alt}\t*\t*\t*\t*"

    @property
    def muttype(self):
        if len(self.ref)>len(self.alt):
            return "DEL"
        elif len(self.ref)<len(self.alt):
            return "INS"
        else:
            return "SNV"

    @property
    def flank10(self, length:int=10):
        '''获取变异的侧翼10bp序列
        使用前需要通过loadReference(reference) 完成参考基因组的加载
        param length: 侧翼序列长度
        '''
        lbase = self.reference.fetch(self.chrom, self.pos-length,self.pos)
        rbase = self.reference.fetch(self.chrom, self.pos+len(self.ref), self.pos+len(self.ref)+length)
        return '..'.join((lbase, rbase))
    
    @property
    def CoverReadList(self):
        if hasattr(self,'cover_readsID_list'):
            return self._cover_readsID_list
        else :
            self.get_suppot()
            return self._cover_readsID_list
    @property
    def CoverReadNum(self):
        return len(self.CoverReadList)

    @property
    def supportReads(self):
        if hasattr(self,'support_reads'):
            return self._support_reads
        else :
            self.get_suppot()
            return self._support_reads

    @property
    def supportreadsIDlist(self):
        if hasattr(self,'support_readsID_list'):
            return self._support_readsID_list
        else :
            self.get_suppot()
            return self._support_readsID_list

    @property
    def supportReadNum(self):
        return len(self.supportreadsIDlist)

    @property
    def ratio(self):
        return self.supportReadNum/self.CoverReadNum

    def flank(self, length:int):
        '''获取变异的任意长度侧翼序列
        使用前需要通过loadReference(reference) 完成参考基因组的加载
        param length: 侧翼序列长度
        '''
        lbase = self.reference.fetch(self.chrom, self.pos-length,self.pos)
        rbase = self.reference.fetch(self.chrom, self.pos+len(self.ref), self.pos+len(self.ref)+length)
        return '..'.join((lbase, rbase))

    def get_suppot(self,bam="",ref="",coverflank=5):
        """
        get support for the mutation with special Bam File &ref;
        param coverflank: only the reads cover the ±coverflank(5) bases will be considered
        get property: support_reads,support_readsID_list,cover_readsID_list
        """
        if(self.bam is None):
            if(bam is not None):
                self.loadBam(bam)
            else:
                raise ValueError("bam file is not set, set it with cpra.loadBam(bamPath)")
        if(self.reference is None):
            if(ref is not None):
                self.loadReference(ref)
            else:
                raise ValueError("reference genome is not set, set it with cpra.loadReference(referencePath)")
        self.pos_fit = self.pos+ self._is_valid_ref_sequence()
        self._support_reads = []
        self._support_readsID_list = []
        self._cover_readsID_list = []
        if self.muttype == "SNV":
            self._support_reads,self._support_readsID_list,self._cover_readsID_list = self._get_snv_support_reads(coverflank)
        elif self.muttype == "INS":
            self._support_reads,self._support_readsID_list,self._cover_readsID_list = self._get_ins_support_reads(coverflank)
        elif self.muttype == "DEL":
            self._support_reads,self._support_readsID_list,self._cover_readsID_list = self._get_del_support_reads(coverflank)

    @lru_cache
    def _get_snv_support_reads(self, coverflank=5, mapq=20, baseq=20, overlaps=True, stepper="all", orphans=True):
        Read = namedtuple('Read', ['read_name', 'pair', 'strand'])
        support_reads = []
        cover_reads = []
        start_reads = {}
        EndSite = self.pos_fit + len(self.ref)
        for pileup_column in self.bam.pileup(region=str(self.chrom) + ':' + str(self.pos_fit) + '-' + str(self.pos_fit),mapq=mapq , baseq = baseq,
                                            stepper=stepper, fastaFile=self.reference, max_depth=200000, **{"truncate": True}):
            if pileup_column.nsegments > 0:
                for pileup_read in pileup_column.pileups:
                    aln = pileup_read.alignment
                    read_name = aln.query_name
                    pair = 'pe1' if aln.is_read1 else 'pe2'
                    strand = '-' if aln.is_reverse else '+'
                    read = Read(read_name, pair, strand)
                    if pileup_read.is_del or pileup_read.is_refskip or (aln.flag > 1024) or (aln.mapping_quality < mapq) or \
                            aln.query_qualities[pileup_read.query_position] < baseq:
                        continue
                    start_reads[read] = [pileup_read.query_position, aln]
        for pileup_column in self.bam.pileup(region=str(self.chrom) + ':' + str(EndSite) + '-' + str(EndSite),
                                            stepper=stepper, fastaFile=self.reference, max_depth=200000, **{"truncate": True}):
            if pileup_column.nsegments > 0:
                for pileup_read in pileup_column.pileups:
                    aln = pileup_read.alignment
                    read_name = aln.query_name
                    pair = 'pe1' if aln.is_read1 else 'pe2'
                    strand = '-' if aln.is_reverse else '+'
                    read = Read(read_name, pair, strand)
                    if pileup_read.is_del or pileup_read.is_refskip:
                        continue
                    if read in start_reads:
                        start_query_position, start_aln = start_reads[read]
                        seq = start_aln.query_sequence[start_query_position:pileup_read.query_position]
                        cover_reads.append(aln)
                        if seq.upper() == self.alt.upper():
                            support_reads.append(aln)
        support_readIDs = []
        cover_readID_list = []
        for aln in cover_reads:
            cover_readID_list.append(aln.query_name)
        for aln in support_reads:
            support_readIDs.append(aln.query_name)
        return [support_reads,support_readIDs,cover_readID_list]

    @lru_cache
    def _get_ins_support_reads(self, coverflank=5, mapq=20, baseq=20, overlaps=True, stepper="all", orphans=True):
        support_reads = []
        cover_reads = []
        bam = {}
        EndSite = self.pos_fit + len(self.ref)
        CoverStart = self.pos_fit-coverflank
        CoverEnd = EndSite + coverflank
        insLength=len(self.alt)-len(self.ref)
        for pileup_column in self.bam.pileup(region=str(self.chrom) + ':' + str(self.pos_fit) + '-' + str(self.pos_fit), mapq=mapq, baseq=baseq, stepper=stepper, fastaFile=self.reference, max_depth=200000, **{"truncate": True}):
            if pileup_column.nsegments > 0:
                for pileup_read in pileup_column.pileups:
                    aln = pileup_read.alignment
                    bam[aln.query_name] = pileup_read
                    if (CoverStart in aln.positions) and (CoverEnd in aln.positions):
                        cover_reads.append(aln)
                        if pileup_read.query_position and aln.cigarstring.find("I") > 0:
                            start = pileup_read.query_position-1
                            altstop = pileup_read.query_position - 1 +len(self.alt)
                            refstop = pileup_read.query_position-1 + len(self.ref)
                            if aln.query_sequence[start:altstop].upper() == self.alt.upper() and \
                                    aln.get_reference_sequence()[start:refstop].upper() == self.ref.upper():
                                support_reads.append(aln)
                            elif aln.query_sequence[pileup_read.query_position-insLength:pileup_read.query_position -insLength+ len(self.alt)].upper() == self.alt.upper() and \
                                aln.get_reference_sequence()[pileup_read.query_position-insLength:pileup_read.query_position - insLength + len(self.ref)].upper() == self.ref.upper():
                                support_reads.append(aln)
                            elif aln.query_sequence[pileup_read.query_position:pileup_read.query_position + len(self.alt)].upper() == self.alt.upper() and \
                                aln.get_reference_sequence()[pileup_read.query_position:pileup_read.query_position + len(self.ref)].upper() == self.ref.upper():
                                support_reads.append(aln)
        support_readID_list = []
        cover_readID_list = []
        for aln in cover_reads:
            cover_readID_list.append(aln.query_name)
        for aln in support_reads:
            support_readID_list.append(aln.query_name)
        return [support_reads,support_readID_list,cover_readID_list]

    @lru_cache
    def _get_del_support_reads(self, coverflank=5, mapq=20, baseq=20, overlaps=True, stepper="all", orphans=True):
        support_reads = []
        cover_reads = []
        bam = {}
        EndSite = self.pos_fit + len(self.ref)
        CoverStart = self.pos_fit-coverflank
        CoverEnd = EndSite + coverflank
        for pileup_column in self.bam.pileup(region=str(self.chrom) + ':' + str(self.pos_fit) + '-' + str(EndSite), mapq=mapq , baseq = baseq,
                                            stepper=stepper, fastaFile=self.reference, max_depth=200000, **{"truncate": True}):
            if pileup_column.nsegments > 0:
                for pileup_read in pileup_column.pileups:
                    aln = pileup_read.alignment
                    bam[aln.query_name]=pileup_read
                    if (CoverStart in aln.positions) and (CoverEnd in aln.positions):
                        cover_reads.append(aln)
                        if pileup_read.query_position_or_next and aln.cigarstring.find("D") > 0:
                            start = pileup_read.query_position_or_next - 1
                            refstop = pileup_read.query_position_or_next + len(self.ref) - 1
                            altstop = pileup_read.query_position_or_next +len(self.alt) -1
                            if aln.get_reference_sequence()[start:refstop].upper() == self.ref.upper() and aln.query_sequence[start:altstop].upper() == self.alt.upper():
                                support_reads.append(aln)
                            elif aln.get_reference_sequence()[start+1:refstop+1].upper() == self.ref.upper() and aln.query_sequence[start+1:altstop+1].upper() == self.alt.upper():
                                support_reads.append(aln)
        support_readsID_list = []
        cover_readID_list = []
        for aln in cover_reads:
            cover_readID_list.append(aln.query_name)
        for aln in support_reads:
            support_readsID_list.append(aln.query_name)
        return [support_reads,support_readsID_list,cover_readID_list]

