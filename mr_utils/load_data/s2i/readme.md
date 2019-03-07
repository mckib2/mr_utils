
## mr_utils.load_data.s2i.channel_header

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/channel_header.py)

```
NAME
    mr_utils.load_data.s2i.channel_header - Holds header data for a single channel.

```


## mr_utils.load_data.s2i.channel_header_and_data

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/channel_header_and_data.py)

```
NAME
    mr_utils.load_data.s2i.channel_header_and_data - Struct to hold both header and data for a single channel.

CLASSES
    builtins.object
        ChannelHeaderAndData
    
    class ChannelHeaderAndData(builtins.object)
     |  Class to hold channel header and data.
     |  
     |  We don't know what the size of the data will be, so we don't create an
     |  np.dtype for this structure.  Instead, since it's just a top
     |  level container, we're fine with just a python class.
     |  
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)

```


## mr_utils.load_data.s2i.defs

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/defs.py)

```
NAME
    mr_utils.load_data.s2i.defs - Constant definitions used by siemens_to_ismrmrd.

```


## mr_utils.load_data.s2i.fill_ismrmrd_header

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/fill_ismrmrd_header.py)

```
NAME
    mr_utils.load_data.s2i.fill_ismrmrd_header - fill_ismrmrd_header

DESCRIPTION
    This is currently not working and silently failing.

FUNCTIONS
    fill_ismrmrd_header(h, study_date, study_time)
        Add dates/times to ISMRMRD header.


```


## mr_utils.load_data.s2i.get_acquisition

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/get_acquisition.py)

```
NAME
    mr_utils.load_data.s2i.get_acquisition - Populate ISMRMRD Acquisition object with data from ChannelHeaderAndData.

FUNCTIONS
    getAcquisition(flash_pat_ref_scan, trajectory, dwell_time_0, max_channels, _isAdjustCoilSens, _isAdjQuietCoilSens, _isVB, traj, scanhead, channels)
        Create ISMRMRD acqusition object for the current channel data.


```


## mr_utils.load_data.s2i.mdh

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/mdh.py)

```
NAME
    mr_utils.load_data.s2i.mdh - All MDH related structures.

```


## mr_utils.load_data.s2i.parse_xml

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/parse_xml.py)

```
NAME
    mr_utils.load_data.s2i.parse_xml - parseXML

FUNCTIONS
    parseXML(debug_xml, parammap_xsl_content, _schema_file_name_content, xml_config)
        Apply XSLT.


```


## mr_utils.load_data.s2i.process_parameter_map

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/process_parameter_map.py)

```
NAME
    mr_utils.load_data.s2i.process_parameter_map - ProcessParameterMap

FUNCTIONS
    ProcessParameterMap(config_buffer, parammap_file_content)
        Fill in the headers of all parammap_file's fields.
    
    reduce(...)
        reduce(function, sequence[, initial]) -> value
        
        Apply a function of two arguments cumulatively to the items of a sequence,
        from left to right, so as to reduce the sequence to a single value.
        For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) calculates
        ((((1+2)+3)+4)+5).  If initial is present, it is placed before the items
        of the sequence in the calculation, and serves as a default when the
        sequence is empty.


```


## mr_utils.load_data.s2i.read_channel_headers

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/read_channel_headers.py)

```
NAME
    mr_utils.load_data.s2i.read_channel_headers - Store data and header for each channel.

FUNCTIONS
    readChannelHeaders(siemens_dat, VBFILE, scanhead)
        Read the headers for the channels.

```


## mr_utils.load_data.s2i.read_measurement_header_buffers

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/read_measurement_header_buffers.py)

```
NAME
    mr_utils.load_data.s2i.read_measurement_header_buffers - readMeasurementHeaderBuffers

FUNCTIONS
    readMeasurementHeaderBuffers(siemens_dat, num_buffers)
        Filler.


```


## mr_utils.load_data.s2i.read_parc_file_entries

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/read_parc_file_entries.py)

