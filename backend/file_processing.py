from ebooklib import epub

#since the library gives error when processing an bytes object, this method gets stays on hold for the moment

class MissingMetadataError(Exception):
    pass

def get_epub_metadata(epub_file):
    try:
        book = epub.read_epub(epub_file)
        
        title = book.get_metadata('DC', 'title')
        if not title:
            raise MissingMetadataError("Title metadata is missing in the EPUB file")
        
        
        author = book.get_metadata('DC', 'creator')
        if not author:
            raise MissingMetadataError("Creator metadata is missing in the EPUB file")

        return {'title': title[0][0], 'creator': author[0][0]}

    except Exception as e:
        raise ValueError(f"Error processing {epub_file}: {e}")