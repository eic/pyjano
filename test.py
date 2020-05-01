bufsize = 1000000

with open('pythia6_ep_10k_5x41GeV.lund') as infile:
    with open('pythia6_ep_10k_5x41GeV.stripped.lund', 'w') as outfile:
        while True:
            lines = infile.readlines(bufsize)
            if not lines:
                break
            for i, line in enumerate(lines):
                if i < 6:
                    continue
                if line[3] == '=':
                    continue
                outfile.write(line)

