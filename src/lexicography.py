"""
Module for extracting and filtering words to save in a uniform format.
"""
import json
from gematria import full_test
from multiprocessing import Process, JoinableQueue, cpu_count
from os.path import dirname, realpath, abspath

RSRC_PATH = f'{dirname(realpath(__file__))}/../resources'
WORDS_PATH = abspath(f'{RSRC_PATH}/words.txt')
LOCO_PATH = abspath(f'{RSRC_PATH}/LOCO.json')
HISTORY_PATH = abspath(f'{RSRC_PATH}/history.json')
LEXICON_PATH = abspath(f'{RSRC_PATH}/lexicon.json')
CORES = cpu_count()
WORKERS = dict()
WORKER_COUNT = range(CORES)
WORKER_FILES = [abspath(f'{RSRC_PATH}/worker_{i}.words') for i in WORKER_COUNT]
EN_FULL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
FILTER = """[]{}|\;:',.<>/?!@#$%^&*()_+-=`~""" + '''"'''


def __sanitize_words_list__(queue):
    """
    Extract words and phrases from words.txt
    """
    print(f'*** Extracting Words: {WORDS_PATH} ***')
    with open(WORDS_PATH, 'r') as f:
        raw_words = f.readlines()
    for rw in raw_words:
        queue.put(rw)


def __sanitize_loco_list__(queue):
    """
    Extract words and phrases from loco.json
    """
    print(f'*** Extracting Words: {LOCO_PATH} ***')
    with open(LOCO_PATH, 'r') as f:
        raw_data = json.load(f)
    for entry in raw_data:
        queue.put(entry['txt'])


def __create_lexicon__():
    print(f'*** Creating the lexicon... ***')
    lexicon = dict()
    all_words = list()
    for worker_id in WORKER_COUNT:
        with open(WORKER_FILES[worker_id], 'r') as f:
            all_words += f.readlines()
    print(f'*** all_words: {len(all_words)}')
    sorted_words = sorted(set(all_words))
    print(f'*** sorted_words: {len(sorted_words)}')
    for w in sorted_words:
        for skippable in ['WWW','HTTP','HTML']:
            if skippable in w:
                continue
        word = w.replace(chr(10), '')
        lexicon[word] = full_test(word)
    with open(LEXICON_PATH, 'w+') as f:
        json.dump(lexicon, f)
    with open(HISTORY_PATH, 'w+') as f:
        json.dump(dict(), f)
    print(f'*** Finished creating the lexicon with {len(lexicon)} entries. ***')


def word_sanity(word):
    """
    Remove all non-alphabetic characters from word.
    """
    for c in list(word):
        if c not in EN_FULL:
            word = word.replace(c, "")
    return word


def append_word(queue, worker_id):
    """
    Worker thread for saving a sanitized group of words and phrases to disk.
    """
    file_path = WORKER_FILES[worker_id]
    print(f'*** Worker {worker_id}: {file_path} ***')
    with open(file_path, 'w+') as f:
        while True:
            qg = queue.get()
            if not qg:
                queue.task_done()
                break
            for fc in FILTER:
                qg = qg.replace(fc, " ")
            words = qg.split()
            i = -1
            e = len(words) - 3
            for w in words:
                i += 1
                w = word_sanity(w)
                w_len = len(w)
                if w_len < 3 or w_len > 13:
                    continue
                f.write(f'{w}\n'.upper())
                if w == w.capitalize() and i < e:
                    w2 = word_sanity(words[i + 1])
                    w2_len = len(w2)
                    if w2_len < 2 or w2_len > 13:
                        continue
                    if w2 == w2.capitalize() or w2 == 'of':
                        if w2 != 'of':
                            f.write(f'{w} {w2}\n'.upper())
                    w3 = word_sanity(words[i + 2])
                    w3_len = len(w3)
                    if w3_len < 3 or w3_len > 13:
                        continue
                    if w3 == w3.capitalize():
                        f.write(f'{w} {w2} {w3}\n'.upper())
            queue.task_done()
    print(f'*** Worker {worker_id}: got exit signal. ***')
    return False


if __name__ == '__main__':
    job_queue = JoinableQueue()
    for wid in WORKER_COUNT:
        WORKERS[wid] = Process(target=append_word, args=(job_queue, wid))
        WORKERS[wid].daemon = True
        WORKERS[wid].start()
    __sanitize_words_list__(job_queue)
    __sanitize_loco_list__(job_queue)
    for wid in WORKER_COUNT:
        job_queue.put(None)
    job_queue.join()
    __create_lexicon__()
