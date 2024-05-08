from argparse import ArgumentParser

def main():
  parser = ArgumentParser()
  parser.add_argument('-i', '--input', required=True)
  parser.add_argument('-o', '--output', required=True)
  parser.add_argument('--images', required=True)
  parser.add_argument('--protocol', default='sqlite', required=False, choices=['sqlite', 'fs'], help='Protocol used in queues')

  args = parser.parse_args()


  import os
  input_path = os.path.join(os.getcwd(), args.input)
  output_path = os.path.join(os.getcwd(), args.output)
  images_path = os.path.join(os.getcwd(), args.images)
  proto = args.protocol
  
  print(f'Running preprocessing...')
  print(f'Images path: "{images_path}"')
  print(f'Queues protocol: "{proto}"')
  print(f'Input path: "{input_path}"')
  print(f'Output path: "{output_path}"')
  
  from typing import Any
  from q.kv import QueueKV
  from moveread.pipelines.input_validation import run_local, Input, Result

  Qin = QueueKV.at(tuple[Input, Any], input_path, protocol=proto)
  Qout = QueueKV.at(tuple[Result, Any], output_path, protocol=proto)
  run_local(Qin, Qout, images_path=images_path)

if __name__ == '__main__':
  import sys
  import os
  os.chdir('/home/m4rs/mr-github/rnd/data/moveread-pipelines/backend/input-validation/demo')
  sys.argv.extend('-i in -o out --images images/ --protocol sqlite'.split(' '))
  main()