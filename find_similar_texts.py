import re
from pathlib import Path
from collections import defaultdict

from helpers import Agreement, pre_process, tib_sort
from nalanda_formatting import extract_nalanda

# ཡིག་ཆ་ཚང་མ་བཏང་དགོས་ན། all ཞེས་ཕྲིས། ཡིག་ཆ་གཅིག་བཏང་དགོས་ན་དེའི་མིང་ཕྲིས། དཔེར་ན། "D1129" ལྟ་བུ།
mode = "all"


def reinsert_numbers(chunks):
    out = []
    for i in range(len(chunks)):
        out.append([i + 1,  chunks[i]])

    return out


def format_canon_input(text):
    text = re.sub(r'\..', '', text)  # remove line numbers
    text = re.sub(r'[^\]]\[[0-9]+?[ab]\]([^\r\n][^\[])', r'\1', text)  # remove line numbers
    text = re.sub(r'\{D[0-9]+[ab]?\}', '', text)  # remove volume id
    chunks = text.replace('\n', '').split('#')
    chunks = reinsert_numbers(chunks)
    return chunks


def extract_last_note_number(text):
    text = text.strip()
    _, end = text.rsplit('\n', maxsplit=1)
    ref, _ = end.split('.', maxsplit=1)
    return int(ref)


def format_notes(content):
    formatted = {}
    count = 1
    for line in content.strip().split('\n')[1:]:
        line = line.replace('\ufeff', '')
        parts = line.split(',')
        title, page_num, num, note_num = parts[:4]
        rest = parts[4:]
        limit = False
        entry = {}
        for i in range(0, len(rest), 2):
            eds = rest[i]
            if not eds:
                limit = True
            if limit:
                continue
            note = rest[i+1]

            eds = eds.replace('》《', ',').replace('》', '').replace('《', '').split(',')
            for e in eds:
                entry[e] = note

        formatted[count] = entry

        count += 1
    return formatted


def group_syllables(structure):
    grouped = []
    tmp = []
    for u in structure:
        if type(u) != dict:
            tmp.append(u)
        else:
            grouped.append(tmp)
            grouped.append(u)
            tmp = []
    if tmp:
        grouped.append(tmp)
    return grouped


