"""
Parse the StrongHelp file format into structured data.

Example usage::

    from riscos_stronghelp.format import StrongHelp, objtype_dir

    sh = StrongHelp(shfilename)

    try:
        os.makedirs(output_dir)
    except OSError:
        pass

    for shf in sh:
        print("{}".format(shf.filename))
        filename = os.path.join(output_dir, shf.unix_filename)
        if shf.objtype == objtype_dir:
            try:
                os.makedirs(filename)
            except OSError:
                pass
        else:
            with open(filename, 'wb') as fh:
                fh.write(shf.read())
"""

import struct


# Flags in the StrongHelp file
flag_owner_read = (1<<0)  # owner read
flag_owner_write = (1<<1)  # owner write
flag_locked = (1<<3)  # locked
flag_public_read = (1<<4)  # public read
flag_public_write = (1<<5)  # public write
flag_directory = (1<<8)  # is directory


# RISC OS Object types
objtype_file = 1
objtype_dir = 2


class StrongHelpFormatError(Exception):
    pass


class StrongHelpBlock(object):

    def __init__(self, sh, offset):
        self.sh = sh
        self.offset = offset

    def read_bytes(self, size, offset=0):
        return self.sh.read_bytes(size, self.offset + offset)

    def read_word(self, offset=0):
        return self.sh.read_word(self.offset + offset)

    def read_string(self, offset=0):
        return self.sh.read_string(self.offset + offset)


class StrongHelpObject(StrongHelpBlock):

    def __init__(self, sh, offset, parent_dir, leafname, loadaddr=0, execaddr=0, flags=0, length=0):
        super(StrongHelpObject, self).__init__(sh, offset)
        self.parent_dir = parent_dir
        self.leafname = leafname
        self.loadaddr = loadaddr
        self.execaddr = execaddr
        self.flags = flags
        self.length = length

        #print("{} '{}' at &{:x}".format(self.__class__.__name__,
        #                                self.filename, self.offset))

    def __repr__(self):
        return "<{}('{}', &{:08x}/&{:08x}, &{:x} bytes)>".format(self.__class__.__name__,
                                                                 self.filename,
                                                                 self.loadaddr,
                                                                 self.execaddr,
                                                                 self.length)

    @property
    def attributes(self):
        """
        RISC OS File attributes.
        """
        # Just the bottom 8 bits
        return self.flags & 0xFF

    @property
    def objtype(self):
        """
        RISC OS object type.
        """
        return objtype_dir if (self.flags & flag_directory) else objtype_file

    @property
    def filetype(self):
        if self.flags & flag_directory:
            return 0x1000
        if self.loadaddr & 0xFFF00000 == 0xFFF00000:
            return (self.loadaddr >> 8) & 0xFFF
        return -1

    @property
    def filename(self):
        if not self.parent_dir:
            return self.leafname
        parent = self.parent_dir.filename
        return "{}.{}".format(parent, self.leafname.encode('latin-1'))

    @property
    def unix_filename(self):
        leafname = self.leafname.replace('/', '.')
        if not self.parent_dir:
            return self.leafname

        if self.filetype in (0xFFF, 0x1000):
            # A text file or a directory
            suffix = ''

        elif self.filetype == -1:
            # Not filetyped - there's a load and exec address.
            # We will treat these as Data for now - the strongcopy tool
            # doesn't support load and exec formats.
            suffix = ',ffd'

        else:
            # Other filetypes
            suffix = ',%03x' % (self.filetype,)

        parent = self.parent_dir.unix_filename
        if parent == '$':
            return leafname + suffix
        else:
            return "{}/{}{}".format(parent, leafname.encode('utf-8'), suffix)


class StrongHelpFile(StrongHelpObject):

    def __init__(self, sh, offset, parent_dir, leafname, loadaddr=0, execaddr=0, flags=0, length=0):
        super(StrongHelpFile, self).__init__(sh, offset, parent_dir, leafname, loadaddr, execaddr, flags, length)

        if offset == 0:
            # This is a 0 byte file
            self.size = 0

        else:
            if self.read_bytes(4, offset=0) != 'DATA':
                raise StrongHelpFormatError("Bad file entry '{}' at offset &{:x}: "
                                            "Block header is invalid".format(self.filename,
                                                                             offset))

            self.size = self.read_word(4)
            if self.size < self.length:
                raise StrongHelpFormatError("Bad file entry '{}' at offset &{:x}: "
                                            "Block is too small ({}) for file length ({})".format(self.filename,
                                                                                                  offset,
                                                                                                  self.size,
                                                                                                  self.length))

    def read(self, encoding=None):
        if not self.size:
            data = b''
        else:
            data = self.read_bytes(self.length - 8, offset=8)
        if encoding:
            data = data.decode(encoding)

        return data


