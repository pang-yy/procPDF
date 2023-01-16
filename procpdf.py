import argparse, os
from shutil import get_terminal_size
from pdf_scripts.pypdf2_scripts import *

# TODO : modify python pakage's structure
# TODO : setup setup.py

# CONSTANTS START HERE
DEFAULT_PDF_DIR_NAME = 'put_pdf_here'
DEFAULT_PDF_PATH = f'./{DEFAULT_PDF_DIR_NAME}/'
TERMINAL_WIDTH = get_terminal_size().columns
PROGRAM_NAME = 'procpdf'
VERSION = '1.0.0'
# CONSTANTS END HERE

# CLASS START HERE
class SubcommandHelpFormatter(argparse.RawDescriptionHelpFormatter): # code from https://stackoverflow.com/questions/13423540/argparse-subparser-hide-metavar-in-command-listing
    def _format_action(self, action):
        parts = super(argparse.RawDescriptionHelpFormatter, self)._format_action(action)
        if action.nargs == argparse.PARSER:
            parts = "\n".join(parts.split("\n")[1:])
        return parts

class UExtension:
    def __init__(self, eP):
        self.extension = eP
# CLASS END HERE

# FUNCTION START HERE
def main():
    parser = argparse.ArgumentParser(
                        prog = PROGRAM_NAME,
                        #description = 'Pdf Tools via CLI',
                        # epilog = 'Text at the bottom of help',
                        # usage = '%(prog)s <command> [option]',
                        # add_help=False
                        formatter_class=SubcommandHelpFormatter
                        )
    parser._positionals.title = 'Commands'
    parser._optionals.title = 'General Options'
    subparsers = parser.add_subparsers(metavar='<command>')
    # create put_pdf_here if not exists
    if not(os.path.exists(DEFAULT_PDF_DIR_NAME)):
        os.mkdir(DEFAULT_PDF_DIR_NAME)

    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {VERSION}', help='program version')

    listall = subparsers.add_parser('listall', help='list all pdf files detected', usage='%(prog)s [-e EXTENSION]')
    listall._positionals.title = 'Arguments'
    listall._optionals.title = 'Command Options'
    listall.set_defaults(func=listAllFiles)
    listall.add_argument('-e', '--extension', default='.pdf', help='extention of file to search', metavar='EXTENSION')

    merge = subparsers.add_parser('merge', help='merge multiple pdf files into one pdf file', usage='%(prog)s (-a | -n | -s FILENAME...| -e FILENAME...) [-o OUTPUT_FILENAME]')
    merge._positionals.title = 'Arguments'
    merge._optionals.title = 'Command Options'
    merge.set_defaults(func=mergeFiles)
    mergeMutuallyExclusiveGroup = merge.add_mutually_exclusive_group(required=True)
    mergeMutuallyExclusiveGroup.add_argument('-a', '--all', action='store_true', help='merge all files')
    mergeMutuallyExclusiveGroup.add_argument('-n', '--number-input', action='store_true', help='list available all files and input files by number')
    mergeMutuallyExclusiveGroup.add_argument('-s', '--select', nargs='*', help='merge given files')
    mergeMutuallyExclusiveGroup.add_argument('-e', '--exclude', nargs='*', help='merge all files except given files')
    merge.add_argument('-o', '--output-filename', default='Combined_PyPDF2.pdf', help='filename of merged file')
    
    encrypt = subparsers.add_parser('encrypt', help='encrypt pdf file', usage='%(prog)s FILENAME [-r]')
    encrypt._positionals.title = 'Arguments'
    encrypt._optionals.title = 'Command Options'
    encrypt.set_defaults(func=encryptFiles)
    encrypt.add_argument('filename', help='name of file to encrypt', metavar='FILENAME')
    encrypt.add_argument('-r', '--remove', help='remove original file', action='store_true')

    decrypt = subparsers.add_parser('decrypt', help='decrypt an encrypted pdf file', usage='%(prog)s FILENAME [-r]')
    decrypt._positionals.title = 'Arguments'
    decrypt._optionals.title = 'Command Options'
    decrypt.set_defaults(func=decryptFiles)
    decrypt.add_argument('filename', help='name of file to decrypt', metavar='FILENAME')
    decrypt.add_argument('-r', '--remove', help='remove original file', action='store_true')
    
    extractImg = subparsers.add_parser('extractImg', help='extract images in pdf file', usage='%(prog)s FILENAME')
    extractImg._positionals.title = 'Arguments'
    extractImg._optionals.title = 'Command Options'
    extractImg.set_defaults(func=extractImages)
    extractImg.add_argument('filename', help='name of file', metavar='FILENAME')

    compress = subparsers.add_parser('compress', help='compress pdf file (Lossless Compression)', usage='%(prog)s FILENAME')
    compress._positionals.title = 'Arguments'
    compress._optionals.title = 'Command Options'
    compress.set_defaults(func=compressFiles)
    compress.add_argument('filename', help='name of file to compress', metavar='FILENAME')
    
    metadata = subparsers.add_parser('metadata', help='read or Write pdf metadata', usage='%(prog)s (-r | -w) FILENAME')
    metadata._positionals.title = 'Arguments'
    metadata._optionals.title = 'Command Options'
    metadata.set_defaults(func=metadataFiles)
    metadataMutuallyExclusiveGroup = metadata.add_mutually_exclusive_group(required=True)
    metadataMutuallyExclusiveGroup.add_argument('-r', '--read', help='read pdf metadata')
    metadataMutuallyExclusiveGroup.add_argument('-w', '--write', help='write pdf metadata')
    # metadata.add_argument('filename', help='name of file to process', metavar='FILENAME')
    # argument for write
    writeMetadataGroup = metadata.add_argument_group(title='Options for write', description='list of options available for writing metadata')
    writeMetadataGroup.add_argument('--author', help='author\'s name')
    writeMetadataGroup.add_argument('--creator', help='creator\'s name')
    writeMetadataGroup.add_argument('--producer', help='producer\'s name')
    writeMetadataGroup.add_argument('--subject', help='subject')
    writeMetadataGroup.add_argument('--title', help='title')
    writeMetadataGroup.add_argument('--new-filename', help='new file\'s name')

    # pdf2images = subparsers.add_parser('pdf2images', help='convert pdf pages into images')
    # pdf2images._positionals.title = ''
    # pdf2images._optionals.title = ''


    args = parser.parse_args()

    if 'func' in vars(args):
        args.func(args)


