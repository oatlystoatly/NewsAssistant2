"""Bob Bot: offline rule-based interaction prototype, not an LLM."""
from pathlib import Path
import re
from copy import deepcopy
from datetime import date, timedelta

RECENT_DAYS = 30

SOURCE_DIR = Path(__file__).parent / 'sources'
TYPES = {'news': 'News', 'academic': 'Academic', 'social_media': 'Social media'}

def load_sources():
    records = []
    for path in sorted(SOURCE_DIR.glob('*.md')):
        try:
            _, header, body = path.read_text(encoding='utf-8-sig').split('---', 2)
            meta = dict(line.split(':', 1) for line in header.splitlines() if ':' in line)
            meta = {k.strip(): v.strip() for k, v in meta.items()}
            category = meta.get('source_type', '').casefold()
            if category == 'tiktok':
                category = 'social_media'
            if not {'source','section','updated','source_type','superseded'} <= meta.keys():
                raise ValueError('missing metadata')
            if category not in TYPES or meta['superseded'].lower() not in ('true','false'):
                raise ValueError('invalid source type or superseded flag')
            date.fromisoformat(meta['updated'])
            records.append({**meta, 'category': category, 'body': body.strip()})
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

def academic_purpose(text):
    return bool(re.search(r'\b(report|assignment|essay|dissertation|coursework|thesis|academic research|university project|literature review|research paper)\b', text.lower()))


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
    source_text = re.sub(r'\bacademic research\b', '', t)
    types = set() if uncertain else preferences(source_text)
    if all_sources and not types and re.search(r'\ball\b.*\bsources?\b', t):
        types = set(TYPES)
    if re.search(r'\b(recent|latest|current)\s+(?:news|articles?|sources?|reports?|academic|social media|tiktok)\b', t) or re.search(r'\b(recent|latest)\b', t):
        recency = 'recent'
    elif re.search(r'\b(historical|older|outdated)\b', t):
        recency = 'historical'
    elif all_sources:
        recency = None
    elif re.search(r'\b(current|updates)\b', t):
        recency = 'recent (inferred from updates)' if 'updates' in t else 'recent'
    else:
        recency = None
    return dict(topic=topic, location='Selly Oak' if topic.startswith('Selly') else ('Birmingham' if 'birmingham' in t else None), purpose='report' if academic_purpose(t) else None, types=types, all=all_sources, recency=recency, origin='explicit' if types else 'missing', original=text, uncertain=uncertain)

def retrieve(request):
    matching, excluded = [], []
    for r in load_sources():
        if r['section'].casefold() != request['topic'].casefold():
            reason = 'Different topic'
        elif r['category'] not in request['types']:
            reason = 'Source type not selected'
        elif (request['recency'] or '').startswith('recent') and (
            r['superseded'].lower() == 'true' or not date.today() - timedelta(days=RECENT_DAYS) <= date.fromisoformat(r['updated']) <= date.today()
        ):
            reason = 'Superseded or outside the recent date range'
        elif request['recency'] == 'historical' and r['superseded'].lower() != 'true' and date.fromisoformat(r['updated']) >= date.today() - timedelta(days=RECENT_DAYS):
            reason = 'Not historical'
        elif r['superseded'].lower() == 'true' and not request['all'] and request['recency'] != 'historical':
            reason = 'Superseded; current-only filter'
        else:
            matching.append(r); continue
        excluded.append((r,reason))
    type_order = {kind: index for index, kind in enumerate(TYPES)}
    matching.sort(key=lambda r: (type_order[r['category']], r['source'].casefold()))
    return matching, excluded

