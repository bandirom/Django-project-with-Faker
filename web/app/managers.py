from django.db.models import Manager


class CompanyManager(Manager):
    quota_size = (
        ('mb', 'MB'),
        ('gb', 'GB'),
        ('tb', 'TB'),
    )


class DataTransferManager(Manager):
    size = (
        ('b', 'B'),
        ('kb', 'kB'),
        ('mb', 'MB'),
        ('gb', 'GB'),
        ('tb', 'TB'),

    )

    def get_data__by_time(self, month, year):
        return self.select_related('user', 'company', 'resource').filter(time__timestamp__month=month,
                                                                         time__timestamp__year=year)

    @staticmethod
    def humanbytes(b):
        """Return the given bytes as a human friendly KB, MB, GB, or TB
            :return tuple('value', 'size')
        """
        b = float(b)
        kb = float(1024)
        mb = float(kb ** 2)  # 1,048,576
        gb = float(kb ** 3)  # 1,073,741,824
        tb = float(kb ** 4)  # 1,099,511,627,776

        if b < kb:
            return f'{b}', 'b'
        elif kb <= b < mb:
            return '{0:.2f}'.format(b / kb), 'kb'
        elif mb <= b < gb:
            return '{0:.2f}'.format(b / mb), 'mb'
        elif gb <= b < tb:
            return '{0:.2f}'.format(b / gb), 'gb'
        elif tb <= b:
            return '{0:.2f}'.format(b / tb), 'tb'

    @staticmethod
    def convert_to_bytes(value, size):
        dct = {'b': 1024, 'kb': 1024 ** 2, 'mb': 1024 ** 3, 'gb': 1024 ** 4}
        return round(float(value) * dct[size] / dct['b'])
