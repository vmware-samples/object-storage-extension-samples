from faker import Faker
import random
import string


class FakerUtil:
    def __init__(self):
        self.fake = Faker()

    def gen_btk_n(self, length=9):
        str_list = [random.choice(string.digits + string.ascii_lowercase + './') for _ in range(length)]
        random_str = ''.join(str_list)
        return random_str

    '''
    https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-s3-bucket-naming-requirements.html

    The bucket name can be between 3 and 63 characters long, and can contain only lower-case characters, numbers, periods, and dashes.

    Each label in the bucket name must start with a lowercase letter or number.

    The bucket name cannot contain underscores, end with a dash, have consecutive periods, or use dashes adjacent to periods.

    The bucket name cannot be formatted as an IP address (198.51.100.24).
    '''

    def invalid_bkt_n(self):
        invalid_name_list = []

        name_with_blank = self.gen_btk_n() + ' ' + self.gen_btk_n()
        invalid_name_list.append(name_with_blank)

        name_len_lt_3 = self.gen_btk_n(length=2)
        invalid_name_list.append(name_len_lt_3)

        name_len_gt_63 = self.gen_btk_n(length=64)
        invalid_name_list.append(name_len_gt_63)

        name_start_with_period = '.'+self.gen_btk_n()
        invalid_name_list.append(name_start_with_period)

        name_start_with_dash = '/'+self.gen_btk_n()
        invalid_name_list.append(name_start_with_dash)

        invalid_c = random.choice('!@#$%^&*()')
        name_with_invalid_c = self.gen_btk_n() + invalid_c
        invalid_name_list.append(name_with_invalid_c)

        # name_format_as_ip =

        return random.choice(invalid_name_list)


if __name__ == "__Main__":
    f = FakerUtil()
    print(f.invalid_bkt_n())


