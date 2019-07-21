import sys
import os
from physcraper import ConfigObj, IdDicts, PhyscraperScrape


import pickle#

sys.stdout.write("\ntests remove_identical\n")


# tests if identical sequences are removed.
workdir = "tests/output/test_remove_id_seq"
configfi = "tests/data/test.config"
absworkdir = os.path.abspath(workdir)

def test_remove_id_seq():
    conf = ConfigObj(configfi, interactive=False)
    data_obj = pickle.load(open("tests/data/precooked/tiny_dataobj.p", 'rb'))
    data_obj.workdir = absworkdir
    ids = IdDicts(conf, workdir=data_obj.workdir)
    ids.acc_ncbi_dict = pickle.load(open("tests/data/precooked/tiny_acc_map.p", "rb"))

    filteredScrape =  PhyscraperScrape(data_obj, ids)
    filteredScrape._blasted = 1

    #############################

    id_seq = ["TCGAAACCTGCATAGCAGAACGACCT-GTGAACATGTAAAAACAATTGGG-TGTTCTAAGTATCGGGCTCTTGTTCGATTTCTA-GGATGCCATGTTGACGTGCGTCTTTGGCAAGCCCCTTGGGTGT-CTAAGGACGTCACGTCGACG-CAACAACAAACCCCCGGCACGGCATGTGCCAAGGAAATATAAACTTAAGAAGGGC--TT-GTTCCATGCATT--GCCGTT--CGCGGTGATTGCATTGAAACTTGCTTCTTTATAA-TTCATAAACGACTCTCGG-CAACGGATATCTCGGCTCACGCATCGATGAAGAACGTAGCAAAATGCGATACTTGGTGTGAATTGCAGAATCCCGTGAACCATCGAGTTTTTGAACGCAAGTTGCGCCC-GAAGCCTTTTGGTTGAGGGCACGTCTGCCTGGGCGTCACATATCGCGTCGCCC-CCATCAC---ACCTCTT-GACGGGGATGTTTGAATGGGGA-CGGAGATTGGTCTCCCGTTCCT---AAGGTGCGGTTGCCTGAATTTTGAGTCCTCTTCGACGGACGCACGATTAGTGGTGGTTGACAAGACCTTCT--------------TATCGAGTTGTGTG--TTCCAAGAAGTAA-GGAATATCTCTTTAACGACCC-TAAAGTGTTGTCTCATG-ACGATGCTTCGACTGC",
                "TCGAAACCTGCATAGCAGAACGACCTGTGAACATGTAAAAACAATTGGGTGTTCTAAGTATCGGGCTCTTGTTCGATTTCTAGGATGCCATGTTGACGTGCGTCTTTGGCAAGCCCCTTGGGTGTCTAAGGACGTCACGTCGACGCAACAACAAACCCCCGGCACGGCATGTGCCAAGGAAATATAAACTTAAGAAGGGCTTGTTCCATGCATTGCCGTTCGCGGTGATTGCATTGAAACTTGCTTCTTTATAATTCATAAACGACTCTCGGCAACGGATATCTCGGCTCACGCATCGATGAAGAACGTAGCAAAATGCGATACTTGGTGTGAATTGCAGAATCCCGTGAACCATCGAGTTTTTGAACGCAAGTTGCGCCCGAAGCCTTTTGGTTGAGGGCACGTCTGCCTGGGCGTCACATATCGCGTCGCCCCCATCACACCTCTTGACGGGGATGTTTGAATGGGGACGGAGATTGGTCTCCCGTTCCTAAGGTGCGGTTGCCTGAATTTTGAGTCCTCTTCGACGGACGCACGATTAGTGGTGGTTGACAAGACCTTCTTATCGAGTTGTGTGTTCCAAGAAGTAAGGAATATCTCTTTAACGACCCTAAAGTGTTGTCTCATGACGATGCTTCGACTGC",
                "TCGAAACCTGCATAGCAGAACGACCTGTGAACATGTAAAAACAATTGGGTGTTCTAAGTATCGGGCTCTTGTTCGATTTCTAGGATGCCATGTTGACGTGCGTCTTTGGCAAGCCCCTTGGGTGTCTAAGGACGTCACGTCGACGCAACAACAAACCCCCGGCACGGCATGTGCCAAGGAAATATAAACTTAAGAAGGGCTTGTTCCATGCATTGCCGTTCGCGGTGATTGCATTGAAACTTGCTTCTTTATAATTCATAAACGACTCTCGGCAACGGATATCTCGGCTCACGCATCGATGAAGAACGTAGCAAAATGCGATACTTGGTGTGAATTGCAGAATCCCGTGAACCATCGAGTTTTTGAACGCAAGTTGCGCCCGAAGCCTTTTGGTTGAGGGCACGTCTGCCTGGGCGTCACATATCGCGTCGCCCCCATCACACCTCTTGACGGGGATGTTTGAATGGGGACGGAGATTGGTCTCCCGTTCCTAAGGTGCGGTTGCCTGAATTTTGAGTCCTCTTCGACGGACGCACGATTAGTGGTGGTTGACAAGACCTTCTTATCGAGTTGTGTGTTCCAAGAAGTAAGGAATATCTCTTTAACGACCCTAAAGTGTTGTCTCATGACGATGCTTCGACTGCGCGCGCGC",
                "TCGAAACCTGCATAGCAGAACGACCTGTGAACATGTAAAAACAATTGGGTGTTCTAAGTATCGGGCTCTTGTTCGATTTCTAGGATGCCATGTTGACGTGCGTCTTTGGCAAGCCCCTTGGGTGTCTAAGGACGTCACGTCGACGCAACAACAAACCCCCGGCACGGCATGTGCCAAGGAAATATAAACTTAAGAAGGGCTTGTTCCATGCATTGCCGTTCGCGGTGATTGCATTGAAACTTGCTTCTTTATAATTCATAAACGACTCTCGGCAACGGATATCTCGGCTCACGCATCGATGAAGAACGTAGCAAAATGCGATACTTGGTGTGAATTGCAGAATCCCGTGAACCATCGAGTTTTTGAACGCAAGTTGCGCCCGAAGCCTTTTGGTTGAGGGCACGTCTGCCTGGGCGTCACATATCGCGTCGCCCCCATCACACCTCTTGACGGGGATGTTTGAATGGGGACGGAGATTGGTCTCCCGTTCCTAAGGTGCGGTTGCCTGAATTTTGAGTCCTCTTCGACGGACGCACGATTAGTGGTGGTTGACAAGACCTTCTTATCGAGTTGTGTGTTCCAAGAAGTAAGGAATATCTCTTTAACGACCCTAAAGTGTTGTCTCATGACGATGCTTCGACTGCGCGCGCGC"
                ]

    # print("start test")
    tmp_dict = dict((taxon.label, filteredScrape.data.aln[taxon].symbols_as_string()) for taxon in filteredScrape.data.aln)
    old_seqs = tmp_dict.keys()
    avg_seqlen = sum(filteredScrape.data.orig_seqlen)/len(filteredScrape.data.orig_seqlen)
    assert filteredScrape.config.seq_len_perc <= 1
    seq_len_cutoff = avg_seqlen*filteredScrape.config.seq_len_perc
    count=1

    for item in id_seq:
        if len(item.replace("-", "").replace("N", "")) > seq_len_cutoff:
            ott = "OTT_{}".format(count)
            count += 1
            otu_id = ott
            filteredScrape.data.otu_dict[otu_id] = {}
            filteredScrape.data.otu_dict[otu_id]['^ncbi:gi'] = 1061375300
            filteredScrape.data.otu_dict[otu_id]['^ncbi:accession'] =   "KX494441"
            filteredScrape.data.otu_dict[otu_id]['^ncbi:title'] = "some random title"
            filteredScrape.data.otu_dict[otu_id]['^ncbi:taxon'] = 0101010101
            filteredScrape.data.otu_dict[otu_id]['^ot:ottId'] = ott
            filteredScrape.data.otu_dict[otu_id]['^physcraper:status'] = "query"
            filteredScrape.data.otu_dict[otu_id]['^ot:ottTaxonName'] = "Senecio vulgaris"
            filteredScrape.data.otu_dict[otu_id]['^physcraper:last_blasted'] = "1800/01/01"
            filteredScrape.del_superseq = set()
            filteredScrape.seq_dict_build(item, otu_id, tmp_dict)
    for tax in old_seqs:
        try:
            del tmp_dict[tax]
        except KeyError:
            pass
    filteredScrape.new_seqs_otu_id = tmp_dict
    expected_add = 1
    assert expected_add == len(filteredScrape.new_seqs_otu_id)
    sys.stdout.write("todo: add check that newly added seq are checked. they are, but there is no test")
