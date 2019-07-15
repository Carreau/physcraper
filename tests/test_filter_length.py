import os
import json
import sys
import pickle
from physcraper import wrappers, OtuJsonDict, ConfigObj, IdDicts, generate_ATT_from_files
from physcraper.filterblast import FilterBlast

#
from pytest import mark

localblast = mark.localblast

@localblast
def test_filter_length():

    workdir = "tests/output/test_selectbylength"
    absworkdir = os.path.abspath(workdir)
    conf = ConfigObj("tests/data/test.config", interactive=False)
    threshold = 2
    selectby = "length"
    downtorank = "species"
    add_unpubl_seq = None
    blacklist=None
                    
    id_to_spn_addseq_json=None
    ingroup_mrca=None
    shared_blast_folder=None
     
    data_obj = pickle.load(open("tests/data/precooked/tiny_dataobj.p", 'rb'))
    data_obj.workdir = absworkdir
    ids = IdDicts(conf, workdir=data_obj.workdir)
    ids.acc_ncbi_dict = pickle.load(open("tests/data/precooked/tiny_acc_map.p", "rb"))

    # Now combine the data, the ids, and the configuration into a single physcraper scrape object
    filteredScrape = FilterBlast(data_obj, ids)
    filteredScrape.add_setting_to_self(downtorank, threshold)
    filteredScrape.blacklist = blacklist

    sys.stdout.write("BLASTing input sequences\n")
    if shared_blast_folder:
        filteredScrape.blast_subdir = shared_blast_folder
    else:
        shared_blast_folder = None
    # filteredScrape.run_blast_wrapper()
    filteredScrape.read_blast_wrapper(blast_dir="tests/data/precooked/fixed/tte_blast_files")
    filteredScrape.remove_identical_seqs()
    filteredScrape.dump()
    sys.stdout.write("Filter the sequences\n")
    length_unfiltered = len(filteredScrape.new_seqs)

    if threshold is not None:
        filteredScrape.sp_dict(downtorank)
        filteredScrape.make_sp_seq_dict()
        filteredScrape.how_many_sp_to_keep(selectby=selectby)
        filteredScrape.replace_new_seq()

    length_filtered = len(filteredScrape.new_seqs)

    assert length_filtered != length_unfiltered

test_filter_length()