def mergeFiles(args):
    arg_dict = vars(args)

    available_files = listAllFiles(UExtension('.pdf'), display=False)
    file_to_merge = []

    # decide file_to_merge
    if arg_dict['all']: # include all files
        file_to_merge = available_files
    else:
        if arg_dict['number_input']: # number input
            file_to_merge = fileSelector('.pdf')
        else:
            if arg_dict['select']: # only selected files
                selected_file = arg_dict['select']

                # add .pdf if filename don't have
                for i in range(len(selected_file)):
                    file = selected_file[i]
                    if not(file.endswith('.pdf')) and not(file.endswith('.PDF')):
                        selected_file[i] = file + '.pdf'
                
                file_to_merge = validateFiles(selected_file)
            else:
                if arg_dict['exclude']: # exclude selected files
                    excluded_file = arg_dict['exclude']
                    # add .pdf if filename don't have
                    for i in range(len(excluded_file)):
                        file = excluded_file[i]
                        if not(file.endswith('.pdf')) and not(file.endswith('.PDF')):
                            excluded_file[i] = file + '.pdf'
                    
                    # validate filename
                    excluded_file = validateFiles(excluded_file)
                    # assign to file_to_merge
                    file_to_merge = set(available_files).difference(set(excluded_file))
    
    # merge file
    if file_to_merge != []:
        mergePdf(file_to_merge, outputFileName=args.output_filename, path=DEFAULT_PDF_PATH)
    else:
        print('No file to merge')

