# A. High level Flow
# 1. Search root directory tree and return list of files with same extension
# 2. For each file:
#        open, read and correct it and store corrected version in same place
#        with option of deleting source file
#
# B. MathJaxCorrector
# 1. TBC

import abc
import re
from pathlib import Path
from bs4 import BeautifulSoup

class FileManager:
    '''Parse root directory tree structure recursively. Find files matching
    regex string, opens, corrects and saves new version in same location as
    origin. Parse files content and correct it using sequence of processors.

    Arguments:
        root_dir: String, root directory to start from.
        file_match_pattern: String, glob-style pattern to match selected files
        processors: List of Processor instances.
        delete_origin: Bool, to delete origin files. Default False. If False
            origin files are kept.
        file_suffix: String, to construct name of corrected file. It attaches
            after origin file name prior extension. If Default value None is
            kept and delete_origin is True 'fixed' is used as default.
    '''

    def __init__(self, root_dir, file_match_pattern, processors,
                 delete_origin=False, file_suffix=None):
        self.root_dir = root_dir
        self.file_match_pattern = re.compile(file_match_pattern)
        self.processors = processors
        self.delete_origin = delete_origin

        if (not file_suffix) and (not delete_origin):
            self.file_suffix = 'fixed'
        else
            self.file_suffix = file_suffix if file_suffix else ''

    def files(self):
        '''Generator returning Path of next selected file for processing.'''
        for dirpath, _, filenames in os.walk(self.root_dir):
            for name in filenames:
                path = Path(dirpath, name)
                if path.match(self.file_match_pattern):
                    yield path

    def process(self):
        '''Process selected files'''
        for path in self.files():
            outfile_name = (path.name + self.file_suffix + path.suffix)
            outfile_path = infile_path.parent / outfile_name
            inffile_path = path

            for processor in self.processors:
                processor.process(infile_path, outfile_path)
                infile_path = outfile_path

            if (path != outfile_path) and self.delete_origin:
                os.remove(path)


class Corrector(metaclass=abc.ABCMeta):
    '''Abstract class for Processor.'''

    def process(self, infile_path, outfile_path):
        '''Basic process method for proper hanlding of files. Reading from,
        processing and writing to file should be implemented in
        internal _process method of derived class.

        Arguments:
            infile_path: Path object, path of the origin file.
            outfile_path: Path of the corrected file. If same with
                infile_path origin file is overwritten
        '''
        if infile_path == outfile_path:
            infile = open(infile_path, 'wb')
            outfile = infile
        else:
            infile = open(infile_path, 'rb')
            outfile = open(outfile_path, 'wb')

        self.infile_ = infile
        self.outfile_ = outfile

        self._process()

        self.outfile_.close()
        if infile_path != outfile_path:
            self.infile_.close()

    @abstractclass
    def _process():
        pass

class MathJaxCorrector(Processor):
    '''Correct broken mathjax expression due to tag signs "<", ">"
    incorrectly rendered as html tags.

    Arguments:
        tag_kws: Dictionary of keyword arguments for identifying
            tags with Mathjax expressions
        soup_kws: Dictionary of keyword arguments for BeautifulSoup object
    '''

    def __init__(tag_kws, soup_kws):
        self.find_kws = tag_kws
        self.soup_kws = soup_kws

    def _process(self):
        # read content
        self.dom_ = BeautifulSoup(self.infile_, **soup_kws)

        # correct content
        self._correct_tag(self.dom_)

        # write content
        content = self.dom_.prettify(self.dom_.original_encoding)
        self.outfile_.write(content)

    def _correct_tag(self, tag):
        tags = tag.findall(self.tag_kws)
        if tags:
            # traverse DOM until relevant tag does not have relevant child
            for tag in tags:
                self._correct_tag(tag)
        else:
            # find broken tag and replace it
            self._replace_tag(tag)

    def _replace_tag(self, parent_tag):
        html = parent_tag.prettify()

        mathjax_tag_stack = []
        html_tag_stack = []

        for tag in match_tag(html):

            if isinstance(tag, MathJaxTag):
                if (not mathjax_tag_stack) or mathjax_tag_stack[-1].closed:
                    # pop out closed mathjax tag from stack
                    mathjax_tag_stack.pop()
                else:
                    # put open mathjax tag to stack
                    mathjax_tag_stack.append(tag())

            if isinstance(tag, HtmlTag):
                if (not html_tag_stack) or html_tag_stack[-1].closed:
                    if tag.broken:
                        # delete closed broken tag in html
                        html = tag.delete(html)

                    # pop out closed html tag from stack
                    html_tag_stack.pop()
                else:
                    if (not math_tag_stack) or mathjax_tag_stack[-1].closed:
                        # put valid html tag in stack
                        html_tag_stack.append(tag())
                    else:
                        # flag open broken html tag
                        tag.broken = True
                        # replace broken open html tag in html
                        html = tag.replace(html)
                        # put broken open html tag in stack
                        html_tag_stack.append(tag())

        if (not html_tag_stack) and (not mathjax_tag_stack):
            raise Exception('Broken html code:\n', HtmlTag)

        HtmlTag.replace_with(BeautifulSoap(html))
