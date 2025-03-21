"""Classes and functions to work with OpenITI URIs


Todo:
    * make the print output look nicer
    * reflow texts + insert milestones?
    * compare with Maxim's script: _add_new_text_from_folder.py
      in maintenance repo


The Module contains a URI class that represents an OpenITI URI as an object.
The URI class's methods allow

* Checking whether all components of the URI are valid
* Accessing and changing components of the URI
* Getting the URI's current uri_type ("author", "book", "version", None)
* Building different versions of the URI ("author", "book", etc.)
* Building paths based on the URI

In addition to the URI class, the module contains a number of functions for
implementing URI changes in the OpenITI corpus



Examples:
    The Module contains a URI class that represents an OpenITI URI as an object.
    By calling the URI class, you create an instance of the URI class

    >>> from uri import URI
    >>> instance1 = URI("0255Jahiz.Bayan")
    >>> instance2 = URI("0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed")

    The URI instance inherits all the URI class's methods and properties:

    - Making string representations of a URI instance: print() and repr():

    >>> t = URI("0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed")
    >>> print(repr(t))
    uri(date:0255, author:Jahiz, title:Hayawan, version:Sham19Y0023775, language:ara, edition_no:1, extension:completed)
    >>> print(t)
    0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed

    - Accessing components of the URI:

    >>> t.author
    'Jahiz'
    >>> t.date
    '0255'

    - Changing components of the URI by setting properties to a new value:

    >>> u = URI("0255Jahiz.Hayawan")
    >>> u.author = "JahizBasri"
    >>> print(u)
    0255JahizBasri.Hayawan

    - Validity tests: setting invalid values for part of a uri returns an error\
    (implemented for instantiation of URI objects + setting URI components)::

        # >>> URI("255Jahiz")
        Exception: Date Error: URI must start with a date of 4 digits (255 has 3!)

        # >>> URI("0255Jāḥiẓ")
        Exception: Author name Error: Author name (Jāḥiẓ) should not contain
        digits or non-ASCII characters(culprits: ['ā', 'ḥ', 'ẓ'])

        # >>> t.author = "Jāḥiẓ"
        Exception: Author name Error: Author name (Jāḥiẓ) should not contain
        digits or non-ASCII characters(culprits: ['ā', 'ḥ', 'ẓ'])

        # >>> t.author = "0255Jahiz"
        Exception: Author name Error: Author name (0255Jahiz) should not contain
        digits or non-ASCII characters(culprits: ['0', '2', '5', '5'])

        # >>> URI("0255Jahiz.Al-Hayawan")
        Exception: Book title Error: Book title (Al-Hayawan) should not contain
        non-ASCII characters(culprits: ['-'])

        # >>> URI("0255Jahiz.Hayawan.Shāmila00123545-ara1")
        Exception: Version string Error: Version string (Shāmila00123545)
        should not contain non-ASCII characters(culprits: ['ā'])

        # >>> URI("0255Jahiz.Hayawan.Shamela00123545-arab1")
        Exception: Language code (arab) should be an ISO 639-2 language code,
        consisting of 3 characters

        # >>> t.extension = "markdown"
        Exception: Extension (markdown) is not among the allowed extensions
        (['inProgress', 'completed', 'mARkdown', 'yml', ''])

        # >>> URI("0255Jahiz.Hayawan.Shamela00123545-ara1.markdown")
        Exception: Extension (markdown) is not among the allowed extensions
        (['inProgress', 'completed', 'mARkdown', 'yml', ''])

    - Getting the URI's current uri_type ("author", "book", "version", None),\
    i.e., the longest URI that can be built from the object's components:

    >>> t.uri_type
    'version'
    >>> t.language = ""
    >>> t.uri_type
    'book'
    >>> t.date = ""
    >>> t.uri_type == None
    True

    - Building different versions of the URI\
    (uri_types: "author", "author_yml", "book", "book_yml",\
    "version", "version_yml", "version_file"):

    >>> t = URI("0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed")
    >>> t.build_uri(uri_type="author")
    '0255Jahiz'
    >>> t.build_uri("book")
    '0255Jahiz.Hayawan'
    >>> t.build_uri("book_yml")
    '0255Jahiz.Hayawan.yml'
    >>> t.build_uri("version")
    '0255Jahiz.Hayawan.Sham19Y0023775-ara1'
    >>> t.build_uri("version_file")
    '0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed'

    Simply calling the URI object (i.e., writing parentheses after
    the variable name works as an alias for the build_uri function:

    >>> t = URI("0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed")
    >>> t(uri_type="author")
    '0255Jahiz'
    >>> t("book")
    '0255Jahiz.Hayawan'
    >>> t("book_yml")
    '0255Jahiz.Hayawan.yml'
    >>> t("version")
    '0255Jahiz.Hayawan.Sham19Y0023775-ara1'
    >>> t("version_file")
    '0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed'


    - Building paths based on the URI:

    >>> t.build_pth(uri_type="version", base_pth="D:\\test")
    'D:/test/0275AH/data/0255Jahiz/0255Jahiz.Hayawan'
    >>> t.build_pth(uri_type="version_file", base_pth="D:\\test")
    'D:/test/0275AH/data/0255Jahiz/0255Jahiz.Hayawan/0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed'
    >>> t.build_pth("version")
    './0275AH/data/0255Jahiz/0255Jahiz.Hayawan'
    >>> t.build_pth(uri_type="book_yml")
    './0275AH/data/0255Jahiz/0255Jahiz.Hayawan/0255Jahiz.Hayawan.yml'

    Without uri_type argument, build_pth() builds the fullest path it can:

    >>> t.build_pth()
    './0275AH/data/0255Jahiz/0255Jahiz.Hayawan/0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed'
    >>> t.language=""  # (removing the language property makes it impossible to build a version uri)
    >>> t.build_pth()
    './0275AH/data/0255Jahiz/0255Jahiz.Hayawan'

    NB: by default, build_pth() takes the OpenITI folder structure into account,
    in which authors are grouped in 25-year batches by their death date.
    If you do not want to use this feature, set the URI class's
    data_in_25_year_repos attribute to False:

    >>> t.build_pth()
    './0275AH/data/0255Jahiz/0255Jahiz.Hayawan'
    >>> t.data_in_25_year_repos = False
    >>> t.build_pth()
    './0255Jahiz/0255Jahiz.Hayawan'
    >>> t.data_in_25_year_repos = True
    
    >>> URI.data_in_25_year_repos = False
    >>> u = URI("0255Jahiz.Hayawan")
    >>> u.build_pth()
    './0255Jahiz/0255Jahiz.Hayawan'
    >>> URI.data_in_25_year_repos = True
    >>> u.build_pth()
    './0275AH/data/0255Jahiz/0255Jahiz.Hayawan'

    ---------------------------------------------------------------------------


    In addition to the URI class, the module contains a function for    
    implementing URI changes in the OpenITI corpus: change_uri.
    
    The function has an *execute* flag. If set to False,\
    the function will not immediately be executed but first show all changes\
    it will make, and then ask the user whether to carry out the changes or not.
    
    If a version URI changes:
    
        * new author and book folders are made if necessary
          (including the creation of new author and book yml files)
        * all text files related that version should be moved
        * the yml file of that version should be updated and moved
        
    If a book uri changes:
    
        * new author and book folders are made if necessary
        * the yml file of that book should be updated and moved
        * all text files of all versions of the book should be moved
        * all yml files of versions of that book should be updated and moved
        * the original book folder itself should be (re)moved
        
    if an author uri changes:

        * new author and book folders are made if necessary
        * the yml file of that author should be updated and moved
        * all book yml files of that should be updated and moved
        * all annotation text files of all versions of all books should be moved
        * all yml files of versions of all books should be updated and moved
        * the original book folders should be (re)moved
        * the original author folder itself should be (re)moved

    Examples::
    
        change_uri("0255Jahiz", "0256Jahiz")
        change_uri("0255Jahiz", "0255JahizBasri")
        change_uri("0255Jahiz.Hayawan", "0255Jahiz.KitabHayawan")
        change_uri("0255Jahiz.Hayawan.Shamela002526-ara1",
                   "0255Jahiz.Hayawan.Shamela002526-ara2")
        change_uri("0255Jahiz.Hayawan.Shamela002526-ara1.completed",
                   "0255Jahiz.Hayawan.Shamela002526-ara1.mARkdown")
"""

import copy
import os
import re
import shutil

