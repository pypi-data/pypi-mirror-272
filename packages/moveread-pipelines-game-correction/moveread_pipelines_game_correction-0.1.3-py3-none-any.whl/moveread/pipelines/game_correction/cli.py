import os
from argparse import ArgumentParser

def main():
  parser = ArgumentParser()
  parser.add_argument('--images', required=True, type=str)
  parser.add_argument('-i', '--input', required=True, type=str)
  parser.add_argument('-o', '--output', required=True, type=str)
  parser.add_argument('--protocol', default='sqlite', required=False, choices=['sqlite', 'fs'], help='Protocol used in queues')

  parser.add_argument('-p', '--port', default=8000, type=int)
  parser.add_argument('--host', default='0.0.0.0', type=str)


  args = parser.parse_args()
  images = os.path.join(os.getcwd(), args.images)
  inp = os.path.join(os.getcwd(), args.input)
  out = os.path.join(os.getcwd(), args.output)
  proto = args.protocol
  
  print(f'Running API...')
  print(f'- Queues protocol: "{proto}"')
  print(f'- Input path: "{inp}"')
  print(f'- Output path: "{out}"')
  print(f'- Images path: "{images}"')
  os.makedirs(images, exist_ok=True)

  from typing import Any
  from q.kv import QueueKV
  from moveread.pipelines.game_correction import run_api, Input, Result
  Qin = QueueKV.at(tuple[Input, Any], inp, protocol=proto)
  Qout = QueueKV.at(tuple[Result, Any], out, protocol=proto)
  run_api(Qin, Qout, images_path=images, port=args.port, host=args.host)
  
if __name__ == '__main__':
  main()