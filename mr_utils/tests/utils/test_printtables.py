import unittest
from mr_utils.utils.printtable import Table

class TestPrintTable(unittest.TestCase):

    def setUp(self):
        self.headings = [ 'a','b','c' ]
        self.widths = [ 2,3,4 ]
        self.formatters = [ 'd','d','d' ]
        self.width = 8
        self.pad = 0

    def test_table_header_int_width(self):
        t = Table(self.headings,self.width,self.formatters,pad=self.pad)
        hdr = t.header()

        # *2 because we have two lines, +1 because we have a newline
        self.assertEqual(len(hdr),self.width*len(self.headings)*2 + 1)

    def test_table_header(self):
        t = Table(self.headings,self.widths,self.formatters,pad=self.pad)
        hdr = t.header()
        self.assertEqual(len(hdr),sum(self.widths)*2 + 1)

    def test_table_row(self):
        t = Table(self.headings,self.widths,self.formatters,pad=self.pad)
        hdr = t.header()
        row = t.row(self.widths)
        self.assertEqual(len(row),sum(self.widths))

if __name__ == '__main__':
    unittest.main()