if __name__ == '__main__':
    from os import sys, path
    root_folder = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
    sys.path.append(root_folder)

from openiti.helper.funcs import read_header, get_all_yml_files_in_folder, get_all_text_files_in_folder
from openiti.helper.ara import ar_cnt_file
from openiti.helper.templates import author_yml_template, book_yml_template, \
                                     version_yml_template, readme_template, \
                                     text_questionnaire_template
from openiti.helper import yml


os.sep = "/"
ISO_CODES = re.split("[\n\r\s]+",
                     """aar abk ace ach ada ady afa afh afr ain aka akk alb sqi
ale alg alt amh ang anp apa ara arc arg arm hye arn arp art arw asm ast ath aus
ava ave awa aym aze bad bai bak bal bam ban baq eus bas bat bej bel bem ben ber
bho bih bik bin bis bla bnt tib bod bos bra bre btk bua bug bul bur mya byn cad
cai car cat cau ceb cel cze ces cha chb che chg chi zho chk chm chn cho chp chr
chu chv chy cmc cnr cop cor cos cpe cpf cpp cre crh crp csb cus wel cym cze ces
dak dan dar day del den ger deu dgr din div doi dra dsb dua dum dut nld dyu dzo
efi egy eka gre ell elx eng enm epo est baq eus ewe ewo fan fao per fas fat fij
fil fin fiu fon fre fra fre fra frm fro frr frs fry ful fur gaa gay gba gem geo
kat ger deu gez gil gla gle glg glv gmh goh gon gor got grb grc gre ell grn gsw
guj gwi hai hat hau haw heb her hil him hin hit hmn hmo hrv hsb hun hup arm hye
iba ibo ice isl ido iii ijo iku ile ilo ina inc ind ine inh ipk ira iro ice isl
ita jav jbo jpn jpr jrb kaa kab kac kal kam kan kar kas geo kat kau kaw kaz kbd
kha khi khm kho kik kin kir kmb kok kom kon kor kos kpe krc krl kro kru kua kum
kur kut lad lah lam lao lat lav lez lim lin lit lol loz ltz lua lub lug lui lun
luo lus mac mkd mad mag mah mai mak mal man mao mri map mar mas may msa mdf mdr
men mga mic min mis mac mkd mkh mlg mlt mnc mni mno moh mon mos mao mri may msa
mul mun mus mwl mwr bur mya myn myv nah nai nap nau nav nbl nde ndo nds nep new
nia nic niu dut nld nno nob nog non nor nqo nso nub nwc nya nym nyn nyo nzi oci
oji ori orm osa oss ota oto paa pag pal pam pan pap pau peo per fas phi phn pli
pol pon por pra pro pus qaa qtz que raj rap rar roa roh rom rum ron rum ron run
rup rus sad sag sah sai sal sam san sas sat scn sco sel sem sga sgn shn sid sin
sio sit sla slo slk slo slk slv sma sme smi smj smn smo sms sna snd snk sog som
son sot spa alb sqi srd srn srp srr ssa ssw suk sun sus sux swa swe syc syr tah
tai tam tat tel tem ter tet tgk tgl tha tib bod tig tir tiv tkl tlh tli tmh tog
ton tpi tsi tsn tso tuk tum tup tur tut tvl twi tyv udm uga uig ukr umb und urd
uzb vai ven vie vol vot wak wal war was wel cym wen wln wol xal xho yao yap yid
yor ypk zap zbl zen zgh zha chi zho znd zul zun zxx zza""")

extensions = ["inProgress", "completed", "mARkdown", "yml", "",
              "pdf", "zip", "rar"]

created_folders = []
created_ymls = []

