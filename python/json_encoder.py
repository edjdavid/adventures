import json
import pandas as pd


class PandasEncoder(json.JSONEncoder):
    __make_iterencode = None

    def default(self, o):
        # convert tz naive datetime to tz aware before converting to unix epoch
        if isinstance(o, pd.Timestamp):
            if o.tz is None:
                o = o.tz_localize('Asia/Manila')
            return o.value / 10**9  # value is in nanoseconds

        return pd.io.json.dumps(o)

    def encode(self, o):
        """Dirty hack to allow overriding the float encoder

        """
        __c_make_encoder = json.encoder.c_make_encoder
        self.__make_iterencode = json.encoder._make_iterencode

        json.encoder.c_make_encoder = None
        json.encoder._make_iterencode = self._make_iterencode

        try:
            return super(PandasEncoder, self).encode(o)

        finally:
            json.encoder.c_make_encoder = __c_make_encoder
            json.encoder._make_iterencode = self.__make_iterencode

    def _make_iterencode(self, markers, _default, _encoder, _indent, _floatstr,
                         *args, **kwargs):
        """Signature copied from JSON source

        """
        _floatstr = self.float_encoder
        return self.__make_iterencode(markers, _default, _encoder,
                                      _indent, _floatstr, *args, **kwargs)

    @staticmethod
    def float_encoder(o, allow_nan=True,
                      _repr=json.encoder.FLOAT_REPR,
                      _inf=json.encoder.INFINITY,
                      _neginf=-json.encoder.INFINITY):
        if o != o:
            text = '"NaN"'
        elif o == _inf:
            text = '"Infinity"'
        elif o == _neginf:
            text = '"-Infinity"'
        else:
            return _repr(o)

        if not allow_nan:
            raise ValueError(
                "Out of range float values are not JSON compliant: " +
                repr(o))

        return text