def format_footnote(note, chosen, ref):
    punct = ['༄', '༅', '༆', '༇', '༈', '།', '༎', '༏', '༐', '༑', '༔', '་', ' ']

    def agree_zhas(chosen_ed):
        last_syl = pre_process(chosen_ed, mode='syls')[-1]
        return Agreement().part_agreement(last_syl, 'ཞེས')

    def is_punct(string):
        ok = True
        for s in string:
            if s not in punct:
                ok = False
        return ok

    def strip_punct(string):
        if is_punct(string):
            return string

        while string != '' and string[-1] in punct:
            string = string[:-1]
        return clean_ed_text(string)

    def clean_ed_text(ed):
        return ''.join(ed).replace(' ', '').replace('#', '').replace('_', ' ')

    def strip_similar_to_chosen(note, chosen_ed):
        stripped = {}
        for k, v in note.items():
            if k != chosen_ed:
                stripped[k] = v
        return stripped

    if chosen == 'K':
        try:
            stripped_note = strip_similar_to_chosen(note, 'སྡེ་')
        except KeyError:
            stripped_note = strip_similar_to_chosen(note, 'པེ་')
        ordered = defaultdict(list)
        for k, v in stripped_note.items():
            ordered[strip_punct(v)].append(k)
        # ཞེས་པར་མ་གཞན་ནང་མེད། for all notes where Derge adds something.
        if not [a for a in ordered.keys() if a != '']:
            try:
                return '{}: {}། ཞེས་པར་མ་གཞན་ནང་མེད།'.format(ref, strip_punct(''.join(note['སྡེ་'])))
            except KeyError:
                final = ''
                full_names = {'སྡེ་': 'སྡེ་དགེ', 'ཅོ་': 'ཅོ་ནེ', 'པེ་': 'པེ་ཅིན', 'སྣར་': 'སྣར་ཐང་'}
                for text in tib_sort(ordered.keys()):
                    if text != '':
                        if is_punct(text):
                            final += text + ' '
                        else:
                            final += text + '། '
                        ed_names = [full_names[clean_ed_text(ed)] for ed in tib_sort(ordered[text]) if ed != 'ཞོལ་']
                        final += '། '.join(ed_names) + '།'
                return '{}: {}'.format(ref, final)
        else:
            final = ''
            full_names = {'སྡེ་': 'སྡེ་དགེ', 'ཅོ་': 'ཅོ་ནེ', 'པེ་': 'པེ་ཅིན', 'སྣར་': 'སྣར་ཐང་'}
            for text in tib_sort(ordered.keys()):
                if text != '':
                    if is_punct(text):
                        final += text + ' '
                    else:
                        final += text + '། '
                    ed_names = [full_names[clean_ed_text(ed)] for ed in tib_sort(ordered[text]) if ed != 'ཞོལ་']
                    final += '། '.join(ed_names) + '།'
            return '{}: {}'.format(ref, final)

    elif chosen == 'b':
        derge = strip_punct(clean_ed_text(note['སྡེ་']))
        both = strip_punct(clean_ed_text(note['སྣར་']))
        zhas = agree_zhas(both)
        return '{}: མ་དཔེར་{}། བྱུང་ཡང་པེ་ཅིན་དང་སྣར་ཐང་བཞིན། {}། {}་བཅོས།'.format(ref, derge, both, zhas)
    elif chosen == 'n':
        derge = strip_punct(clean_ed_text(note['སྡེ་']))
        narthang = strip_punct(clean_ed_text(note['སྣར་']))
        zhas = agree_zhas(narthang)
        return '{}: མ་དཔེར་{}། བྱུང་ཡང་སྣར་ཐང་བཞིན། {}། {}་བཅོས།'.format(ref, derge, narthang, zhas)
    elif chosen == 'p':
        derge = strip_punct(clean_ed_text(note['སྡེ་']))
        pecing = strip_punct(clean_ed_text(note['པེ་']))
        zhas = agree_zhas(pecing)
        return '{}: མ་དཔེར་{}། བྱུང་ཡང་པེ་ཅིན་བཞིན། {}། {}་བཅོས།'.format(ref, derge, pecing, zhas)


def content_to_dict(content):
    out = {}
    count = 0
    for num, c in content:
        assert num - 1 == count, f'There is a problem with the slot of note {num}. It should have been {count}'
        out[num] = c
        count = num
    return out


def insert_notes(content, notes):
    content = content_to_dict(content)
    count = 0
    text = []
    footnotes = []
    for note_num in content:
        assert note_num - 1 == count

        if note_num == len(content) and len(content) == len(notes) + 1:
            text.append(content[note_num])
            break
        elif len(content) > len(notes) + 1:
            raise ValueError('notes and content don"t match')

        # get data
        note = notes[note_num]
        chunk = content[note_num]

        # process data
        ref = f'[^{note_num}K]'
        if note:
            text.append(f'{chunk}{ref}')
            formatted_note = format_footnote(note, 'K', ref)
            footnotes.append(formatted_note)
        else:
            text.append(f'{chunk}')
            formatted_note = ''
            footnotes.append(formatted_note)

        # increment count
        count = note_num

    return text, footnotes


def insert_report_notes(content, notes):
    content = content_to_dict(content)
    count = 0
    text = []
    footnotes = []
    for note_num in content:
        assert note_num - 1 == count

        if note_num >= len(notes):
            break

        if note_num == len(content) and len(content) == len(notes) + 1:
            text.append(content[note_num])
            break

        # get data
        note = notes[note_num]
        chunk = content[note_num]

        # process data
        ref = f'[^{note_num}K]'
        if note:
            text.append(f'{chunk}{ref}')
            formatted_note = format_footnote(note, 'K', ref)
            footnotes.append(formatted_note)
        else:
            text.append(f'{chunk}')
            formatted_note = ''
            footnotes.append(formatted_note)

        # increment count
        count = note_num

    return text, footnotes


def format_new_text(text, footnotes):
    text = ''.join(text)
    footnotes = '\n'.join(footnotes)
    return f'{text}\n\n{footnotes}'


