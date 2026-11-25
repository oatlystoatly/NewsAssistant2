"""Bob Bot: offline rule-based interaction prototype, not an LLM."""
from pathlib import Path
import re
from copy import deepcopy

SOURCE_DIR = Path(__file__).parent / 'sources'
TYPES = {'news': 'News', 'academic': 'Academic', 'social_media': 'Social media'}

def load_sources():
    records = []
    for path in sorted(SOURCE_DIR.glob('*.md')):
        try:
            _, header, body = path.read_text(encoding='utf-8-sig').split('---', 2)
            meta = dict(line.split(':', 1) for line in header.splitlines() if ':' in line)
            meta = {k.strip(): v.strip() for k, v in meta.items()}
            if meta.get('source_type', '').casefold() == 'tiktok':
                meta['source_type'] = 'social_media'
            if not {'source','section','updated','source_type','superseded'} <= meta.keys():
                raise ValueError('missing metadata')
            if meta['source_type'] not in TYPES or meta['superseded'].lower() not in ('true','false'):
                raise ValueError('invalid source type or superseded flag')
            records.append({**meta, 'body': body.strip()})
        except (OSError, ValueError) as exc:
            print(f'Warning: {path.name}: {exc}')
    return records

def preferences(text):
    t = text.lower().strip()
    if re.fullmatch(r'[abc](?:[ ,]+[abc])*', t):
        return {list(TYPES)[ord(letter) - ord('a')] for letter in re.findall(r'[abc]', t)}
    return {k for k,p in [('news',r'\bnews\b'),('academic',r'\bacademic\b'),('social_media',r'\bsocial media\b|\btiktok\b')] if re.search(p,t)}

def names(types):
    return ', '.join(TYPES[k] for k in TYPES if k in types) or 'Not specified'

def interpret(text):
    t = text.lower()
    if 'black sabbath' in t:
        topic = 'Black Sabbath'
    elif ('selly oak' in t or 'selly bin' in t) and re.search(r'bin|strike|waste',t):
        topic = 'Selly Oak bin strikes'
    else:
        return None
    # Limited intent rules; negated or complex source instructions need clarification.
    uncertain = bool(re.search(r'\b(not|except|without|rather than|exclude|no)\b',t))
    all_sources = bool(re.search(r'\ball\b',t)) and not uncertain
    types = set(TYPES) if all_sources else (set() if uncertain else preferences(t))
    recency = 'recent' if re.search(r'\b(current|latest|recent)\b',t) else ('recent (inferred from updates)' if 'updates' in t else None)
    return dict(topic=topic, location='Selly Oak' if topic.startswith('Selly') else ('Birmingham' if 'birmingham' in t else None), purpose='report' if 'report' in t else None, types=types, all=all_sources, recency=recency, origin='explicit' if types else 'missing', original=text, uncertain=uncertain)

def retrieve(request):
    matching, excluded = [], []
    for r in load_sources():
        if r['section'].casefold() != request['topic'].casefold():
            reason = 'Different topic'
        elif not request['all'] and r['source_type'] not in request['types']:
            reason = 'Source type not selected'
        elif r['superseded'].lower() == 'true' and not request['all']:
            reason = 'Superseded; current-only filter'
        else:
            matching.append(r); continue
        excluded.append((r,reason))
    type_order = {kind: index for index, kind in enumerate(TYPES)}
    matching.sort(key=lambda r: (type_order[r['source_type']], r['source'].casefold()))
    return matching, excluded