def encryptFiles(args):
    arg_dict = vars(args)
    filename = arg_dict['filename']

    if validateFiles([filename], debug=False) != []:
        encryptPdf(filename, path=DEFAULT_PDF_PATH)
        if arg_dict['remove']:
            os.remove(f'{DEFAULT_PDF_PATH}{filename}')
    else:
        print('NOTE: File not available, make sure to include file extension')

def decryptFiles(args):
    arg_dict = vars(args)
    filename = arg_dict['filename']

    if validateFiles([filename], debug=False) != []:
        decryptPdf(filename, path=DEFAULT_PDF_PATH)
        if arg_dict['remove']:
            os.remove(f'{DEFAULT_PDF_PATH}{filename}')
    else:
        print('NOTE: File not available, make sure to include file extension')

def extractImages(args):
    arg_dict = vars(args)
    filename = arg_dict['filename']

    if validateFiles([filename], debug=False) != []:
        extractImagesFromPdf(filename, path=DEFAULT_PDF_PATH)
    else:
        print('NOTE: File not available, make sure to include file extension')

def compressFiles(args):
    arg_dict = vars(args)
    filename = arg_dict['filename']

    if validateFiles([filename], debug=False) != []:
        compressPdf(filename, path=DEFAULT_PDF_PATH)
    else:
        print('NOTE: File not available, make sure to include file extension')

def metadataFiles(args):
    arg_dict = vars(args)
    if arg_dict['read']:
        filename = arg_dict['read']
    elif arg_dict['write']:
        filename = arg_dict['write']

    if validateFiles([filename], debug=False) != []:
        if arg_dict['read']: # read metadata
            metadata = readMetadataPdf(filename, path=DEFAULT_PDF_PATH)
            
            # display metadata summary
            print(f' Metadata of {filename} '.center(TERMINAL_WIDTH, '='))
            for key, value in metadata.items():
                left_padding = len('page_count') + 5
                right_padding = TERMINAL_WIDTH - left_padding - 1
                print(f'{key:<{left_padding}}:{str(value):>{right_padding}}')
            print('='*TERMINAL_WIDTH)

        elif arg_dict['write']: # write metadata
            newMetadata = {
                'author': arg_dict['author'],
                'creator': arg_dict['creator'],
                'producer': arg_dict['producer'],
                'subject': arg_dict['subject'],
                'title': arg_dict['title'],
            }
            if arg_dict['new_filename']:
                new_filename = arg_dict['new_filename']
            else:
                new_filename = filename
            writeMetadataPdf(fileName=filename, newFilename=new_filename, newMetaData=newMetadata, path=DEFAULT_PDF_PATH)
    else:
        print('NOTE: File not available, make sure to include file extension')

###############################################

def listAllFiles(args, display=True):
    extension = args.extension
    fileNameArray = [file for file in os.listdir(DEFAULT_PDF_PATH) if file.endswith(extension)]
    if display:
        ext = extension.lstrip('.').upper()
        print(f' All Available {ext} Files '.center(TERMINAL_WIDTH, '='))
        for index, file in enumerate(fileNameArray):
            print(f'{index+1} - {file}')
        print('='*TERMINAL_WIDTH)
    return fileNameArray

def fileSelector(extension):
    available_files = listAllFiles(UExtension(extension), display=True)
    selected_files = []

    selection = input("Give file's number seperated by ','/comma \nFile To Merge: ").replace(' ', '').strip(',').split(',')
    for index in selection:
        try:
            index = int(index)
            if 1 <= index <= len(available_files):
                selected_files.append(available_files[index-1])
        except ValueError:
            pass

    return selected_files

def validateFiles(files_array, debug=True):
    ok_list = []
    for file in files_array:
        if os.path.exists(f'{DEFAULT_PDF_PATH}{file}'):
            ok_list.append(file)
        else:
            if debug:
                print(f'NOTE: {file} removed because not exists')
    
    return ok_list

# FUNCTION END HERE

if __name__ == '__main__':
    main()