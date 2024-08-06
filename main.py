from subprocess import Popen, PIPE




comando = [
    'marker_single',
    './data/douglas_bersch_sample.pdf',
    'OUTPUT',
    '--max_pages', '1',
    '--batch_multiplier', '2',
    '--langs', 'Portuguese'
]

process = Popen(comando, stdout=PIPE, text=True)

while process.stdout.readable():
    line = process.stdout.readline()

    if not line:
        break

    print(line.strip())