```
NAME
    mr_utils.load_data.s2i.read_parc_file_entries - readParcFileEntries

FUNCTIONS
    readParcFileEntries(siemens_dat, ParcRaidHead, VBFILE)
        struct MrParcRaidFileEntry
        {
          uint32_t measId_;
          uint32_t fileId_;
          uint64_t off_;
          uint64_t len_;
          char patName_[64];
          char protName_[64];
        };


```


## mr_utils.load_data.s2i.read_scan_header

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/read_scan_header.py)

```
NAME
    mr_utils.load_data.s2i.read_scan_header - readScanHeader

FUNCTIONS
    readScanHeader(siemens_dat, VBFILE)
        Read the header from the scan.

```


## mr_utils.load_data.s2i.read_xml_config

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/read_xml_config.py)

```
NAME
    mr_utils.load_data.s2i.read_xml_config - readXmlConfig

FUNCTIONS
    readXmlConfig(debug_xml, parammap_file_content, num_buffers, buffers, wip_double, trajectory, dwell_time_0, max_channels, radial_views, baseLineString, protocol_name)
        Read in and format header from raw data file.


```


## mr_utils.load_data.s2i.regex_parser

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/regex_parser.py)

```
NAME
    mr_utils.load_data.s2i.regex_parser - Make a parser using regex.

DESCRIPTION
    Let's see how this goes...

CLASSES
    builtins.object
        Parser
    
    class Parser(builtins.object)
     |  Parse XProtocol.
     |  
     |  Methods defined here:
     |  
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  isconsistent(self)
     |      Make sure cur_rule is a subset of some rule.
     |  
     |  isrule(self)
     |      Check to see if cur_rule is a rule.
     |  
     |  istoken(self)
     |      Check to see if cur_token is a token.
     |  
     |  parse(self, buf)
     |      Parse buffer into dictionary.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)

```


## mr_utils.load_data.s2i.scan_header

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/scan_header.py)

```
NAME
    mr_utils.load_data.s2i.scan_header - Structure to hold the header of a scan.

```


## mr_utils.load_data.s2i.xml_fun

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/xml_fun.py)

```
NAME
    mr_utils.load_data.s2i.xml_fun - All the XML related functions required by siemens_to_ismrmrd.

FUNCTIONS
    get_embedded_file(file)
        Retrieve embedded file from github.
        
        file -- Name of embedded file to get.
    
    get_ismrmrd_schema(method='ET')
        Download XSD file from ISMRMD git repo.
    
    get_list_of_embedded_files()
        List of files to go try to find from the git repo.
    
    getparammap_file_content(parammap_file, usermap_file, VBFILE)
        Filler.


```


## mr_utils.load_data.s2i.xprot_parser_strsearch

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/load_data/s2i/xprot_parser_strsearch.py)

```
NAME
    mr_utils.load_data.s2i.xprot_parser_strsearch - Quick and lazy -- only read what we need from the XProtocol header.

DESCRIPTION
    This is a way engineered to Get the Job Done(TM).  It could be made a lot
    better and faster, but right now I'm just trying to get it working after the
    debacle with ply...
    
    The lookup table seems like a good idea, but having a little trouble getting it
    to work properly.  Currently it's supressing a lot of fields that don't exist,
    it's just not letting us display the warning that it doesn't exist.

FUNCTIONS
    find_matching_braces(s, lsym='{', rsym='}', qlsym='"', qrsym='"')
        Given string s, find indices of matching braces.
    
    findp(p, config)
        Decode the tag and return index.
        
        p -- Current path node.
        config -- The current header portion we're searching in.
        
        All of these tag assignments are ad hoc -- just to get something to work.
    
    xprot_get_val(config_buffer, val, p_to_buf_table=None, return_table=False)
        Get value from config buffer.
        
        config_buffer -- String containing the XProtocol innards.
        val -- Dot separated path to search for.
        p_to_buf_table --
        return_table --


```

