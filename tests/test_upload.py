import unittest
from image_uploader import app
from io import BytesIO

from flask import url_for, Request
from werkzeug.datastructures import FileStorage, MultiDict


# Mock FileStorage.
# Gotten from: https://github.com/srusskih/flask-uploads/blob/master/flaskext/uploads.py with some modifications
class TestingFileStorage(FileStorage):
    """
    This is a helper for testing upload behavior in your application. You
    can manually create it, and its save method is overloaded to set `saved`
    to the name of the file it was saved to. All of these parameters are
    optional, so only bother setting the ones relevant to your application.

    :param stream: A stream. The default is an empty stream.
    :param filename: The filename uploaded from the client. The default is the
                     stream's name.
    :param name: The name of the form field it was loaded from. The default is
                 ``None``.
    :param content_type: The content type it was uploaded as. The default is
                         ``application/octet-stream``.
    :param content_length: How long it is. The default is -1.
    :param headers: Multipart headers as a `werkzeug.Headers`. The default is
                    ``None``.
    """
    def __init__(self, stream=None, filename=None, name=None,
                 content_type='application/octet-stream', content_length=-1,
                 headers=None):
        FileStorage.__init__(
            self, stream, filename, name=name,
            content_type=content_type, content_length=content_length,
            headers=None)
        self.saved = None

    def save(self, dst, buffer_size=16384):
        """
        This marks the file as saved by setting the `saved` attribute to the
        name of the file it was saved to.

        :param dst: The file to save to.
        :param buffer_size: Ignored.
        """
        # if isinstance(dst, basestring):
        #     self.saved = dst
        # else:
        #     self.saved = dst.name
        self.saved = dst


class FlaskAppUploadFileTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app

        self.app.config['TESTING'] = True
        self.app.config['CSRF_ENABLED'] = False

    def test_status_code(self):
        class TestingRequest(Request):
            """A testing request to use that will return a
            TestingFileStorage to test the uploading."""

            @property
            def files(self):
                d = MultiDict()
                d['photo'] = TestingFileStorage(filename=filename)
                return d

        # Loop over some files and the status codes that we are expecting
        for filename, status_code in \
                (('foo.png', 201), ('foo.pdf', 400), ('foo.jpg', 201), ('foo.doc', 400),
                 ('foo.jpeg', 201), ('foo.py', 400), ('foo', 400), ('foo.gif', 201)):

            # Tell flask app to use our custom Request
            self.app.request_class = TestingRequest

            test_client = self.app.test_client()

            # We need to work within the request context
            with self.app.test_request_context():
                rv = test_client.post(
                    url_for('index'),
                    data=dict(
                        file=(BytesIO(), filename),
                    ),
                    content_type='multipart/form-data'
                )

                self.assertEqual(rv.status_code, status_code)

                rv_filename = rv.headers.get('X-Filename')

                if rv_filename:
                    self.assertEqual(rv_filename, filename)


if __name__  == '__main__':
    unittest.main()