class URI:
    """
    A class that represents the OpenITI URI as a Python object.

    OpenITI URIs consist of the following elements:
    0768IbnMuhammadTaqiDinBaclabakki.Hadith.Shamela0009426-ara1.mARkdown
    
        * VersionURI: consists of
        
          - EditionURI: consists of
          
            * Work URI: consists of
            
              - AuthorID: consists of
              
                * author's death date (self.date): 0768
                * shuhra of the author (self.author): IbnMuhammadTaqiDinBaclabakki
                
              - BookID (self.title): Hadith: short title of the book
              
            * Version URI: consists of
            
              - VersionID (self.version): Shamela0009426: ID of the collection/contributor
                from which we got the book + number of the book in that collection
                
              - Lang:
              
                * self.language: ara: ISO 639-2 language code
                * self.edition_no: 1: edition version number
                  (different digitizations of the same edition get the same edition_no)
                  
        * self.extension = mARkdown (can be inProgress, mARkdown, completed, "")

    Examples:
        >>> from uri import URI
        >>> t = URI("0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed")

        Representations of a URI object: print() and repr():

        >>> print(repr(t))
        uri(date:0255, author:Jahiz, title:Hayawan, version:Sham19Y0023775, language:ara, edition_no:1, extension:completed)
        >>> print(t)
        0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed

        Accessing components of the URI:
        
        >>> t.author
        'Jahiz'
        >>> t.date
        '0255'

        Getting URI's current uri_type ("author", "book", "version", None),
        i.e., the longest URI that can be built from the object's components:

        >>> t.uri_type
        'version'
        >>> t.language = ""
        >>> t.uri_type
        'book'
        >>> t.date = ""
        >>> t.uri_type == None
        True

        Building different versions of the URI
        (uri_types: "author", "author_yml", "book", "book_yml",
        "version", "version_yml", "version_file"):

        >>> t = URI("0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed")
        >>> t.build_uri(uri_type="author")
        '0255Jahiz'
        >>> t.build_uri("book")
        '0255Jahiz.Hayawan'
        >>> t.build_uri("book_yml")
        '0255Jahiz.Hayawan.yml'
        >>> t.build_uri("version")
        '0255Jahiz.Hayawan.Sham19Y0023775-ara1'
        >>> t.build_uri("version_file")
        '0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed'

        Building paths based on the URI:

        >>> t.build_pth(uri_type="version", base_pth="D:\\test")
        'D:/test/0275AH/data/0255Jahiz/0255Jahiz.Hayawan'
        >>> t.build_pth(uri_type="version_file", base_pth="D:\\test")
        'D:/test/0275AH/data/0255Jahiz/0255Jahiz.Hayawan/0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed'
        >>> t.build_pth("version")
        './0275AH/data/0255Jahiz/0255Jahiz.Hayawan'
        >>> t.build_pth(uri_type="book_yml")
        './0275AH/data/0255Jahiz/0255Jahiz.Hayawan/0255Jahiz.Hayawan.yml'

        Without uri_type argument, build_pth() builds the fullest path it can:

        >>> t.build_pth()
        './0275AH/data/0255Jahiz/0255Jahiz.Hayawan/0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed'
        >>> t.language=""  # (removing the language property makes it impossible to build a version uri)
        >>> t.build_pth()
        './0275AH/data/0255Jahiz/0255Jahiz.Hayawan'

        NB: by default, build_pth() takes the OpenITI folder structure
        into account, in which authors are grouped in 25-year batches
        by their death date.
        If you do not want to use this feature, set the URI class's
        data_in_25_year_repos attribute to False:

        >>> t.build_pth()
        './0275AH/data/0255Jahiz/0255Jahiz.Hayawan'
        >>> t.data_in_25_year_repos = False
        >>> t.build_pth()
        './0255Jahiz/0255Jahiz.Hayawan'
        >>> t.language="ara"
        >>> t.build_pth()
        './0255Jahiz/0255Jahiz.Hayawan'
        >>> t.data_in_25_year_repos = True
        
        >>> URI.data_in_25_year_repos = False
        >>> u = URI("0255Jahiz.Hayawan")
        >>> u.build_pth()
        './0255Jahiz/0255Jahiz.Hayawan'
        >>> URI.data_in_25_year_repos = True
        >>> u.build_pth()
        './0275AH/data/0255Jahiz/0255Jahiz.Hayawan'

        Validity tests: setting invalid values for part of a uri returns an error::

            # >>> URI("255Jahiz")
            Exception: Date Error: URI must start with a date of 4 digits (255 has 3!)
            
            # >>> URI("0255Jāḥiẓ")
            Exception: Author name Error: Author name (Jāḥiẓ) should not contain
            digits or non-ASCII characters(culprits: ['ā', 'ḥ', 'ẓ'])
            
            # >>> t.author = "Jāḥiẓ"
            Exception: Author name Error: Author name (Jāḥiẓ) should not contain
            digits or non-ASCII characters(culprits: ['ā', 'ḥ', 'ẓ'])
            
            # >>> t.author = "0255Jahiz"
            Exception: Author name Error: Author name (0255Jahiz) should not contain
            digits or non-ASCII characters(culprits: ['0', '2', '5', '5'])
            
            # >>> URI("0255Jahiz.Al-Hayawan")
            Exception: Book title Error: Book title (Al-Hayawan) should not contain
            non-ASCII characters(culprits: ['-'])
            
            # >>> URI("0255Jahiz.Hayawan.Shāmila00123545-ara1")
            Exception: Version string Error: Version string (Shāmila00123545)
            should not contain non-ASCII characters(culprits: ['ā'])

            # >>> URI("0255Jahiz.Hayawan.Shamela00123545-arab1")
            Exception: Language code (arab) should be an ISO 639-2 language code,
            consisting of 3 characters

            # >>> t.extension = "markdown"
            Exception: Extension (markdown) is not among the allowed extensions
            (['inProgress', 'completed', 'mARkdown', 'yml', ''])

            # >>> URI("0255Jahiz.Hayawan.Shamela00123545-ara1.markdown")
            Exception: Extension (markdown) is not among the allowed extensions
            (['inProgress', 'completed', 'mARkdown', 'yml', ''])
    """

    def __init__(self, uri_string=None):
        """Initialize the URI object and its components: if a uri_string is provided,
        it will be split into its components.

        Args:
            uri_string (str): (a path to) an OpenITI URI, e.g.,
                0768IbnMuhammadTaqiDinBaclabakki.Hadith.Shamela0009426-ara1; 
                0768IbnMuhammadTaqiDinBaclabakki.Hadith; 
                0768IbnMuhammadTaqiDinBaclabakki; 
                D:\OpenITI\25Yrepos\data\0275AH\0255Jahiz. 
                Defaults to None

        Examples:
            >>> uri1 = URI("0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed")
            >>> uri2 = URI("0255Jahiz.Hayawan")
            >>> uri3 = URI()
            >>> uri4 = URI(r"D:\\OpenITI\\25Yrepos\\data\\0275AH\\0255Jahiz\\0255Jahiz.Hayawan\\0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed")
            >>> print(uri4)
            0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed
            >>> print(uri4.base_pth)
            D:/OpenITI/25Yrepos/data
        """
        try:
            self.data_in_25_year_repos
        except:
            self.data_in_25_year_repos = True
        #print("init: self.data_in_25_year_repos", self.data_in_25_year_repos)
        self.date = ""
        self.author = ""
        self.title = ""
        self.version = ""
        self.language = ""
        self.edition_no = ""
        self.extension = ""
        if uri_string:
            if len(re.split(r"[\\/]", uri_string)) > 1: # deal with paths:
                self.base_pth, self.uri_string = os.path.split(uri_string)
                if self.data_in_25_year_repos:
                    # set self.base_pth to the parent of the 25Y folder:
                    if re.search("\d{4}AH", self.base_pth):
                        while not re.search("\d{4}AH",
                                            os.path.split(self.base_pth)[1]):
                            self.base_pth = os.path.split(self.base_pth)[0]
                        self.base_pth = os.path.split(self.base_pth)[0]
                    else: # if there is no 25Y folder:
                        self.base_pth, self.uri_string = os.path.split(uri_string)
                else:
                    self.base_pth, self.uri_string = os.path.split(uri_string)
                    #print("init: establishing self.base_pth")
                    #print("  ", self.base_pth)
                    #print("  split:", os.path.split(self.base_pth))
                    while re.search("\d{4}[A-Za-z]",
                                    os.path.split(self.base_pth)[1]):
                        self.base_pth = os.path.split(self.base_pth)[0]
                        #print("   >", self.base_pth)
            else:
                self.uri_string = uri_string
            self.split_uri(self.uri_string)
        else:
            self.uri_string = ""
        # make it possible to set these values for every instance of the class:
        try:
            self.base_pth
        except: # if the base_pth has not been set before instantiating the class:
            self.base_pth = "."
        #print("init: self.base_pth", self.base_pth)



    ############################################################################
    # Setter and getter methods: intercept mistakes when setting URI properties:

    @property
    def date(self):
        """Get the URI's date property"""
        return self.__date

    @date.setter
    def date(self, date):
        """Set the URI's date property, after checking its conformity."""
        self.__date = self.check_date(date)

    def check_date(self, date):
        """Check if date is valid (i.e., 4-digit number or empty string)"""
        if date == "":
            return ""
        date = str(date)
        if len(date) != 4:
            msg = "Date Error: URI must start with a date of 4 digits "
            msg += "({} has {}!)".format(date, len(date))
            raise Exception(msg)
        return date


    @property
    def author(self):
        """Get the URI's author property"""
        return self.__author

    @author.setter
    def author(self, author):
        """Set the URI's author property, after checking its conformity."""
        self.__author = self.check_ASCII_letters(author, "Author name")

    def check_ASCII_letters(self, test_string, string_type):
        """Check whether the test_string only contains ASCII letters."""
        if re.findall("[^A-Za-z]", test_string):
            msg = "{0} Error: {0} ({1}) ".format(string_type, test_string)
            msg += "should not contain digits or non-ASCII characters"
            msg += "(culprits: {})".format(re.findall("[^A-Za-z]", test_string))
            raise Exception(msg)
        return test_string


    @property
    def title(self):
        """Get the URI's title property."""
        return self.__title

    @title.setter
    def title(self, title):
        """Set the URI's title property, after checking its conformity."""
        #self.__title = self.check_ASCII_letters(title, "Book title")
        self.__title = self.check_ASCII(title, "Book title")


    @property
    def version(self):
        """Set the URI's version property."""
        return self.__version

    @version.setter
    def version(self, version):
        """Set the URI's version property, after checking its conformity."""
        self.__version = self.check_ASCII(version, "Version string")

    def check_ASCII(self, test_string, string_type):
        """Check whether the test_string only contains ASCII letters and digits."""
        if re.findall("[^A-Za-z0-9]", test_string):
            msg = "{0} Error: {0} ({1}) ".format(string_type, test_string)
            msg += "should not contain non-ASCII characters"
            msg += "(culprits: {})".format(re.findall("[^A-Za-z0-9]", test_string))
            raise Exception(msg)
        return test_string


    @property
    def language(self):
        """Get the URI's language property (an ISO 639-2 language code)."""
        return self.__language

    @language.setter
    def language(self, language):
        """Set the URI's language property, after checking its conformity."""
        self.__language = self.check_language_code(language)

    def check_language_code(self, language):
        """Check whether language is a valid ISO 639-2 language code."""
        if language == "":
            return ""
        if not language in ISO_CODES:
            msg = "Language code ({}) ".format(language)
            msg += "should be an ISO 639-2 language code, consisting of 3 characters"
            raise Exception(msg)
        return language


    @property
    def edition_no(self):
        """Get the URI's edition_no property (i.e., the last digit of the URI)"""
        return self.__edition_no

    @edition_no.setter
    def edition_no(self, edition_no):
        """Set the URI's edition_no property, after checking its conformity."""
        self.__edition_no = edition_no


    @property
    def extension(self):
        """Get the URI's extension property."""
        return self.__extension

    @extension.setter
    def extension(self, extension):
        """Set the URI's extension property, after checking its conformity."""
        self.__extension = self.check_extension(extension)

    def check_extension(self, extension):
        """Check whether the proposed extension is allowed."""
        if extension not in extensions:
            msg = "Extension ({}) ".format(extension)
            msg += "is not among the allowed extensions ({})".format(extensions)
            raise Exception(msg)
        return extension


    @property
    def base_pth(self):
        """Get the URI's base_pth property (the path to be prepended to the URIs)
        (usually the folder in which the OpenITI 25-years repos reside)"""
        return self.__base_pth

    @base_pth.setter
    def base_pth(self, base_pth):
        """Set the URI's extension property, after checking its conformity."""
        self.__base_pth = self.check_base_pth(base_pth)

    def normpath(func):
        """replace backslashes by forward slashes also on Windows
        This is necessary to make the doctests behave the same way
        on Windows, Mac and Unix systems"""
        def normalize(*args, **kwargs):
            r = func(*args, **kwargs)
            return re.sub(r"\\+","/", r.encode('unicode-escape').decode())
        return normalize

    @normpath
    def check_base_pth(self, base_pth):
        """Check whether the base_pth is None, in wich case it is set to '.'"""
        if base_pth == None:
            return "."
        return base_pth

    @property
    def uri_type(self):
        """Get the URI object's current uri_type
        ("author", "book", "version", None) based on its defined components.

        NB: uri_type does not have a setter method, making it read-only!

        Examples:
            >>> my_uri = URI("0255Jahiz.Hayawan.Sham19Y0023775-ara1.inProgress")
            >>> my_uri.uri_type
            'version'
            >>> my_uri.language = ""
            >>> my_uri.uri_type
            'book'
            >>> my_uri = URI()
            >>> my_uri.uri_type is None
            True
        """
        uri_type = None
        if self.date and self.author:
            uri_type = "author"
            if self.title:
                uri_type = "book"
                if self.version and self.language and self.edition_no:
                    uri_type = "version"
        return uri_type

    ############################################################################

    def __call__(self, uri_type=None, ext=None):
        """Call the self.build_uri() method of the URI instance.

        Examples:
            >>> my_uri = URI("0768IbnMuhammadTaqiDinBaclabakki")
            >>> my_uri.title = "Hadith"
            >>> my_uri.version = "Shamela0009426"
            >>> my_uri.language = "ara"
            >>> my_uri.edition_no = "1"
            >>> my_uri()
            '0768IbnMuhammadTaqiDinBaclabakki.Hadith.Shamela0009426-ara1'
            >>> my_uri("date")
            '0768'
            >>> my_uri("author")
            '0768IbnMuhammadTaqiDinBaclabakki'
            >>> my_uri("author_yml")
            '0768IbnMuhammadTaqiDinBaclabakki.yml'
            >>> my_uri("book")
            '0768IbnMuhammadTaqiDinBaclabakki.Hadith'
            >>> my_uri("book_yml")
            '0768IbnMuhammadTaqiDinBaclabakki.Hadith.yml'
            >>> my_uri("version")
            '0768IbnMuhammadTaqiDinBaclabakki.Hadith.Shamela0009426-ara1'
            >>> my_uri("version_yml")
            '0768IbnMuhammadTaqiDinBaclabakki.Hadith.Shamela0009426-ara1.yml'
            >>> my_uri("version_file", ext="completed")
            '0768IbnMuhammadTaqiDinBaclabakki.Hadith.Shamela0009426-ara1.completed'
        """
        return self.build_uri(uri_type, ext)


    def __repr__(self):
        """Return a representation of the components of the URI.

        Returns:
            (str): a representation of the components of the URI.

        Examples:
            >>> my_uri = URI("0255Jahiz.Hayawan.Sham19Y0023775-ara1")
            >>> repr(my_uri)
            'uri(date:0255, author:Jahiz, title:Hayawan, version:Sham19Y0023775, \
language:ara, edition_no:1, extension:)'
            >>> my_uri = URI()
            >>> repr(my_uri)
            'uri(date:, author:, title:, version:, language:, edition_no:, extension:)'
        """
        component_names = "date author title version language edition_no extension"
        fmt = [x+":{_URI__"+x+"}" for x in component_names.split()]
        fmt = "uri({})".format(", ".join(fmt))
        return fmt.format(**self.__dict__)

    def __str__(self, *args, **kwargs):
        """Return the reassembled URI.

        Returns:
            (str): the reassembled URI

        Examples:
            >>> my_uri = URI("0255Jahiz.Hayawan.Sham19Y0023775-ara1.inProgress")
            >>> my_uri.extension = "completed"
            >>> print(my_uri)
            0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed
        """
        return self.build_uri()


    def __iter__(self):
        """Enable iteration over a URI object.

        Returns:
            (iterator): an iterator containing the components of the URI

        Examples:
            >>> my_uri = URI("0255Jahiz.Hayawan.Sham19Y0023775-ara1.inProgress")
            >>> for component in my_uri: print(component)
            0255
            Jahiz
            Hayawan
            Sham19Y0023775
            ara
            1
            inProgress
            >>> my_uri = URI()
            >>> for component in my_uri: print(component)

        """
        return iter(self.split_uri())