class BobBot:
    def __init__(self):
        self.reset()
    def reset(self):
        self.request = None
        self.history = []
        self.selections = []
        self.requests = []
        self.records = []
        self.available_records = []
        self.excluded = []
        self.state = 'idle'
    def say(self, message):
        print('Bob Bot: '+message)
        self.history.append(('Bob Bot',message))
    def options(self):
        self.say('Source options: a. News | b. Academic | c. Social media. Choose one or more, e.g. a, c.')
    def clarify(self):
        self.state = 'clarify'
        self.say('What sort of update source would you like?')
        self.options()
        if self.selections:
            self.say('Previous selection: '+names(self.selections[-1])+'. Type use previous to explicitly reuse it, or choose new sources.')
    def context(self):
        r = self.request
        if not r:
            self.say('No active request.'); return
        explicit = [f"Topic: {r['topic']}"]
        missing, inferred = [], []
        for k in ('location','purpose','recency'):
            v = r[k]
            (missing if not v else inferred if 'inferred' in v else explicit).append(f'{k.title()}: {v or "Not specified"}')
        (missing if not r['types'] else explicit).append('Sources: '+names(r['types'])+' ('+r['origin']+')')
        if r['all']: explicit.append('Include all available records, including superseded')
        else: inferred.append('Default filter: exclude superseded records')
        self.say('Current request\nExplicit / user-confirmed: '+ '; '.join(explicit)+'\nInferred / default: '+('; '.join(inferred) or 'None')+'\nMissing: '+('; '.join(missing) or 'None')+'\nState: '+self.state+'\nMissing purpose alone does not prevent retrieval.')
    def display(self):
        self.available_records,self.excluded = retrieve(self.request)
        self.records = []
        self.state = 'select_record'
        source_types = 'All (including other source types)' if self.request['all'] else names(self.request['types'])
        self.say('Available source types: '+source_types)
        if not self.available_records:
            self.say('I understand the request, but no supporting records match these preferences in my local dataset.')
            return
        self.say('Available sources:')
        for index, r in enumerate(self.available_records, 1):
            labels = []
            if r['superseded'].lower() == 'true':
                labels.append('[outdated source]')
            if r['source_type'] == 'social_media' and self.request['purpose'] == 'report':
                labels.append('[not academically suitable for a report]')
            warning_label = ' ' + ' '.join(labels) if labels else ''
            self.say(f"{index}. {r['source']} | Updated: {r['updated']} | Type: {TYPES[r['source_type']]}{warning_label}")
        self.say('Choose a source number (or numbers separated by commas), or type all to preview every listed source.')

    def read_records(self, records):
        self.records = records
        self.state = 'feedback'
        for r in self.records:
            old = r['superseded'].lower() == 'true'
            warnings = ''
            if old:
                warnings += 'WARNING: Superseded record; may not describe the current dispute.\n'
            if r['source_type'] == 'social_media' and self.request['purpose'] == 'report':
                warnings += 'WARNING: TikTok is not an academically suitable source for a report.\n'
            divider = '----------------'
            reason = 'matches the topic and is included under the all-sources preference' if self.request['all'] else 'matches the topic and chosen source type'
            self.say(divider+'\nSIMULATED SOURCE: '+r['source']+'\nUpdated: '+r['updated']+'\nSource type: '+TYPES[r['source_type']]+'\n'+warnings+r['body']+'\nSelection reason: '+reason+('; includes a superseded record.' if old else '.')+'\n'+divider)
        if any(r['superseded'].lower()=='true' for r in self.records):
            self.say('I included the older record because you requested all available sources. Type exclude outdated to revise this.')
        self.say('Are the sources satisfactory? (yes / no / change sources)')
    def select(self, chosen, origin, all_sources=False):
        self.request['types'] = set(chosen)
        self.request['all'] = all_sources
        self.request['origin'] = origin
        self.selections.append(set(chosen))
        self.display()
    def handle(self, message):
        t = message.lower().strip()
        if not t: return True
        if t in ('exit','quit'):
            self.history.append(('You',message))
            self.say('Goodbye.'); return False
        if t=='reset':
            self.history.append(('You',message))
            self.reset(); self.say('Session cleared. What would you like to know?'); return True
        if t=='history':
            previous_history = self.history[:]
            self.history.append(('You',message))
            if not previous_history:
                print('No conversation history yet.')
                return True
            print('\n--- Session transcript ---')
            for role, text in self.history: print(f'{role}: {text}')
            return True
        self.history.append(('You',message))
        if t in ('help', '?'):
            self.say('Commands: help, context, history, requests, preferences, sources, use previous, why, exclude outdated, reset, exit.')
            return True
        if t=='context': self.context(); return True
        if t=='preferences':
            self.say('Previous selections: '+(' | '.join(names(s) for s in self.selections) or 'None')+'. Never applied automatically.'); return True
        if t=='requests':
            self.say('Previous requests: '+(' | '.join(r['original'] for r in self.requests) or 'None')); return True
        if t=='sources':
            if self.request and self.request['topic']!='Black Sabbath':
                self.state = 'clarify'
                self.options()
            else: self.say('Enter a supported request before choosing source options.')
            return True
        if t in ('change sources','no'):
            if self.request and self.request['topic']!='Black Sabbath' and (t!='no' or self.state=='feedback'): self.clarify()
            else: self.say('No active source selection to revise.')
            return True
        if t=='yes' and self.state=='feedback':
            self.state='accepted'; self.say('Thank you for confirming. You can ask another question or change sources.'); return True
        if t=='use previous':
            if self.state=='clarify' and self.selections: self.select(self.selections[-1],'user-confirmed historical preference')
            else: self.say('Previous preferences can be reused only during clarification when a previous selection exists.')
            return True
        if t=='exclude outdated':
            if self.request and self.state in ('select_record','feedback','accepted'):
                if self.request['all'] and not self.request['types']:
                    self.request['types'] = set(TYPES)
                self.request['all'] = False
                self.say('Outdated sources excluded. Here is the revised source list:')
                self.display()
            else:
                self.say('Request sources first, then use exclude outdated to remove superseded records from the list.')
            return True
        if t == 'all' and self.state == 'clarify' and self.request and self.request['topic'] != 'Black Sabbath':
            self.select(set(TYPES), 'user-confirmed all sources', all_sources=True)
            return True
        if t=='why' or (t.startswith('why') and re.search(r'old|cnn|2020|outdated|superseded|source|article',t)):
            if self.state not in ('feedback','accepted'): self.say('No completed source selection to explain.')
            else:
                if any(r['superseded'].lower()=='true' for r in self.records): self.say('You requested all available articles, so I included the superseded record and displayed its date.')
                self.say('Included: '+('; '.join(r['source']+' — topic and source type match' for r in self.records) or 'None')+'\nExcluded: '+('; '.join(r['source']+' — '+reason for r,reason in self.excluded) or 'None'))
            return True
        if self.state == 'select_record':
            if t == 'all':
                self.read_records(self.available_records[:])
                return True
            if re.fullmatch(r'\d+(?:[ ,]+\d+)*', t):
                indexes = [int(value) for value in re.findall(r'\d+', t)]
                if indexes and all(1 <= index <= len(self.available_records) for index in indexes):
                    selected = [self.available_records[index - 1] for index in dict.fromkeys(indexes)]
                    self.read_records(selected)
                else:
                    self.say(f'Choose a number from 1 to {len(self.available_records)}, or type all.')
                return True
        new = interpret(message)
        if new:
            self.request=new; self.requests.append(deepcopy(new)); self.records=[]; self.available_records=[]; self.excluded=[]
            if new['topic']=='Black Sabbath':
                self.state='unsupported'; self.say('I understand you are asking about Black Sabbath, but my local dataset contains no supporting information. I cannot provide a reliable answer.')
            elif not new['types'] and not new['all']: self.clarify()
            else: self.select(new['types'],'explicit',all_sources=new['all'])
            return True
        chosen = preferences(t)
        # Only accept a source-only reply, not arbitrary sentences containing a source word.
        source_reply = re.fullmatch(r'(?:[abc](?:[ ,]+[abc])*|(?:news(?: sources)?|academic(?: sources)?|social media|tiktok)(?:\s*(?:,|and|\+)\s*(?:news(?: sources)?|academic(?: sources)?|social media|tiktok))*)',t)
        if chosen and source_reply and self.request and self.request['topic']!='Black Sabbath':
            self.select(chosen,'user-confirmed'); return True
        self.say('I cannot understand that request within this simulation. Please rephrase or choose a supported source option.'); return True

def main():
    bot=BobBot()
    print('Bob Bot | Offline design simulation')
    bot.say('What would you like to know?')
    while True:
        try: message=input('You: ')
        except (EOFError,KeyboardInterrupt): print('\nBob Bot: Goodbye.'); break
        if not bot.handle(message): break

if __name__=='__main__': main()