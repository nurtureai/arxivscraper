"""
A python program to retreive recrods from ArXiv.org in given
categories and specific date range.

Author: Mahdi Sadjadi (sadjadi.seyedmahdi[AT]gmail[DOT]com)., James tan(c00lways[AT]gmail[DOT]com)
"""
from __future__ import print_function
import xml.etree.ElementTree as ET
import datetime
import time
import sys
PYTHON3 = sys.version_info[0] == 3
if PYTHON3:
    from urllib.parse import urlencode
    from urllib.request import urlopen
    from urllib.error import HTTPError
else:
    from urllib import urlencode
    from urllib2 import HTTPError, urlopen
OAI = '{http://www.openarchives.org/OAI/2.0/}'
ARXIV = '{http://arxiv.org/OAI/arXiv/}'
BASE = 'http://export.arxiv.org/oai2?verb=ListRecords&'

class Record(object):
    """
    A class to hold a single record from ArXiv
    Each records contains the following properties:

    object should be of xml.etree.ElementTree.Element.
    """

    def __init__(self, xml_record):
        """if not isinstance(object,ET.Element):
        raise TypeError("")"""
        self.xml = xml_record
        self.id = self._get_text(ARXIV, 'id')
        self.url = 'https://arxiv.org/abs/' + self.id
        self.title = self._get_text(ARXIV, 'title')
        self.abstract = self._get_text(ARXIV, 'abstract')
        self.cats = self._get_text(ARXIV, 'categories').split(" ")
        self.pdf = "https://arxiv.org/pdf/" + self.id + ".pdf"
        self.created = self._get_text(ARXIV, 'created')
        self.updated = self._get_text(ARXIV, 'updated')
        self.doi = self._get_text(ARXIV, 'doi')
        self.authors = self._get_authors()

    def _get_text(self, namespace, tag):
        """Extracts text from an xml field"""
        try:
            return self.xml.find(namespace + tag).text.strip().lower().replace('\n', '')
        except:
            return ''

    def _get_authors(self):
        authors = self.xml.findall(ARXIV + 'authors/' + ARXIV + 'author')
        res = []
        for author in authors:
            fornamesDom = author.find(ARXIV + 'forenames')
            keynameDom  = author.find(ARXIV + 'keyname')
            # print("forname", fornamesDom, "keyname", keynameDom)
            res.append({'keyname': None if keynameDom == None else keynameDom.text.lower(), 'forenames': None if fornamesDom == None else fornamesDom.text.lower() })
        return res

    def output(self):
        d = {'title': self.title,
         'id': self.id,
         'abstract': self.abstract,
         'categories': self.cats,
         'doi': self.doi,
         'created': self.created,
         'updated': self.updated,
         'authors': self.authors,
         'url': self.url,
         'pdf': self.pdf}
        return d