##        return iter([self.date, self.author, self.title, self.version,
##                     self.language, self.edition_no, self.extension])


    ############################################################################


##    def get_uri_type(self):
##        """Get the type of the URI object.
##
##        Examples:
##            >>> my_uri = URI("0255Jahiz.Hayawan.Sham19Y0023775-ara1.inProgress")
##            >>> my_uri.get_uri_type()
##            'version'
##            >>> my_uri = URI()
##            >>> my_uri.get_uri_type() is None
##            True
##        """
##        uri_type = None
##        if self.date and self.author:
##            uri_type = "author"
##            if self.title:
##                uri_type = "book"
##                if self.version and self.language and self.edition_no:
##                    uri_type = "version"
##        return uri_type

    def split_uri(self, uri_string=None):
        """
        Split an OpenITI URI string into its components and check if components are valid.

        Args:
            uri_string (str): OpenITI URI, e.g.,
                0768IbnMuhammadTaqiDinBaclabakki.Hadith.Shamela0009426-ara1

        Returns:
            (list): list of uri components

        Examples:
            >>> my_uri = URI("0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed")
            >>> my_uri.split_uri()
            ['0255', 'Jahiz', 'Hayawan', 'Sham19Y0023775', 'ara', '1', 'completed']
            >>> my_uri.extension=""
            >>> my_uri.language=""
            >>> my_uri.split_uri()
            ['0255', 'Jahiz', 'Hayawan']
        """
        if not uri_string:
            uri_string = self.build_uri()
        split_uri = uri_string.split(".")

        if split_uri == [""]:
            return []

        if len(split_uri) > 4:
            msg = "URI ({}) has too many parts separated by dots".format(uri_string)
            raise Exception(msg)

        self.dateAuth = split_uri[0]
        self.date = re.findall("^\d+", self.dateAuth)[0]
        self.check_date(self.date)
        self.author = self.dateAuth[4:]
        if not self.author:
            msg = "No author name found. \
Did you put a dot between date and author name?"
            raise Exception(msg)
        split_components = [self.date, self.author]

        if len(split_uri) > 1:
            if split_uri[1] != "yml":
                self.title = split_uri[1]
                split_components.append(self.title)

        if len(split_uri) > 2:
            if split_uri[2] != "yml":
                self.versionLang = split_uri[2]
                try:
                    self.version, language = self.versionLang.split("-")
                except:
                    raise Exception("URI () misses language ")
                self.check_ASCII(self.version, "Version ID")
                split_components.append(self.version)
                if language[-1].isnumeric():
                    self.edition_no = re.findall("\d+", language)[0]
                    self.language = re.sub("\d+", "", language)
                    split_components.append(self.language)
                    split_components.append(self.edition_no)
                else:
                    self.edition_no = ""
                    self.language = language
                    split_components.append(self.language)
                self.check_language_code(self.language)
        if len(split_uri) > 3:
            #if split_uri[3] != "yml":
            self.extension = split_uri[3]
            split_components.append(self.extension)
            #else:
