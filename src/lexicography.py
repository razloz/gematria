import json
from gematria import full_test
from multiprocessing import Process, JoinableQueue, cpu_count
from os.path import dirname, realpath, abspath

LATIN_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LATIN_LOWER = 'abcdefghijklmnopqrstuvwxyz'
LATIN_FULL = LATIN_UPPER + LATIN_LOWER
RSRC_PATH = abspath(f'{dirname(realpath(__file__))}/../resources/')
LEXICON_PATH = abspath(f'{RSRC_PATH}/lexicon.json')
HIDDEN_PATH = abspath(f'{RSRC_PATH}/hidden.json')
FAVORITE_PATH = abspath(f'{RSRC_PATH}/favorite.json')
WORDS_PATH = abspath(f'{RSRC_PATH}/words.txt')
LOCO_PATH = abspath(f'{RSRC_PATH}/LOCO.json')
CORES = cpu_count()
WORKER_COUNT = range(CORES)
WORKER_FILES = [abspath(f'{RSRC_PATH}/worker_{i}.words') for i in WORKER_COUNT]


def __sanitize_words_list__():
    """
    Extract words and phrases from words.txt
    """
    print(f'*** Extracting Words: {WORDS_PATH} ***')
    with open(WORDS_PATH, 'r') as rf:
        raw_words = rf.readlines()
    for rw in raw_words:
        pq.put(rw)


def __sanitize_loco_list__():
    """
    Extract words and phrases from loco.json
    """
    print(f'*** Extracting Words: {LOCO_PATH} ***')
    with open(LOCO_PATH, 'r') as rf:
        raw_data = json.load(rf)
    for entry in raw_data:
        pq.put(entry['txt'])


def __create_lexicon__():
    print(f'*** Creating The Lexicon: {LEXICON_PATH} ***')
    lexicon = dict()
    all_words = list()
    for worker_id in WORKER_COUNT:
        with open(WORKER_FILES[worker_id], 'r') as f:
            all_words += f.readlines()
    print(f'*** all_words: {len(all_words)}')
    sorted_words = sorted(set(all_words))
    print(f'*** sorted_words: {len(sorted_words)}')
    for w in sorted_words:
        if 'WWW' in w or 'HTTP' in w:
            print(f'*** REMOVED: {w}')
            continue
        word = w.replace(chr(10), '')
        lexicon[word] = full_test(word)
    with open(LEXICON_PATH, 'w+') as f:
        f.write(json.dumps(lexicon))
    print(f'*** Saved lexicon with {len(lexicon.keys())} entries. ***')


def word_sanity(word):
    """
    Remove all non-alphabetic characters from word.
    """
    for c in list(word):
        if c not in LATIN_FULL:
            word = word.replace(c, "")
    return word


def append_word(queue, worker_id):
    """
    Worker thread for saving a sanitized group of words and phrases to disk.
    """
    print(f'*** Worker ID {worker_id} dispatched. ***')
    file_path = WORKER_FILES[worker_id]
    with open(file_path, 'w+') as f:
        while True:
            qg = queue.get()
            if not qg:
                queue.task_done()
                break
            words = f'{qg}'.replace(":", " ").replace(";", " ").split()
            i = -1
            e = len(words) - 3
            for w in words:
                i += 1
                w = word_sanity(w).upper()
                if len(w) == 0:
                    continue
                f.write(f'{w}\n')
                if w == w.capitalize() and i < e:
                    words_two = None
                    words_three = None
                    w2 = word_sanity(words[i + 1])
                    if len(w2) == 0:
                        continue
                    w3 = word_sanity(words[i + 2])
                    if w2 == w2.capitalize() or w2 == 'of':
                        if w2 != 'of':
                            words_two = f'{w} {w2}'.upper()
                    if w3 == w3.capitalize() and len(w3) != 0:
                        words_three = f'{w} {w2} {w3}'.upper()
                    if words_two:
                         f.write(f'{words_two}\n')
                    if words_three:
                        f.write(f'{words_three}\n')
            queue.task_done()
    print(f'*** Worker ID {worker_id} got exit code. ***')
    return False


if __name__ == '__main__':
    pq = JoinableQueue()
    workers = dict()
    for worker_id in WORKER_COUNT:
        workers[worker_id] = Process(target=append_word, args=(pq, worker_id))
        workers[worker_id].daemon = True
        workers[worker_id].start()
    __sanitize_words_list__()
    __sanitize_loco_list__()
    for worker_id in WORKER_COUNT:
        pq.put(None)
    pq.join()
    __create_lexicon__()