class Scraper(object):
    """
    A class to hold info about attributes of scraping,
    such as date range, categories, and number of returned
    records. If `from` is not provided, the first day of
    the current month will be used. If `until` is not provided,
    the current day will be used.

    Paramters
    ---------
    category: str
    The category of scraped records
    data_from: str
    starting date in format 'YYYY-MM-DD'. Updated eprints are included even if
    they were created outside of the given date range. Default: first day of current month.
    date_until: str
    final date in format 'YYYY-MM-DD'. Updated eprints are included even if
    they were created outside of the given date range. Default: today.
    t: int
    Waiting time between subsequent calls to API, triggred by Error 503.
    filter: dictionary
    A dictionary where keys are used to limit the saved results. Possible keys:
    subcats, author, title, abstract. See the example, below.

    Example:
    Returning all eprints from
    """

    def __init__(self, category, date_from=None, date_until=None, t=30, filters={}):
        self.cat = str(category)
        self.t = t
        self.offset = 0
        self.nextUrl = ""
        DateToday = datetime.date.today()
        if date_from is None:
            self.f = str(DateToday.replace(day=1))
        else:
            self.f = date_from
        if date_until is None:
            self.u = str(DateToday)
        else:
            self.u = date_until
        self.url = BASE + 'from=' + self.f + '&until=' + self.u + '&metadataPrefix=arXiv&set=%s' % self.cat
        self.filters = filters
        if not self.filters:
            self.append_all = True
        else:
            self.append_all = False
            self.keys = filters.keys()

    def hasNext(self):
        return self.nextUrl != ""

    def next(self, limit=-1):
        t0 = time.time()
        sys.stdout.flush()
        ds = []
        k = 0

        url = self.nextUrl
        while True:
            print("continue fetch: ", self.offset, " for ", limit, url)
            sys.stdout.flush()
            try:
                response = urlopen(url)
                if 1==1:
                    break
            except HTTPError as e:
                if e.code == 503:
                    to = int(e.hdrs.get('retry-after', 30))
                    print('Got 503. Retrying after {0:d} seconds.'.format(self.t))
                    time.sleep(to)
                    continue
                else:
                    raise

        xml = response.read()
        root = ET.fromstring(xml)
        hasError = root.findall("error")
        # print("has error? "+str(len(hasError)))
        if len(hasError) > 0:
            print("has error: "+xml.decode("utf-8"))
            raise "error xml"
        # print("xml:"+xml.decode("utf-8"))

        records = root.findall(OAI + 'ListRecords/' + OAI + 'record')
        print("records: ", len(records), "k", k)
        sys.stdout.flush()
        for record in records:
            meta = record.find(OAI + 'metadata').find(ARXIV + 'arXiv')
            record = Record(meta).output()
            if (limit == -1 or k < limit):
                if self.append_all:
                    ds.append(record)
                else:
                    save_record = False
                    for key in self.keys:
                        for word in self.filters[key]:
                            if word.lower() in record[key]:
                                save_record = True

                    if save_record:
                        ds.append(record)
            k +=1
            if limit >= 0 and k >= limit:
                break# skip after max reached
        
        listRecords = root.find(OAI + 'ListRecords')
        if listRecords is None:
            print("ListRecords not found", xml.decode("utf-8"))
            sys.stdout.flush()
            return ds

        if limit >= 0 and k + 1 > limit:
            print("reached limit", k+1, limit)
            sys.stdout.flush()
        else:
            token = listRecords.find(OAI + 'resumptionToken')
            if token is None or token.text is None:
                self.nextUrl = ""
            else:
                url = BASE + 'resumptionToken=%s' % token.text
                self.nextUrl = url

        print("next size: ", len(ds))
        self.offset += k
        # end while
        t1 = time.time()
        print('fetching is completes in {0:.1f} seconds, offset: '.format(t1 - t0), self.offset)
        sys.stdout.flush()
        return ds

    def scrape(self, limit=-1, start=0):
        self.offset = start
        t0 = time.time()
        # url = self.url +"&max_results="+str(limit)+"&start="+str(start)
        url = self.url
        
        print("fetching: ", start, "/", limit, url)
        sys.stdout.flush()
        ds = []
        k = 0
        while True:
            sys.stdout.flush()
            try:
                response = urlopen(url)
            except SocketError as e:
                print("socker error, retrying...")
                time.sleep(2)
                continue
            except HTTPError as e:
                if e.code == 503:
                    to = int(e.hdrs.get('retry-after', 30))
                    print('Got 503. Retrying after {0:d} seconds.'.format(self.t))
                    time.sleep(to)
                    continue
                else:
                    raise

            xml = response.read()
            root = ET.fromstring(xml)
            hasError = root.findall("error")
            # print("has error? "+str(len(hasError)))
            if len(hasError) > 0:
                print("has error: "+xml.decode("utf-8"))
                raise "error xml"
            # print("xml:"+xml.decode("utf-8"))

            records = root.findall(OAI + 'ListRecords/' + OAI + 'record')
            print("records: ", len(records), "k", k)
            sys.stdout.flush()
            if k >= start:
                for record in records:
                    meta = record.find(OAI + 'metadata').find(ARXIV + 'arXiv')
                    record = Record(meta).output()
                    if k >= start and (limit == -1 or k < start+limit):
                        if self.append_all:
                            ds.append(record)
                        else:
                            save_record = False
                            for key in self.keys:
                                for word in self.filters[key]:
                                    if word.lower() in record[key]:
                                        save_record = True

                            if save_record:
                                ds.append(record)
                    k +=1
                    if limit >= 0 and k >= start+limit:
                        break# skip after max reached
                
                listRecords = root.find(OAI + 'ListRecords')
                if listRecords is None:
                    print("ListRecords not found", xml.decode("utf-8"))
                    sys.stdout.flush()
                    return ds
            else:
                k += len(records)# skipped

            if limit >= 0 and k + 1 > start+limit:
                print("reached limit", k+1, start+limit)
                sys.stdout.flush()
                break

            token = listRecords.find(OAI + 'resumptionToken')
            if token is None or token.text is None:
                self.nextUrl = ""
                break
            else:
                url = BASE + 'resumptionToken=%s' % token.text
                self.nextUrl = url

            if 1==1:
                break# use next to continue
        
        self.offset += k
        # end while
        t1 = time.time()
        print('fetching is completes in {0:.1f} seconds.'.format(t1 - t0))
        sys.stdout.flush()
        return ds