##                print("ERROR: extension '{}' not in the list\
##of acceptable extensions. No extension recorded".format(split_uri[3]))
            #    self.extension = ""
        return split_components


    def build_uri(self, uri_type=None, ext=None):
        """
        Build an OpenITI URI string from its components.

        Args:
            uri_type (str): the uri type to be returned (defaults to None):
                - "date" : only the date (format: 0000)
                - "author" : authorUri (format: 0255Jahiz)
                - "author_yml" : filename of the author yml file\
                  (format: 0255Jahiz.yml)
                - "book": BookUri (format: 0255Jahiz.Hayawan)
                - "book_yml": filename of the book yml file\
                  (format: 0255Jahiz.Hayawan.yml)
                - "version": versionURI\
                  (format: 0255Jahiz.Hayawan.Shamela000245-ara1)
                - "version_yml": filename of the version yml file\
                  (format: 0255Jahiz.Hayawan.Shamela000245-ara1.yml)
                - "version_file": filename of the version text file\
                  (format: 0255Jahiz.Hayawan.Shamela000245-ara1.completed)
            ext (str): extension for the version_file uri string
                (can be "completed", "inProgress", "mARkdown", "" or None).

        Returns:
            (str): OpenITI URI as a string, e.g.,
                0768IbnMuhammadTaqiDinBaclabakki.Hadith.Shamela0009426-ara1

        Examples:
            >>> my_uri = URI("0768IbnMuhammadTaqiDinBaclabakki")
            >>> my_uri.title = "Hadith"
            >>> my_uri.version = "Shamela0009426"
            >>> my_uri.language = "ara"
            >>> my_uri.edition_no = "1"
            >>> my_uri.build_uri()
            '0768IbnMuhammadTaqiDinBaclabakki.Hadith.Shamela0009426-ara1'
            >>> my_uri.build_uri("date")
            '0768'
            >>> my_uri.build_uri("author")
            '0768IbnMuhammadTaqiDinBaclabakki'
            >>> my_uri.build_uri("author_yml")
            '0768IbnMuhammadTaqiDinBaclabakki.yml'
            >>> my_uri.build_uri("book")
            '0768IbnMuhammadTaqiDinBaclabakki.Hadith'
            >>> my_uri.build_uri("book_yml")
            '0768IbnMuhammadTaqiDinBaclabakki.Hadith.yml'
            >>> my_uri.build_uri("version")
            '0768IbnMuhammadTaqiDinBaclabakki.Hadith.Shamela0009426-ara1'
            >>> my_uri.build_uri("version_yml")
            '0768IbnMuhammadTaqiDinBaclabakki.Hadith.Shamela0009426-ara1.yml'
            >>> my_uri.build_uri("version_file", ext="completed")
            '0768IbnMuhammadTaqiDinBaclabakki.Hadith.Shamela0009426-ara1.completed'
        """
        self.uri_string = ""

        if not uri_type:
            if self.version and self.language:
                if self.extension:
                    return self.build_uri("version_file", ext=ext)
                else:
                    return self.build_uri("version", ext=ext)
            elif self.title:
                return self.build_uri("book", ext=ext)
            elif self.author:
                return self.build_uri("author", ext=ext)
            elif self.date:
                return self.build_uri("date", ext=ext)
            else:
                return ""

        if uri_type == "date":
            if self.date:
                self.uri_string = str(self.date)
            else:
                raise Exception("Error: the date component of the URI was not defined")
        elif "author" in uri_type:
            if self.author:
                self.uri_string = "{}{}".format(self.build_uri("date"),self.author)
            else:
                raise Exception("Error: the author component of the URI was not defined")
        elif "book" in uri_type:
            if self.title:
                self.uri_string = "{}.{}".format(self.build_uri("author"), self.title)
            else:
                raise Exception("Error: the title component of the URI was not defined")
        elif "version" in uri_type:
            if self.version and self.language:
                self.uri_string =  "{}.{}-{}{}".format(self.build_uri("book"),
                                                       self.version,
                                                       self.language,
                                                       self.edition_no)
                if "file" in uri_type:
                    if ext != None:
                        if ext != "":
                            self.uri_string += ".{}".format(ext)
                        # else: do not add an extension
                    else:
                        if self.extension:
                            self.uri_string += ".{}".format(self.extension)
            elif self.version:
                raise Exception("Error: the language component of the URI was not defined")
            elif self.language:
                raise Exception("Error: the version component of the URI was not defined")
            else:
                raise Exception("Error: the language and version components of the URI were not defined")
        if "yml" in uri_type:
            self.uri_string += ".yml"
        return self.uri_string

    def get_version_uri(self):
        """
        Returns the version uri.

        Returns:
            (str): OpenITI URI as a string, e.g.,
                0768IbnMuhammadTaqiDinBaclabakki.Hadith.Shamela0009426-ara1

        Example:
            >>> my_uri = URI('0768IbnMuhammadTaqiDinBaclabakki.Hadith.Shamela0009426-ara1')
            >>> my_uri.extension = "completed"
            >>> my_uri.get_version_uri()
            '0768IbnMuhammadTaqiDinBaclabakki.Hadith.Shamela0009426-ara1'
        """
        return self.build_uri("version")

    def get_book_uri(self):
        """
        Returns the book uri.

        Returns:
            uri_string (str): OpenITI URI as a string, e.g.,
                0768IbnMuhammadTaqiDinBaclabakki.Hadith

        Example:
            >>> my_uri = URI('0768IbnMuhammadTaqiDinBaclabakki.Hadith.Shamela0009426-ara1')
            >>> my_uri.get_book_uri()
            '0768IbnMuhammadTaqiDinBaclabakki.Hadith'
        """
        return self.build_uri("book")

    def get_author_uri(self):
        """
        Returns the author uri.

        Returns:
            uri_string (str): OpenITI URI as a string, e.g.,
                0768IbnMuhammadTaqiDinBaclabakki

        Example:
            >>> my_uri = URI('0768IbnMuhammadTaqiDinBaclabakki.Hadith.Shamela0009426-ara1')
            >>> my_uri.get_author_uri()
            '0768IbnMuhammadTaqiDinBaclabakki'
        """
        return self.build_uri("author")


    @normpath  # always use "/" as path separator, for use across Unix and Windows
    def build_pth(self, uri_type=None, base_pth=None):
        """build the path to a file or folder using the OpenITI uri system

        Args:
            uri_type (str): the uri type of the path to be returned
            (defaults to None):
                - "date" : only the 25-years openITI folder (format: 0275AH)
                - "author" : authorUri (format: 0255Jahiz)
                - "author_yml" : path to the author yml file
                    (format: 0275AH/0255Jahiz.yml)
                - "book": path to the book folder
                    (format: 0275AH/0255Jahiz/0255Jahiz.Hayawan)
                - "book_yml": path to the book yml file
                    (format: 0275AH/0255Jahiz/0255Jahiz.Hayawan/0255Jahiz.Hayawan.yml)
                - "version": path to the book folder
                    in which the version files reside
                    (format: 0275AH/0255Jahiz/0255Jahiz.Hayawan)
                - "version_yml": path to the version yml file
                    (format: 0275AH/data/0255Jahiz/0255Jahiz.Hayawan/0255Jahiz.Hayawan.Sham19Y0023775-ara1.yml)
                - "version_file": path to the version text file
                    (format: 0275AH/data/0255Jahiz/0255Jahiz.Hayawan/0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed)
            base_pth (str): path to the root folder,
                to be prepended to the URI path

        Returns:
            (str): relative/absolute path

        Examples:
            >>> my_uri = URI("0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed")
            >>> my_uri.build_pth(base_pth="./master", uri_type="date")
            './master/0275AH'
            >>> my_uri.build_pth(base_pth="./master", uri_type="author")
            './master/0275AH/data/0255Jahiz'
            >>> my_uri.build_pth(base_pth="./master", uri_type="author_yml")
            './master/0275AH/data/0255Jahiz/0255Jahiz.yml'
            >>> my_uri.build_pth(base_pth="./master", uri_type="book")
            './master/0275AH/data/0255Jahiz/0255Jahiz.Hayawan'
            >>> my_uri.build_pth(base_pth="./master", uri_type="book_yml")
            './master/0275AH/data/0255Jahiz/0255Jahiz.Hayawan/0255Jahiz.Hayawan.yml'
            >>> my_uri.build_pth(base_pth="./master", uri_type="version_file")
            './master/0275AH/data/0255Jahiz/0255Jahiz.Hayawan/0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed'
             >>> my_uri.build_pth(base_pth="./master", uri_type="version")
            './master/0275AH/data/0255Jahiz/0255Jahiz.Hayawan'
       """
        if base_pth is None:
            base_pth = self.base_pth
        #print("base_pth:", base_pth)

        if not uri_type:
            if self.version and self.language:
                if self.extension:
                    return self.build_pth(uri_type="version_file", base_pth=base_pth)
                else:
                    return self.build_pth(uri_type="version", base_pth=base_pth)
            elif self.title:
                return self.build_pth(uri_type="book", base_pth=base_pth)
            elif self.author:
                return self.build_pth(uri_type="author", base_pth=base_pth)
            elif self.date:
                return self.build_pth("date", base_pth)


        if uri_type == "date":
            if self.date:
                if str(self.date).endswith("AH"):
                    self.date=self.date[:-2]
                if int(self.date)%25:
                    d = "{:04d}AH".format((int(int(self.date)/25) + 1)*25)
                else:
                    d = "{:04d}AH".format(int(self.date))
                #p = os.path.join(base_pth, d)
                return os.sep.join((base_pth, d))
            else:
                raise Exception("Error: the date component of the URI was not defined")
        elif "author" in uri_type:
            if self.data_in_25_year_repos: 
                pth = os.sep.join((self.build_pth("date", base_pth), "data",
                                   self.build_uri("author")))
            else:
                pth = os.sep.join((base_pth, self.build_uri("author")))
        elif "book" in uri_type:
            pth = os.sep.join((self.build_pth("author", base_pth),
                                self.build_uri("book")))
        elif "version" in uri_type:
            pth = self.build_pth("book", base_pth)