class BobBot:
    def __init__(self):
        self.reset()
    def reset(self):
        self.request = None
        self.history = []
        self.selections = []
        self.selection_contexts = []
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
        if self.request['uncertain']:
            self.say('Your source instructions contain a negation or exclusion that I cannot reliably interpret. Please confirm the desired categories.')
        if self.selections:
            self.say('Previous selection: '+names(self.selections[-1])+' (from: '+self.selection_contexts[-1]+'). Type "use previous" to explicitly reuse it, or choose new sources.')
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
        if r['all']: explicit.append('Include all records matching selected categories and recency')
        elif not r['recency']: inferred.append('Default filter: exclude superseded records')
        self.say('Current request\nExplicit / user-confirmed: '+ '; '.join(explicit)+'\nInferred / default: '+('; '.join(inferred) or 'None')+'\nMissing: '+('; '.join(missing) or 'None')+'\nState: '+self.state+'\nMissing purpose alone does not prevent retrieval.')
    def display(self):
        self.available_records,self.excluded = retrieve(self.request)
        self.records = []
        self.state = 'select_record'
        self.requests[-1]['latest'] = deepcopy(self.request)
        source_types = names(self.request['types'])
        self.say('Available source types: '+source_types)
        if (self.request['recency'] or '').startswith('recent'):
            self.say(f'Recency filter: last {RECENT_DAYS} days, excluding superseded records.')
        if not self.available_records:
            self.state = 'no_results'
            self.say('I understand the request, but no supporting records match these preferences in my local dataset.')
            return
        self.say('Available sources:')
        for index, r in enumerate(self.available_records, 1):
            labels = []
            if r['superseded'].lower() == 'true':
                labels.append('[outdated source]')
            if r['category'] == 'social_media' and self.request['purpose'] == 'report':
                labels.append('[academic warning: social media; verify claims]')
            warning_label = ' ' + ' '.join(labels) if labels else ''
            source_label = 'TikTok' if r['source_type'].casefold() == 'tiktok' else TYPES[r['category']]
            self.say(f"{index}. {r['source']} | Updated: {r['updated']} | Type: {source_label}{warning_label}")
        self.say('Choose a source number (or numbers separated by commas), or type "all" to preview every listed source.')

    def read_records(self, records):
        self.records = records
        self.state = 'feedback'
        for r in self.records:
            old = r['superseded'].lower() == 'true'
            warnings = ''
            if old:
                warnings += 'WARNING: Superseded record; may not describe the current dispute.\n'
            if r['category'] == 'social_media' and self.request['purpose'] == 'report':
                warnings += 'WARNING: This is a social media source, not a peer-reviewed academic publication. Verify its claims before using it in academic work.\n'
            divider = '----------------'
            reason = 'matches the topic and selected category; all matching records requested' if self.request['all'] else 'matches the topic and chosen source type'
            self.say(divider+'\nSIMULATED SOURCE: '+r['source']+'\nUpdated: '+r['updated']+'\nSource type: '+('TikTok' if r['source_type'].casefold() == 'tiktok' else TYPES[r['category']])+'\n'+warnings+r['body']+'\nSelection reason: '+reason+('; includes a superseded record.' if old else '.')+'\n'+divider)
        if any(r['superseded'].lower()=='true' for r in self.records):
            self.say('I included the older record because you requested all available sources. Type "exclude outdated" to revise this.')
        self.say('Are the sources satisfactory? (yes / no / change sources)')
    def select(self, chosen, origin, all_sources=False):
        self.request['types'] = set(chosen)
        self.request['all'] = all_sources
        self.request['origin'] = origin
        self.request['uncertain'] = False
        self.selections.append(set(chosen))
        self.selection_contexts.append(self.request['original'])
        self.display()
    def handle(self, message):
        t = message.lower().strip()
        if not t: return True
        greeting = re.fullmatch(
            r'(?:hi|hello|hey|good morning|good afternoon|good evening|how are you)'
            r'(?: bob bot)?[!.?, ]*',
            t,
        )
        if greeting:
            self.history.append(('You', message))
            if t.startswith('how are you'):
                self.say("I'm ready to help. What would you like to know?")
            else:
                self.say('Hello! How can I help you today?')
            return True
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
                self.say('No earlier conversation history.')
                return True
            transcript = '\n'.join(f'{role}: {text}' for role, text in self.history)
            self.say('Session transcript:\n' + transcript)
            return True
        self.history.append(('You',message))
        if t in ('help', '?'):
            self.say('Commands: help, context, history, requests, preferences, sources, use previous, why, exclude outdated, reset, exit.')
            return True
        if t=='context': self.context(); return True
        if t=='preferences':
            self.say('Previous selections: '+(' | '.join(names(s) for s in self.selections) or 'None')+'. Never applied automatically.'); return True
        if t=='requests':
            self.say('Previous requests: '+(' | '.join(r['original']+' — initial: '+names(r['types'])+'; latest: '+names(r.get('latest',r)['types']) for r in self.requests) or 'None')); return True
        if t=='sources':
            if self.request and self.request['topic']!='Black Sabbath':
                self.state = 'clarify'
                self.options()
            else: self.options(); self.say('Enter a supported request to apply these options.')
            return True
        if t in ('change sources','no'):
            if self.request and self.request['topic']!='Black Sabbath' and (t!='no' or self.state=='feedback'): self.clarify()
            else: self.say('No active source selection to revise.')
            return True
        if t=='yes' and self.state=='feedback':
            self.state='accepted'; self.say('Thank you for confirming. You can ask another question or change sources.'); return True
        if t=='use previous':
            if self.state=='clarify' and self.selections: self.select(self.selections[-1],'user-confirmed historical preference', self.request['all'])
            else: self.say('Previous preferences can be reused only during clarification when a previous selection exists.')
            return True
        if t=='exclude outdated':
            if self.request and self.state in ('select_record','feedback','accepted'):
                if self.request['all'] and not self.request['types']:
                    self.request['types'] = set(TYPES)
                self.request['all'] = False
                self.request['recency'] = 'recent'
                self.say('Outdated sources excluded. Here is the revised source list:')
                self.display()
            else:
                self.say('Request sources first, then use exclude outdated to remove superseded records from the list.')
            return True
        if t == 'all' and self.state == 'clarify' and self.request and self.request['topic'] != 'Black Sabbath':
            self.select(set(TYPES), 'user-confirmed all sources', all_sources=True)
            return True
        if t=='why' or (t.startswith('why') and re.search(r'old|cnn|2020|outdated|superseded|source|article',t)):
            if self.state not in ('select_record','feedback','accepted','no_results'): self.say('No completed source selection to explain.')
            else:
                if any(r['superseded'].lower()=='true' for r in self.records): self.say('You requested all available articles, so I included the superseded record and displayed its date.')
                self.say('Available but not opened: '+('; '.join(r['source'] for r in self.available_records if r not in self.records) or 'None'))
                self.say('Opened: '+('; '.join(r['source']+' — topic and source type match' for r in self.records) or 'None')+'\nExcluded: '+('; '.join(r['source']+' — '+reason for r,reason in self.excluded) or 'None'))
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
                    self.say(f'Choose a number from 1 to {len(self.available_records)}, or type "all".')
                return True
        new = interpret(message)
        # Recognised follow-ups update the active request rather than replacing it.
        if new is None and self.request and self.request['topic'] != 'Black Sabbath' and (
            re.fullmatch(r'(?:show|give me|find|only|just|i want|what about|now)\s+(?:(?:me|the|all|only|just|recent|current|latest|historical|older|outdated|news|academic|social media|tiktok|articles?|sources?|please|and)\s*)+[.!?]?', t)
            or re.fullmatch(r'(?:all |only )?(?:recent|current|latest|historical|older|outdated)(?: (?:news|articles|sources))?', t)
        ):
            update = interpret(message + ' ' + self.request['topic'])
            if update:
                new = deepcopy(self.request)
                if update['types'] or update['uncertain']:
                    new['types'] = update['types']
                    new['origin'] = update['origin']
                if update['recency'] or update['all']:
                    new['recency'] = update['recency']
                if update['all']:
                    new['all'] = True
                new['uncertain'] = update['uncertain']
                self.request = new
                self.say('Using the topic and purpose from your current request.')
                if not new['types']:
                    self.clarify()
                else:
                    self.select(new['types'], new['origin'], new['all'])
                return True
        if new:
            self.request=new; self.requests.append(deepcopy(new)); self.records=[]; self.available_records=[]; self.excluded=[]
            if new['topic']=='Black Sabbath':
                self.state='unsupported'; self.say('I understand you are asking about Black Sabbath, but my local dataset contains no supporting information. I cannot provide a reliable answer.')
            elif not new['types']: self.clarify()
            else: self.select(new['types'],'explicit',all_sources=new['all'])
            return True
        chosen = preferences(t)
        # Only accept a source-only reply, not arbitrary sentences containing a source word.
        source_reply = re.fullmatch(r'(?:[abc](?:[ ,]+[abc])*|(?:news(?: sources)?|academic(?: sources)?|social media|tiktok)(?:\s*(?:,|and|\+)\s*(?:news(?: sources)?|academic(?: sources)?|social media|tiktok))*)',t)
        if chosen and source_reply and self.request and self.request['topic']!='Black Sabbath':
            self.select(chosen,'user-confirmed', self.request['all']); return True
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