class StrongHelpDir(StrongHelpObject):

    def __init__(self, sh, offset, parent_dir, leafname, loadaddr=0, execaddr=0, flags=0, length=0):
        super(StrongHelpDir, self).__init__(sh, offset, parent_dir, leafname, loadaddr, execaddr, flags, length)

        if self.read_bytes(4, offset=0) != 'DIR$':
            raise StrongHelpFormatError("Bad directory entry '{}' at offset &{:x}: "
                                        "Block header is invalid".format(self.filename,
                                                                         offset))

        self.dir_size = self.read_word(4)
        self.dir_used = self.read_word(8)

        if self.dir_used > self.dir_size:
            raise StrongHelpFormatError("Bad directory entry '{}' at offset &{:x}: "
                                        "Block is too small ({}) for used size ({})".format(self.filename,
                                                                                            offset,
                                                                                            self.dir_size,
                                                                                            self.dir_used))
        if self.dir_used < 12 + 24:
            raise StrongHelpFormatError("Bad directory entry '{}' at offset &{:x}: "
                                        "Block is too small ({}) for directory entry".format(self.filename,
                                                                                             offset,
                                                                                             self.dir_used))

        self.objects = []
        offset = 12
        while offset < self.dir_used:
            #print("--- file in dir {}, offset &{:x} ---".format(self.filename, offset))
            object_offset = self.read_word(offset + 0)
            loadaddr = self.read_word(offset + 4)
            execaddr = self.read_word(offset + 8)
            length = self.read_word(offset + 12)
            flags = self.read_word(offset + 16)
            reserved = self.read_word(offset + 20)
            # FIXME: Assuming the filename encoding is latin-1 (probably correct, but not configurable)
            name = self.read_string(offset + 24).decode('latin-1')
            offset += 24 + (len(name) + 4) & ~3

            if flags & flag_directory:
                shfile = StrongHelpDir(self.sh, object_offset, parent_dir=self, leafname=name,
                                       loadaddr=loadaddr, execaddr=execaddr, flags=flags, length=length)
            else:
                shfile = StrongHelpFile(self.sh, object_offset, parent_dir=self, leafname=name,
                                       loadaddr=loadaddr, execaddr=execaddr, flags=flags, length=length)
            self.objects.append(shfile)


class StrongHelp(object):

    def __init__(self, filename=None, data=None):
        self.filename = filename
        if data:
            self.data = data
        else:
            with open(filename, 'rb') as fh:
                self.data = fh.read()

        if self.data[0:4] != 'HELP':
            raise StrongHelpFormatError("This is not a StronhHelp file")

        self.root_size = self.read_word(4)
        self.stronghelp_version = self.read_word(8)
        self.free_list = self.read_word(12)

        self.root_offset = self.read_word(16)

        #print("Root offset = %08x" % (self.root_offset,))

        self.root = StrongHelpDir(self, self.root_offset, parent_dir=None, leafname='$')

    def __iter__(self):
        """
        List all the files in the StrongHelp file.
        """
        shdirs = [self.root]
        while shdirs:
            shdir = shdirs.pop()
            for shobj in shdir.objects:
                if isinstance(shobj, StrongHelpDir):
                    shdirs.append(shobj)
                yield shobj

    def read_word(self, offset):
        #print("Read word at &{:x}".format(offset))
        (data,) = struct.unpack('<L', self.data[offset:offset + 4])
        #print("  &{:08x} = {}".format(data, data))
        return data

    def read_bytes(self, size, offset):
        return self.data[offset:offset + size]

    def read_string(self, offset):
        s = []
        while self.data[offset] != '\0':
            s.append(self.data[offset])
            offset += 1
        return b''.join(s)