##            if "yml" in uri_type or "file" in uri_type:
##                pth = (self.build_pth("book", base_pth))
##            else:
##                pth = os.sep.join((self.build_pth("book", base_pth),
##                                   self.build_uri("version")))
        if "yml" in uri_type or "file" in uri_type:
            return pth + os.sep + self.build_uri(uri_type)
        else:
            return pth

    def from_folder(self, folder):
        """Create a URI from a folder path without a file name."""
        # not yet implemented



################################################################################
# OpenITI corpus functions dependent on URIs:


def change_uri(old, new, old_base_pth=None, new_base_pth=None, execute=False):
    """Change a uri and put all files in the correct folder.

    If a version URI changes:
    
        * all text files of that version should be moved
        * the yml file of that version should be updated and moved
        
    If a book uri changes:
    
        * the yml file of that book should be updated and moved
        * all annotation text files of all versions of the book should be moved
        * all yml files of versions of that book should be updated and moved
        * the original book folder itself should be (re)moved
        
    if an author uri changes:

        * the yml file of that author should be updated and moved
        * all book yml files of that should be updated and moved
        * all annotation text files of all versions of all books should be moved
        * all yml files of versions of all books should be updated and moved
        * the original book folders should be (re)moved
        * the original author folder itself should be (re)moved

    Examples::
    
        change_uri("0255Jahiz", "0256Jahiz")
        change_uri("0255Jahiz", "0255JahizBasri")
        change_uri("0255Jahiz.Hayawan", "0255Jahiz.KitabHayawan")
        change_uri("0255Jahiz.Hayawan.Shamela002526-ara1",\
                   "0255Jahiz.Hayawan.Shamela002526-ara2")
        change_uri("0255Jahiz.Hayawan.Shamela002526-ara1.completed",\
                   "0255Jahiz.Hayawan.Shamela002526-ara1.mARkdown")

    Args:
        old (str): URI string to be changed
        new (str): URI string to which the new URI should be changed.
        old_base_pth (str): path to the folder containing the
            OpenITI 25-year repos, related to the old uri
        new_base_pth (str): path to the folder containing the
            OpenITI 25-year repos, related to the new uri
        execute (bool): if False, the proposed changes will only be printed
            (the user will still be given the option to execute
            all proposed changes at the end);
            if True, all changes will be executed immediately.

    Returns:
        None
    """
    print("old_base_pth:", old_base_pth)
    old_uri = URI(old)
    old_uri.base_pth = old_base_pth
    new_uri = URI(new)
    new_uri.base_pth = new_base_pth

    if not execute:
        print("old uri:", old)
        print("new uri:", new)
        print("Proposed changes:")
    old_folder = old_uri.build_pth()
    if new_uri.uri_type == "version":
        # only move yml and text file(s) of this specific version:
        for file in os.listdir(old_folder):
            fp = os.path.join(old_folder, file)
            if not file.endswith(".md"):
                if URI(file).build_uri(ext="") == old_uri.build_uri(ext=""):
                    if file.endswith(".yml"):
                        move_yml(fp, new_uri, "version", execute)
                    else:
                        old_file_uri = URI(fp)
                        new_uri.extension = old_file_uri.extension
                        move_to_new_uri_pth(fp, new_uri, execute)

        # add readme and text_questionnaire files:

        target_folder = new_uri.build_pth("version")
        if execute:
            if "README.md" not in os.listdir(target_folder):
                add_readme(target_folder)
            if "text_questionnaire.md" not in os.listdir(target_folder):
                add_text_questionnaire(target_folder)
        else:
            print("add/move readme and text questionnaire files")

    else: # move all impacted files and directories
        for root, dirs, files in os.walk(old_folder):
            for file in files:
                if file in ["README.md", "text_questionnaire.md"]:
                    # skip README and text_questionnaire files until last
                    # so we can use the uri of the other files to create path
                    pass
                else:
                    print()
                    print("* file:", file)
                    fp = os.path.join(root, file)
                    old_file_uri = URI(fp)
                    print("  (type: {})".format(old_file_uri.uri_type))
                    new_file_uri = copy.deepcopy(old_file_uri)
                    new_file_uri.base_pth = new_uri.base_pth
                    new_file_uri.date = new_uri.date
                    new_file_uri.author = new_uri.author
                    if new_uri.uri_type == "book":
                        new_file_uri.title = new_uri.title
                    if file.endswith(".yml"):
                        new_fp = move_yml(fp, new_file_uri,
                                          old_file_uri.uri_type, execute)
                    else:
                        new_fp = move_to_new_uri_pth(fp, new_file_uri, execute)

            # Deal with non-URI filenames last:

            for fn in ["README.md", "text_questionnaire.md"]:
                fp = os.path.join(root, fn)
                new_folder = os.path.split(new_fp)[0] # defined in previous loop
                new_fp = os.path.join(new_folder, fn)
                if os.path.exists(fp):
                    # if the old folder contained a readme / text questionnaire:
                    if execute:
                        shutil.move(fp, new_fp)
                        print("  Moved", fp, "to", new_fp)
                    else:
                        print("  Move", fp, "to", new_fp)

    # Remove folders:

    if new_uri.uri_type == "author":
        if execute:
            shutil.rmtree(old_folder)
        else:
            for book_dir in os.listdir(old_folder):
                if not book_dir.endswith("yml"):
                    print("REMOVE BOOK FOLDER", os.path.join(old_folder, book_dir))
            print("REMOVE AUTHOR FOLDER", old_folder)
    if new_uri.uri_type == "book":
        if execute:
            shutil.rmtree(old_folder)
        else:
            print("REMOVE BOOK FOLDER", old_folder)

    if not execute:
        resp = input("To carry out these changes: press OK+Enter; \
to abort: press Enter. ")
        if resp == "OK":
            print()
            change_uri(old, new, old_base_pth, new_base_pth, execute=True)
        else:
            print("User aborted carrying out these changes!")

def add_readme(target_folder):
    """Add default README.md file to target_folder.

    Returns:
        None
    """
    with open(os.path.join(target_folder, "README.md"),
              mode="w", encoding="utf-8") as file:
        file.write(readme_template)

def add_text_questionnaire(target_folder):
    """Add default text_questionnaire.md file to target_folder.

    Returns:
        None
    """
    with open(os.path.join(target_folder, "text_questionnaire.md"),
              mode="w", encoding="utf-8") as file:
        file.write(text_questionnaire_template)

def add_character_count(tok_count, char_count, tar_uri, execute=False):
    """Add the character and token counts to the new version yml file

    Args:
        tok_count (int): number of Arabic tokens in a text
        char_count (int): number of Arabic characters in a text
        tar_uri (URI object): uri of the target text
        execute (bool): if True, the function will do its work silently.
          If False, it will only print a description of the action.

    Returns:
        None
    """

    tar_yfp = tar_uri.build_pth("version_yml")
    if execute:
        with open(tar_yfp, mode="r", encoding="utf-8") as file:
            yml_dic = yml.ymlToDic(file.read().strip())
            yml_dic["00#VERS#LENGTH###:"] = tok_count
            yml_dic["00#VERS#CLENGTH##:"] = char_count
        with open(tar_yfp, mode="w", encoding="utf-8") as file:
            file.write(yml.dicToYML(yml_dic))
    else:
        print("  Add the character count to the version yml file")


def new_yml(tar_yfp, yml_type, execute=False):
    """Create a new yml file from template.

    Args:
        tar_yfp (str): filepath to the new yml file
        yml_type (str): type of yml file
            (either "version_yml", "book_yml", or "author_yml")
    Returns:
        None
    """
    template = eval("{}_template".format(yml_type))
    yml_dic = yml.ymlToDic(template)
    uri_key = "00#{}#URI######:".format(yml_type[:4].upper())
    u = URI(tar_yfp)
    u.extension = ""
    yml_dic[uri_key] = u.build_uri()
    if execute:
        with open(tar_yfp, mode="w", encoding="utf-8") as file:
            file.write(yml.dicToYML(yml_dic))
    else:
        if not tar_yfp in created_ymls:
            print("  Create temporary yml file", tar_yfp)
            created_ymls.append(tar_yfp)