def search_all(df, col, *words):
    """
    Return a sub-DataFrame of those rows whose Name column match all the words.
    source: https://stackoverflow.com/a/22624079/3349443
    """
    return df[np.logical_and.reduce([df[col].str.contains(word) for word in words])]


cats = [
 'astro-ph', 'cond-mat', 'gr-qc', 'hep-ex', 'hep-lat', 'hep-ph', 'hep-th',
 'math-ph', 'nlin', 'nucl-ex', 'nucl-th', 'physics', 'quant-ph', 'math', 'CoRR', 'q-bio',
 'q-fin', 'stat']
subcats = {'cond-mat': ['cond-mat.dis-nn', 'cond-mat.mtrl-sci', 'cond-mat.mes-hall',
              'cond-mat.other', 'cond-mat.quant-gas', 'cond-mat.soft', 'cond-mat.stat-mech',
              'cond-mat.str-el', 'cond-mat.supr-con'],
 'hep-th': [],'hep-ex': [],'hep-ph': [],
 'gr-qc': [],'quant-ph': [],'q-fin': ['q-fin.CP', 'q-fin.EC', 'q-fin.GN',
           'q-fin.MF', 'q-fin.PM', 'q-fin.PR', 'q-fin.RM', 'q-fin.ST', 'q-fin.TR'],

 'nucl-ex': [],'CoRR': [],'nlin': ['nlin.AO', 'nlin.CG', 'nlin.CD', 'nlin.SI',
          'nlin.PS'],
 'physics': ['physics.acc-ph', 'physics.app-ph', 'physics.ao-ph',
             'physics.atom-ph', 'physics.atm-clus', 'physics.bio-ph', 'physics.chem-ph',
             'physics.class-ph', 'physics.comp-ph', 'physics.data-an', 'physics.flu-dyn',
             'physics.gen-ph', 'physics.geo-ph', 'physics.hist-ph', 'physics.ins-det',
             'physics.med-ph', 'physics.optics', 'physics.ed-ph', 'physics.soc-ph',
             'physics.plasm-ph', 'physics.pop-ph', 'physics.space-ph'],
 'math-ph': [],
 'math': ['math.AG', 'math.AT', 'math.AP', 'math.CT', 'math.CA', 'math.CO',
          'math.AC', 'math.CV', 'math.DG', 'math.DS', 'math.FA', 'math.GM', 'math.GN',
          'math.GT', 'math.GR', 'math.HO', 'math.IT', 'math.KT', 'math.LO', 'math.MP',
          'math.MG', 'math.NT', 'math.NA', 'math.OA', 'math.OC', 'math.PR', 'math.QA',
          'math.RT', 'math.RA', 'math.SP', 'math.ST', 'math.SG'],
 'q-bio': ['q-bio.BM',
           'q-bio.CB', 'q-bio.GN', 'q-bio.MN', 'q-bio.NC', 'q-bio.OT', 'q-bio.PE', 'q-bio.QM',
           'q-bio.SC', 'q-bio.TO'],
 'nucl-th': [],'stat': ['stat.AP', 'stat.CO', 'stat.ML',
          'stat.ME', 'stat.OT', 'stat.TH'],
 'hep-lat': [],'astro-ph': ['astro-ph.GA',
              'astro-ph.CO', 'astro-ph.EP', 'astro-ph.HE', 'astro-ph.IM', 'astro-ph.SR']
 }
