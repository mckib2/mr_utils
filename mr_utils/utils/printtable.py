'''Tabular output.'''

class Table(object):
    '''Table with header and columns. Nothing fancy.

    Class meant for simple column printing, e.g., printing updates for each
    iteration of an iterative algorithm.

    Attributes
    ==========
    headings : list
        List of strings giving column labels.
    symbol : str
        Character to use as separator between header and table rows.
    pad : int
        Number of spaces between columns.
    widths : int or list
        List of widths for each column in number of characters.
    formatters : list
        String formatters, will use %g if None is given.
    '''

    def __init__(self, headings, widths, formatters=None, pad=2, symbol='#'):
        '''Initialize the table object.

        headings : list
            List of strings to use as headings for columns.
        widths : list or int
            List of widths for each column.
        formatters : list, optional
            List of format options to use for each column.
        pad : int, optional
            Space between columns
        symbol : str, optional
            Character to use as separator between header and table rows.

        Notes
        =====
        widths=[int] will assign each column the same width of [int].
        formatters=None will use 'g' for every column.
        '''

        assert isinstance(widths, int) or len(headings) == len(widths), \
            'Widths must match up to headings!'
        assert formatters is None or len(formatters) == len(headings), \
            'Must have same number of formatters as headings!'

        self.headings = headings
        self.symbol = symbol
        self.pad = pad

        # If we have only one number, make all widths the same
        if isinstance(widths, int):
            self.widths = [widths]*len(headings)
        else:
            self.widths = widths

        # If user didn't give a formatter, then use 'g' for each
        if formatters is None:
            self.formatters = ['g']*len(self.headings)
        else:
            self.formatters = formatters

        # If formatters include 'g','e', then widths will need to include e+-[]
        self.widths = [w+4 if f in ['g', 'e'] else w for w, f in \
            zip(self.widths, self.formatters)]

    def header(self):
        '''Return table header.

        Returns
        =======
        hdr : str
            Table header.
        '''

        # Create headings with specified widths
        hdr = []
        for idx, h in enumerate(self.headings):
            hdr.append(('{:%ds}' % self.widths[idx]).format(h))
        hdr = (' '*self.pad).join(hdr)

        # Add separator between header and contents
        hdr += '\n' + self.symbol*len(hdr)

        return hdr

    def row(self, vals):
        '''Return row of table.

        Parameters
        ==========
        vals : list
            List of numbers corresponding to display for each row.

        Returns
        =======
        line : str
            The row.
        '''

        line = []
        for idx, val in enumerate(vals):
            line.append((
                '{:%d%s}' % (self.widths[idx], self.formatters[idx]))
                        .format(val))
        line = (' '*self.pad).join(line)
        return line