def move_yml(yml_fp, new_uri, uri_type, execute=False):
    """Replace the URI in the yml file
    and save the yml file in its new location.

    Args:
        yml_fp (str): path to the original yml file
        new_uri (URI object): the new uri
        uri_type (str): uri type (author, book, version)
        execute (bool): if False, the proposed changes will only be printed
            (the user will still be given the option to execute
            all proposed changes at the end);
            if True, all changes will be executed immediately.

    Returns:
        (str): filepath of the new yml file
    """
    new_yml_fp = new_uri.build_pth(uri_type=uri_type+"_yml")
    new_yml_folder = os.path.split(new_yml_fp)[0]
    make_folder(new_yml_folder, new_uri, execute)

    if not execute:
        print("  Change URI inside yml file:")
    yml_dict = yml.readYML(yml_fp)
    key = "00#{}#URI######:".format(uri_type[:4].upper())
    yml_dict[key] = new_uri.build_uri(uri_type=uri_type, ext="")
    yml_str = yml.dicToYML(yml_dict)
    if not execute:
        print(yml_str)

    if execute:
        with open(new_yml_fp, mode="w", encoding="utf-8") as yml_file:
            yml_file.write(yml_str)
        os.remove(yml_fp)
        print("Moved", yml_fp, "\n    to", new_yml_fp)
    else:
        print("  Move", yml_fp, "\n    to", new_yml_fp)
    return new_yml_fp


def make_folder(new_folder, new_uri, execute=False):
    """Check if folder exists; if not, make folder (and, if needed, parents)

    Args:
        new_folder (str): path to new folder
        new_uri (OpenITI uri object): uri of the text
        execute (bool): if False, the proposed changes will only be printed
            (the user will still be given the option to execute
            all proposed changes at the end);
            if True, all changes will be executed immediately.

    Returns:
        None
    """
    if not os.path.exists(new_uri.base_pth):
        msg = """PathError: base path ({}) does not exist.
Make sure base path is correct.""".format(new_uri.base_pth)
        raise Exception(msg)
    if not os.path.exists(new_folder):
        author_folder = new_uri.build_pth("author")
        if not os.path.exists(author_folder):
            if execute:
                os.makedirs(author_folder)
            else:
                if not author_folder in created_folders:
                    print("  Make author_folder", author_folder)
                    created_folders.append(author_folder)
            new_yml(new_uri.build_pth("author_yml"), "author_yml", execute)
        if new_uri.uri_type == "book" or new_uri.uri_type == "version":
            book_folder = new_uri.build_pth("book")
            if not os.path.exists(book_folder):
                if execute:
                    os.makedirs(book_folder)
                else:
                    if not book_folder in created_folders:
                        print(" Make book_folder", book_folder)
                        created_folders.append(book_folder)
                new_yml(new_uri.build_pth("book_yml"), "book_yml", execute)
            if new_uri.uri_type == "version":
                new_yml(new_uri.build_pth("version_yml"),
                            "version_yml", execute)
                target_folder = new_uri.build_pth("version")
                if execute:
                    if "README.md" not in os.listdir(target_folder):
                        add_readme(target_folder)
                    if "text_questionnaire.md" not in os.listdir(target_folder):
                        add_text_questionnaire(target_folder)


def move_to_new_uri_pth(old_fp, new_uri, execute=False):
    """Move file to its new location.

    Args:
        old_fp (filepath): path to the old file
        new_uri (URI object): URI of the new file
        execute (bool): if False, the proposed changes will only be printed
            (the user will still be given the option to execute
            all proposed changes at the end);
            if True, all changes will be executed immediately.

    Returns:
        (str): path to the new file
    """
    new_folder = new_uri.build_pth(uri_type=new_uri.uri_type)
    new_fp = new_uri.build_pth(uri_type=new_uri.uri_type+"_file")
    make_folder(new_folder, new_uri, execute)
    if execute:
        shutil.move(old_fp, new_fp)
        print("  Move", old_fp, "\n    to", new_fp)
    else:
        print("  Move", old_fp, "\n    to", new_fp)
    return new_fp


#def check_token_count(version_uri, ymlD):
def check_token_count(version_uri, ymlD, version_fp="", find_latest=True):
    """Check whether the token count in the version yml file agrees with the\
    actual token count of the text file.

    Args:
        version_uri (URI object): version uri of the target text
        ymlD (dict): dictionary containing the data from the relevant yml file
        version_fp (str): file path to the target text
        find_latest (bool): if False, the version_fp will be used as is;
            if set to True, the script will find the most developed version of
            the text file, based on its extension (mARkdown > completed > inProgress)
    Returns:
        (tuple): Tuple containing 2 values (or None):

            tok_count (int): number of Arabic tokens in the target text
            char_count (int): number of Arabic characters in the target text
    """
    # Get the count from the most complete version of the text file: 
    #fp = version_uri.build_pth(uri_type="version_file")
    if version_fp and not find_latest:
        fp = version_fp
    elif version_fp and find_latest:
        for ext in [".mARkdown", ".completed", ".inProgress", ""]:
            fp = version_fp + ext
            if os.path.exists(fp):
                break
    else:
        for ext in ["mARkdown", "completed", "inProgress", ""]:
            version_uri.extension = ext
            fp = version_uri.build_pth(uri_type="version_file")
            if os.path.exists(fp):
                break
    tok_count = ar_cnt_file(fp, mode="token")
    char_count = ar_cnt_file(fp, mode="char")
    len_key = "00#VERS#LENGTH###:"
    char_len_key = "00#VERS#CLENGTH##:"
    yml_tok_count = ymlD[len_key].strip()
    try:
        yml_char_count = ymlD[char_len_key].strip()
    except:
        yml_char_count = ""
    replace_tok_count = False
    for cnt, yml_cnt in [(tok_count, yml_tok_count),
                         (char_count, yml_char_count)]:
        if yml_cnt == "":
            print("NO TOKEN COUNT", version_uri)
            replace_tok_count = True
        else:
            try:
                if int(yml_cnt) != cnt:
                    replace_tok_count = True
                    #print("TOKEN COUNT CHANGED", uri)
                    #print(yml_tok_count, "!=", tok_count)
            except:
                print("TOKEN COUNT {} IS NOT A NUMBER".format(yml_cnt), uri)
                replace_tok_count = True
    if replace_tok_count:
        return tok_count, char_count

def replace_tok_counts(missing_tok_count):
    """Replace the token counts in the relevant yml files.

    Args:
        missing_tok_count (list): a list of tuples:
            uri (OpenITI URI object)
            version_fp (str)
            token_count (int): the number of Arabic tokens in the text file
            char_count (int): the number of Arabic characters in the text file

    Returns:
        None
    """
    print("replacing token count in {} files".format(len(missing_tok_count)))
    for uri, version_fp, tok_count, char_count in missing_tok_count:
        print(uri, version_fp)
        #yml_fp = uri.build_pth("version_yml")
        if version_fp.endswith(("mARkdown", "completed", "inProgress")):
            yml_fp = os.path.splitext(version_fp)[0] + ".yml"
        else:
            yml_fp = version_fp + ".yml"
        ymlD = yml.readYML(yml_fp)
        len_key = "00#VERS#LENGTH###:"
        ymlD[len_key] = str(tok_count)
        char_len_key = "00#VERS#CLENGTH##:"
        ymlD[char_len_key] = str(char_count)
        ymlS = yml.dicToYML(ymlD)
        with open(yml_fp, mode="w", encoding="utf-8") as outf:
            outf.write(ymlS)

