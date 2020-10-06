import fileinput
import sys


# merge "symetric" hets (0/1+1/0 and vice versa) that match
# exactly (chr, pos, ref, alt). They must be consecutive so
# the VCF should be sorted.
# The variants are merged and the genotype is transformed to 1/1.
# If present, the merged GQ is the minimum of the two variants merged.


# line in the "buffer"
# either merge with the current line if exact het match
# or print and update with current line
line_prev = []
for line in fileinput.input():
    line = line.rstrip()
    # if header, print and skip
    if line[0] == '#':
        print(line)
        continue
    # if not, parse the VCF record
    line = line.split('\t')
    # test if chr, pos, ref, alt match
    if(len(line_prev) > 0 and
       line_prev[0] == line[0] and
       line_prev[1] == line[1] and
       line_prev[3].upper() == line[3].upper() and
       line_prev[4].upper() == line[4].upper()):
        # exact match chr+pos+ref+alt
        # extract FORMAT and genotypes
        ft_prev = line_prev[8].split(':')
        samp_prev = line_prev[9].split(':')
        gt_prev = samp_prev[ft_prev.index('GT')]
        ft = line[8].split(':')
        samp = line[9].split(':')
        gt = samp[ft.index('GT')]
        # check that both are hets
        if gt in ['0/1', '1/0'] and gt_prev in ['0/1', '1/0']:
            # change het to hom
            samp[ft.index('GT')] = '1/1'
            # update genotype quality
            if 'GQ' in ft:
                gq_prev = int(samp_prev[ft_prev.index('GQ')])
                gq = int(samp[ft.index('GQ')])
                samp[ft.index('GQ')] = str(min(gq, gq_prev))
            line[9] = ':'.join(samp)
            # print line and init line_prev
            print('\t'.join(line))
            line_prev = []
        else:
            sys.exit("Exact match but both are not hets!")
    elif len(line_prev) > 0:
        # different variants, print buffer
        # and update with current line
        print('\t'.join(line_prev))
        line_prev = line
    else:
        line_prev = line

# if the last variant wasn't merged, print it
if len(line_prev) > 0:
    print('\t'.join(line_prev))
