import platform
import ctypes as ct

class Stack(ct.Structure):
    _fields_ = [('loc',ct.POINTER(ct.c_long)) , ('m',ct.c_long) , ('m_capacity',ct.c_long)]


parent_dir = '/'.join(__file__.split('/')[:-1]) 

if platform.system() == 'Darwin':
    json_parser = ct.CDLL(parent_dir + '/json_parser_darwin.so')
elif platform.system() == 'Linux':
    json_parser = ct.CDLL(parent_dir + '/json_parser_linux.so')

json_parser.stack_len.argtypes = [ct.POINTER(Stack)]
json_parser.stack_len.restype = ct.c_long

json_parser.stack_release.argtypes = [ct.POINTER(Stack)]
json_parser.stack_release.restype = None

json_parser.stack_initialize.argtypes = [ct.POINTER(Stack)]
json_parser.stack_initialize.restype = None

json_parser.parse.argtypes = [ct.POINTER(ct.c_char),ct.POINTER(Stack),ct.POINTER(Stack),ct.POINTER(ct.c_long)]
json_parser.parse.restype = None


def parse(file_content_bytes):

    valid_ob_locs = []
    invalid_start_point = ct.c_long(0)

    invalid_start_point_p = ct.pointer(invalid_start_point)

    valid_ob_locs_start = Stack()
    valid_ob_locs_end = Stack()

    valid_ob_locs_start_p = ct.pointer(valid_ob_locs_start)
    valid_ob_locs_end_p = ct.pointer(valid_ob_locs_end)

    json_parser.stack_initialize(valid_ob_locs_start_p)
    json_parser.stack_initialize(valid_ob_locs_end_p)

    char_arr = ct.create_string_buffer(file_content_bytes)

    file_content_bytes_p = ct.cast(char_arr , ct.POINTER(ct.c_char))

    json_parser.parse(file_content_bytes_p,valid_ob_locs_start_p,valid_ob_locs_end_p,invalid_start_point_p)

    i=0
    while i < json_parser.stack_len(valid_ob_locs_start_p):
        valid_ob_locs.append(
            (valid_ob_locs_start.loc[i],valid_ob_locs_end.loc[i])
        )
        i+=1

    json_parser.stack_release(valid_ob_locs_start_p)
    json_parser.stack_release(valid_ob_locs_end_p)

    return {
        'valid_ob_locs' : valid_ob_locs,
        'invalid_start_point' : invalid_start_point_p.contents.value
    }


__all__ = ['parse']