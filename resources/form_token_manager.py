import random
import string
from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from resources.authentication import SECRET_KEY, ALGORITHM

pwd_context_form = CryptContext(schemes=["bcrypt"], deprecated="auto")


class FormToken:

    @staticmethod
    def encode_data(data_dict: dict, exp: timedelta | None):
        split_key: str = '?'
        if exp:
            expire_until = datetime.now(timezone.utc) + exp
            data_dict.update({"exp": expire_until})
        encoded_jwt = jwt.encode(data_dict, SECRET_KEY, algorithm=ALGORITHM)
        coded = str()
        numbers = '.-_1234567890'
        all_chars = '~+=!@#$%^&*()'
        new_text = encoded_jwt
        for txt in encoded_jwt:
            if txt in numbers:
                new_text = new_text.replace(txt, all_chars[numbers.index(txt)])
        abc = string.ascii_letters + all_chars
        len_hasher = len(abc)
        abc1 = str()
        rand_abc = random.randint(0, len_hasher - 1)
        for let in range(len_hasher):
            abc1 += abc[(rand_abc + let) % len_hasher]
        abc2 = all_chars + string.ascii_letters + all_chars
        code = f"{bin(rand_abc)[2:]}" + split_key
        for char in new_text:
            real_char = abc1[abc2.index(char)]
            ind_rand = random.randint(0, 3)
            for i in range(4):
                nm = random.randint(0, len_hasher - 1)
                rand_char1 = abc1[nm]
                if ind_rand == i:
                    code += real_char
                else:
                    code += rand_char1
            code += split_key + bin(int(bin(ind_rand)[2:]))[2:] + split_key
        code = code[:-(len(split_key))]
        coded += code[::-1]
        return coded + '-' + pwd_context_form.hash(encoded_jwt)

    @staticmethod
    def decode_data(coded_data: str, split_key='?'):
        encoded_jwt_verify = coded_data.split('-')[-1]
        coded_data = coded_data[:coded_data.index('-')]
        numbers = '.-_1234567890'
        all_chars = '~+=!@#$%^&*()'
        decoded = str()
        _text = coded_data[::-1]
        codes = _text.split(split_key)[0]
        cut_ind = _text[_text.index(split_key) + len(split_key):]
        rand_abc = int(codes, 2)
        bins = cut_ind.split(split_key)[::-2]
        chars = cut_ind.split(split_key)[::2]
        abc = string.ascii_letters + all_chars
        len_hasher = len(abc)
        abc1 = str()
        abc2 = all_chars + string.ascii_letters
        for let in range(len_hasher):
            abc1 += abc[(rand_abc + let) % len_hasher]
        decs = []
        for bin_nm in bins:
            sort_1 = int(f"0b{bin_nm}", 2)
            sort_2 = int(f"0b{sort_1}", 2)
            decs.append(sort_2)
        decs.reverse()
        char_sort1 = str()
        ind = 0
        for char_nm in chars:
            get_ind = (decs[ind])
            char_sort1 += char_nm[get_ind]
            ind += 1
        char_sort2 = str()
        for char_nm in char_sort1:
            char_sort2 += abc2[abc1.index(char_nm)]
        decoded += f"{char_sort2} "
        result = decoded[:-1]
        for txt in result:
            if txt in all_chars:
                result = result.replace(txt, numbers[all_chars.index(txt)])
        payload = jwt.decode(result, SECRET_KEY, algorithms=[ALGORITHM])
        if pwd_context_form.verify(result, encoded_jwt_verify):
            return payload
        raise TypeError
