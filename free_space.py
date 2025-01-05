with open('StorableSidebar.json') as f:
     d = json.load(f)
     for space in d['sidebar']['containers'][1]['spaces']:
         if type(space) == dict:
             print(space['id'], space['title'])
             for item in d['sidebar']['containers'][1]['items']:
                 if type(item) == dict:
                     pprint(item)
                     print('\n%%\n')
             print("\n\n_____\n\n")