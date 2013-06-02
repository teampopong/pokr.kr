from datetime import datetime

ASSEMBLY_TERMS = [
    ('31 May 1948', '30 May 1950'),
    ('31 May 1950', '30 May 1954'),
    ('31 May 1954', '30 May 1958'),
    ('31 May 1958', '30 May 1960'),
    ('29 Jul 1960', '16 May 1961'),
    ('17 Dec 1963', '30 Jun 1967'),
    ('1  Jul 1967', '25 Jul 1971'),
    ('26 Jul 1971', '18 Oct 1972'),
    ('12 Mar 1973', '16 Mar 1979'),
    ('17 Mar 1979', '27 Oct 1980'),
    ('11 Apr 1981', '12 May 1985'),
    ('13 May 1985', '29 May 1988'),
    ('30 May 1988', '29 May 1992'),
    ('30 May 1992', '29 May 1996'),
    ('30 May 1996', '4  Jun 2000'),
    ('5  Jun 2000', '29 May 2004'),
    ('30 May 2004', '29 May 2008'),
    ('30 May 2008', '29 May 2012'),
    ('30 May 2012', '29 May 2016'),
]


class Term(object):

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date


ASSEMBLY_TERMS = [None]\
               + [Term(*(datetime.strptime(d, '%d %b %Y').date() for d in term))
                  for term in ASSEMBLY_TERMS]


def term(assembly_id):
    return ASSEMBLY_TERMS[assembly_id]
