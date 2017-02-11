# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, you can obtain one at http://mozilla.org/MPL/2.0/.

from zstd import ZstdDecompressor


class StreamingZstd():
    def __init__(self, sb):
        self.sb = sb
        self.zstd = ZstdDecompressor().read_from(sb)
        self.buf = ""

    def grow_buffer(self):
        self.buf = self.buf + self.zstd.next()

    def read(self, n=-1):
        if self.zstd is None:
            return ""
        try:
            while len(self.buf) < n:
                self.grow_buffer()
            result = self.buf[:n]
            self.buf = self.buf[n:]
            return result
        except StopIteration:
            self.zstd = None
            return self.buf

    def close(self):
        self.sb.close()


def streaming_zstd_wrapper(body):
    return StreamingZstd(body)
