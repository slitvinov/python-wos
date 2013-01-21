import re
import operator

linefile = open('savedrecs.txt', 'r').read()
records = re.split("\nER", linefile)
records = records[:-1]

def records2list(records):
    lrec = []
    for crec in records:
        keys = re.split("([\n^][A-Z][A-Z0-9])", crec)
        keys.pop(0)
        rec = {}
        for (ke, el) in zip( keys[::2], keys[1::2]):
            lkey = ke.replace("\n", "")
            if lkey=="AF":
                rec[lkey] = [e.strip() for e in el.split("\n")]
            else:
                rec[lkey] = el
        lrec.append(rec)
    return lrec

def parsec1(c1, au):
    """Find affilation of the author"""
    for aff in c1.split("\n"):
        aff_parts = aff.split("]")
        if len(aff_parts)==1:
            return aff
        else:
            author_list = aff_parts[0].replace("[", "").split(";")
            for cauth in author_list:
                if au==cauth.strip():
                    return aff_parts[1].strip()
    # we did not find any affiliations
    return ""

def findrec(rlist, key, val):
    """Find a record with key matching val"""
    r = []
    for i, records in enumerate(rlist):
        if key in records:
            if re.search(val, records[key]):
                r.append(i)
    return r

def author2c1(rlist, au):
    """Returns a list of author's affilcations"""
    c1list = []
    for record in rlist:
        alit = record["AF"]
        if au in alit:
            c1list.append(parsec1(record["C1"], au))
    return c1list

def filteraff(afflist):
    """Filter matching affilations"""
    aff_return = []
    key_set = set()
    for aff in afflist:
        # define key function
        key = aff[:20]
        if not (key in key_set):
            aff_return.append(aff)
            key_set.add(key)
    return aff_return

def sortbyauthors(rlist):
    """Returns a list of authors sorted by number of publications"""
    adict = {}
    for record in rlist:
        alit = record["AF"]
        for au in alit:
            if au in adict:
                adict[au]=adict[au]+1
            else:
                adict[au]=1
    sorted_adict = sorted(adict.iteritems(), key=operator.itemgetter(1))
    return sorted_adict

rlist = records2list(records)
sa = sortbyauthors(rlist)
l = author2c1(rlist, "Barron, Annelise E.")
filteraff(l)

c1= "[Staples, J. Kenneth; Oshaben, Kaylyn M.; Horne, W. Seth] Univ Pittsburgh, Dept Chem, Pittsburgh, PA 15260 USA."
au= "Staples, J. Kenneth"
parsec1(c1, au)

c1 = rlist[23]["C1"]
au = rlist[23]["AF"][3]
parsec1(c1, au)

c1 = rlist[23]["C1"]
au = rlist[23]["AF"][1]
parsec1(c1, au)

l = author2c1(rlist, "Barron, Annelise E.")
l = filteraff(l)
for el in l:
    print el
