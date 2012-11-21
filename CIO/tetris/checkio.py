from copy import copy, deepcopy
from optparse import OptionParser
import json
import os

GEN_STACK_SIZE = 200
parser = OptionParser(version='%prog 0.1')
parser.add_option('-n', '--name',dest='name', default = 'solution')
parser.add_option( '--out-gen',dest='out_gen', default = '')
parser.add_option('--in-gen',dest='in_gen', default = '')
(opts,argv) = parser.parse_args()

#python 3
solution = __import__(opts.name)
assert hasattr(solution,'checkio'), 'checkio function is not defined in your script'
player = solution.checkio

from checkio_org import referee, colouring

next_in = json.loads(open(os.path.join('data','initial.json')).read())

if opts.in_gen:
    import random
    random.seed(open(opts.in_gen,'r').read())
elif opts.out_gen:
    import uuid
    r_seed = uuid.uuid4().hex
    open(opts.out_gen,'w').write(r_seed)
    import random
    random.seed(r_seed)

next_in = deepcopy(referee.initial_checkio(next_in))
cur_tern = 0
while True:
    colouring.referee(next_in)
    next_in = deepcopy(player(next_in))
    colouring.player(next_in)
    try:
        next_in = deepcopy(referee.checkio(next_in))
    except (referee.DoneTest, referee.FailTest) as e:
        raise e