def insert_notes_in_text(text, footnotes):
    l_text, l_note = len(text), len(footnotes)
    if l_text < l_note:
        text.extend(['' for t in range(abs(l_text - l_note))])
    if l_note < l_text:
        footnotes.extend(['' for t in range(abs(l_text - l_note))])

    pairs = [f'{t}【{n}】' for t, n in zip(text, footnotes)]
    return pairs


def generate_report(text, footnotes):
    pairs = insert_notes_in_text(text, footnotes)
    parts = []
    if len(pairs) <= 3:
        parts.append((0, len(pairs) - 1))
    elif len(pairs) <= 10:
        parts.append((0, 3))
        parts.append((len(pairs)-4, len(pairs)-1))
    else:
        beginning = (0, 3)
        end = (len(pairs) - 4, len(pairs) - 1)
        middle = []
        for i in range(4, len(pairs), 7):
            middle.append((i, i + 3))
        parts = [beginning] + middle + [end]

    report = []
    for a, b in parts:
        report.append(''.join(pairs[a:b]))
    return '\n\n'.join(report)


def log_overview(text, footnotes, overview, filename):
    pairs = insert_notes_in_text(text, footnotes)

    begin = ''.join(pairs[:5])
    end = ''.join(pairs[-5:])
    overview.write(f',{filename},{begin},{end}\n', encoding='utf-8')
    overview.flush()


def main(mode):
    # find files
    c_path = Path('canon_notes_input')
    canon_files = list(c_path.glob('*.txt'))
    d_path = Path('output/works')
    derge_files = list(d_path.glob('*.txt'))

    # list files to process
    nalanda_derge = []
    canon_stems = [c.stem for c in canon_files]
    for c in derge_files:
        if c.stem in canon_stems:
            nalanda_derge.append(c)

    log = Path('log.txt').open('w', -1, encoding='utf-8')
    # overview = Path('overview.csv').open('w')

    Path('output').mkdir(exist_ok=True)
    log_path = Path('output/log')
    log_path.mkdir(exist_ok=True)
    for f in log_path.glob('*.*'):
        f.unlink()

    problem_path = Path('output/problem')
    problem_path.mkdir(exist_ok=True)
    for p in problem_path.glob('*.*'):
        p.unlink()

    final_path = Path('output/final')
    final_path.mkdir(exist_ok=True)
    for f in final_path.glob('*.*'):
        f.unlink()

    ok = 0
    no = 0
    for n in sorted(nalanda_derge):
        if mode != 'all':
            if n.stem != mode:
                continue
        # open and format contents
        d_content = n.read_text(encoding='utf-8')
        d_content = format_canon_input(d_content)
        c_content = Path(c_path / n.name).read_text(encoding='utf-8')

        # get last note number
        d_num = d_content[-1][0]
        c_num = extract_last_note_number(c_content)

        notes_content = Path(Path('canon_notes_input/') / str(n.stem + '.csv')).read_text(encoding='utf-8')
        notes = format_notes(notes_content)

        # the amount of notes is not the same, so the file can't be processed.
        if abs(d_num - c_num) != 0:
          
            print(f'{n.name}\tc\t{c_num}\td\t{d_num}')
            log.write(f'{n.name}\tc\t{c_num}\td\t{d_num}\n')
            no += 1
            text, footnotes = insert_report_notes(d_content, notes)
            report = generate_report(text, footnotes)
            report_file = problem_path / n.name
            report_file.write_text(report, encoding='utf-8')


        # the file can be processed
        else:
            print('\t', n.name)
            ok += 1

            text, footnotes = insert_notes(d_content, notes)
            # log_overview(text, footnotes, overview, n.stem)
            report = generate_report(text, footnotes)
            report_file = log_path / n.name
            report_file.write_text(report, encoding='utf-8')

            out = format_new_text(text, footnotes)
            final_file = final_path / n.name
            final_file.write_text(out, encoding='utf-8')

    print(f'files ok: {ok}, note amount discrepancy: {no}')
    log.write(f'files ok: {ok}, note amount discrepancy: {no}', encoding='utf-8')
    log.flush()
    log.close()
    # overview.flush()
    # overview.close()

extract_nalanda()
main(mode)