def check_yml_file(yml_fp, yml_type, version_fp=None, execute=False,
                   check_token_counts=True):
    """Check whether a yml file exist, is valid, and contains no foreign keys

    Args:
        yml_fp (str): path to the yml file
        yml_type (str): either "author", "book", or "version"
        version_fp (str): path to the text file of the version
            (only relevant for version yml files; default = None)
        execute (bool): if False, the user will be prompted
            before any changes are made to the yml file
        check_token_counts (bool): if True, the script will check
            the number of tokens (and characters) in the text

    Returns:
        None or yml_fp
    """
    yml_changed = False
    
    # Check if yml file exists:
    if not os.path.exists(yml_fp):
        print(yml_fp, "DOES NOT EXIST")
        # create a new yml file:
        if execute or input("Create yml file? Y/N? ").lower() == "y":
            new_yml(yml_fp, yml_type+"_yml", True)
            print("New yml file created.")
            yml_d = yml.readYML(yml_fp) 
        else:
            print("No new yml file created. Check manually!")
            return yml_fp
        

    # Check if yml is valid:
    try:
        yml_d = yml.readYML(yml_fp)
        if yml_d == {}:
            print("Empty yml file")
            if execute or input("Create yml file? Y/N? ").lower() == "y":
                new_yml(yml_fp, yml_type+"_yml", True)
                print("New yml file created.")
                yml_d = yml.readYML(yml_fp)
            else:
                print("No new file created. Check manually!")
                return yml_fp
            
        yml_d.keys()
    except Exception as e:
        print("invalid YML file structure:", yml_fp)
        print("Error message:", e)
        yml_d = yml.fix_broken_yml(yml_fp, execute)
        if yml_d:
            yml_changed = True
        else:
            return yml_fp
    for key in list(yml_d.keys()):  # NB: list needed because otherwise keys cannot be deleted!
        
        # check if all keys have the prefix of the yml type (..#AUTH, ..#BOOK, ..#VERS):
        if key[3:7] != yml_type.upper()[:4]:
            print("wrong key in yml file", yml_fp, ":", key)
            if execute or input("Delete yml key {}? Y/N: ".format(key)).lower() == "y":
                del yml_d[key]
                yml_changed = True
                print("-> deleted yml key", key)
            else:
                return yml_fp

        # check whether the URI in the yml file is identical with that in the filename:
        if "URI" in key:
            fn = os.path.splitext(os.path.split(yml_fp)[-1])[0]
            fn = re.sub("\.inProgress|\.mARkdown|\.completed", "", fn)
            if yml_d[key].strip() != fn:
                print("URI", yml_d[key], "!= filename", fn)
                if execute or input("Replace URI with filename? Y/N: ").lower() == "y":
                    yml_d[key] = fn
                    yml_changed = True
                    print("-> URI replaced with", fn)
                else:
                    return yml_fp
                
    # check whether version yml files contain token and character length values:
    if yml_type == "version" and check_token_counts:
        res = check_token_count(URI(yml_fp), yml_d, version_fp)
        if res:
            tok_count, char_count = res
            if execute or input("Change token count? Y/N? ").lower() == "y":
                yml_d["00#VERS#LENGTH###:"] = str(tok_count)
                yml_d["00#VERS#CLENGTH##:"] = str(char_count)
                yml_changed = True
                print(yml_fp)
                print("-> token and character counts changed")
            else:
                return yml_fp

    # save changes to yml file if anything has changed: 
    if yml_changed:
        with open(yml_fp, mode="w", encoding="utf-8") as file:
            file.write(yml.dicToYML(yml_d))


def check_yml_files(start_folder, exclude=[],
                    execute=False, check_token_counts=True,
                    flat_folder=False):
    """Check whether yml files are missing or have faulty data in them.

    Args:
        start_folder (str): path to the parent folder of the folders
            that need to be checked.
        exclude (list): a list of directory names that should be excluded.
        execute (bool): if execute is set to False, the script will only show
            which changes it would undertake if set to True.
            After it has looped through all files and folders, it will give
            the user the option to execute the proposed changes.

    Returns:
        None
    """
    failed = []
    for fp in get_all_text_files_in_folder(start_folder, excluded_folders=exclude):
        uri = URI(fp)
        for yml_type in ("author", "book", "version"):
            yml_fn = uri.build_uri(uri_type="{}_yml".format(yml_type))
            if yml_type == "author":
                if flat_folder:
                    yml_fp = os.path.join(os.path.dirname(fp), yml_fn)
                else:
                    yml_fp = os.path.join(os.path.dirname(os.path.dirname(fp)), yml_fn)
            else:
                yml_fp = os.path.join(os.path.dirname(fp), yml_fn)
            r = check_yml_file(yml_fp, yml_type, version_fp=fp, execute=execute,
                               check_token_counts=check_token_counts)
            if r:
                failed.append(r)
    if failed:
        print("The following yml files could not be read. Please correct them manually:")
        for yml_fp in failed:
            print("*", yml_fp)
        print()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("passed doctests")
    print()

    folder = r"D:\London\OpenITI\25Y_repos/0450AH"
    check_yml_files(folder)
    input("CONTINUE?")

    # Additional tests:


##    URI.base_pth = r"."
##    print("URI path in 25Y-repo format:")
##    my_uri = URI("0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed")
##    print(my_uri.build_pth())
##    print("URI path in release format (without 25Y repos):")
##    URI.data_in_25_year_repos = False
##    my_uri = URI("0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed")
##    print(my_uri.build_pth())
##    print("URI path in 25Y-repo format:")
##    URI.data_in_25_year_repos = True
##    print(my_uri.build_pth())
##    my_uri.data_in_25_year_repos = False
##    print("URI path in release format (without 25Y repos):")
##    print(my_uri.build_pth())
##
##    # Reset:
##    URI.data_in_25_year_repos = True
##    URI.base_pth = r"D:\London\OpenITI\25Y_repos"
##
##    input("Press Enter to continue")
##    print()
    
##    exclude = (["OpenITI.github.io", "Annotation", "maintenance", "i.mech00",
##                "i.mech01", "i.mech02", "i.mech03", "i.mech04", "i.mech05",
##                "i.mech06", "i.mech07", "i.mech08", "i.mech09", "i.logic",
##                "i.cex", "i.cex_Temp", "i.mech", "i.mech_Temp", ".git"])
##    resp = check_yml_files(r"D:\London\OpenITI\25Y_repos",
##                           exclude=exclude, execute=False)
##    missing_ymls, missing_tok_count, non_uri_files, erratic_ymls = resp
##    #print(non_uri_files)
##    input("continue?")
##
    base_pth = r"D:\London\OpenITI\python_library\openiti\openiti\test"

##    # test initialize_new_texts_in_folder function:
##    barzakh = os.path.join(base_pth, "barzakh")
##    initialize_new_texts_in_folder(barzakh, base_pth, execute=True)
##    print("Texts in test/barzakh initialized; check if initialization was successful!")
##    input("Press Enter to continue")

##    # test initialize_texts_from_CSV function:
##    csv_fp = os.path.join(base_pth, "initialize.csv")
##    initialize_texts_from_CSV(csv_fp, old_base_pth="", new_base_pth=base_pth,
##                              execute=False)
##    print("Texts in test/barzakh initialized; check if initialization was successful!")
##    input("Press Enter to continue")

##    # test change_uri function for author uri change:
##    old = "0001KitabAllah"
##    new = "0001Allah"
##    change_uri(old, new,
##               old_base_pth=base_pth, new_base_pth=base_pth,
##               execute=False)
##    input("Press Enter to continue")

##    # test change_uri function for book uri change:
##    old = "0375IkhwanSafa.RisalatJamicaJamica"
##    new = "0375IkhwanSafa.RisalatJamica"
##    change_uri(old, new,
##               old_base_pth=base_pth, new_base_pth=base_pth,
##               execute=False)
##    input("Press Enter to continue")

##    # test change_uri function for version uri change:
##    old = "0001Allah.KitabMuqaddas.BibleCorpus002-per1"
##    new = "0001Allah.KitabMuqaddas.BibleCorpus2-per1"
##    change_uri(old, new,
##               old_base_pth=base_pth, new_base_pth=base_pth,
##               execute=False)
##    print("Check if the URI really changed??")
##    input("Press Enter to continue")

    my_uri = "0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed"

    #URI.base_pth = "XXXX"

    t = URI(my_uri)
    print("repr(t):")
    print(repr(t))
    print("print(t):")
    print(t)
    print("t.author:", t.author)
    print("t.date:", t.date)
    print("URI type:", t.uri_type)
    print('t.build_uri("author"):')
    print(t.build_uri("author"))
    print('t.build_pth("version_file"):')
    print(t.build_pth("version_file"))
    print('t.build_pth("version_file", ""):')
    print(t.build_pth("version_file", ""))

    print("*"*30)

    u = URI()
    u.author="IbnCarabi"
    u.date="0681"
    print('u.build_uri("author"):')
    print(u.build_uri("author"))
    print('u:')
    print(u)

    print("*"*30)

    my_uri = URI("0255Jahiz.Hayawan.Sham19Y0023775-ara1.completed")
    print('my_uri.split_uri():')
    print(my_uri.split_uri())
#    my_uri.extension=""
    my_uri.language=""
    print('my_uri.split_uri(): (language="")')
    print(my_uri.split_uri())
    my_uri.extension=""
    print("try to build a path from an incomplete version URI (language=''):")
    print("AN ERROR WARNING SHOULD FOLLOW: ")
    print(my_uri.build_pth(base_pth="./master", uri_type="version_file"))




