import argparse
import json
import os
import sys
import urllib.parse
import urllib.request


with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json') as j:
    config = json.load(j)

AUTH_KEY = config['auth_key']
DEEPL_TRANSLATE_EP = 'https://api.deepl.com/v2/translate'
T_LANG_CODES = ["DE", "EN", "FR", "IT", "JA", "ES",
                "NL", "PL", "PT-PT", "PT-BR", "PT", "RU", "ZH"]
S_LANG_CODES = ["DE", "EN", "FR", "IT",
                "JA", "ES", "NL", "PL", "PT", "RU", "ZH"]

p = argparse.ArgumentParser()
p.add_argument('-m', '--message',
               help='text to translate. (Default: Hello World.)',
               default='Hello World.')
p.add_argument('-t', '--target',
               help=f'target language code (Default: JA). allowed lang code : {str(T_LANG_CODES)}',
               default='JA')
p.add_argument('-s', '--source',
               help=f'source language code (Default: auto). allowed lang code : {str(S_LANG_CODES)}',
               default='')
args = p.parse_args()


def translate(text, s_lang='', t_lang='JA'):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; utf-8'
    }

    params = {
        'auth_key': AUTH_KEY,
        'text': text,
        'target_lang': t_lang
    }

    if s_lang != '':
        params['source_lang'] = s_lang

    req = urllib.request.Request(
        DEEPL_TRANSLATE_EP,
        method='POST',
        data=urllib.parse.urlencode(params).encode('utf-8'),
        headers=headers
    )

    try:
        with urllib.request.urlopen(req) as res:
            res_json = json.loads(res.read().decode('utf-8'))
            print(json.dumps(res_json, indent=2, ensure_ascii=False))
    except urllib.error.HTTPError as e:
        print(e)


if __name__ == '__main__':
    t_lang = args.target
    s_lang = args.source
    text = args.message

    if t_lang not in T_LANG_CODES:
        print((
            f'ERROR: Invalid target language code "{t_lang}". \n'
            f'Alloed lang code are following. \n{str(T_LANG_CODES)}'
        ))
        sys.exit(1)

    if s_lang != '' and s_lang not in S_LANG_CODES:
        print((
            f'WARNING: Invalid source Language code "{s_lang}". \n'
            'The source language is automatically determined in this request. \n'
            f'Allowed source lang code are following. \n{str(S_LANG_CODES)} \n\n'
        ))
        s_lang = ''

    translate(text, t_lang=t_lang, s_lang=s_lang)