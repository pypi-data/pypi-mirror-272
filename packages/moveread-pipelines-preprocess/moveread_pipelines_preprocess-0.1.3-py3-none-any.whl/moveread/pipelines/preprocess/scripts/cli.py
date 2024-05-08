from argparse import ArgumentParser

def main():
  parser = ArgumentParser()
  parser.add_argument('-i', '--input', required=True)
  parser.add_argument('-o', '--output', required=True)
  parser.add_argument('-q', '--queues', required=True)
  parser.add_argument('--images', required=True)
  parser.add_argument('--protocol', default='sqlite', required=False, choices=['sqlite', 'fs'], help='Protocol used in queues')

  parser.add_argument('-p', '--port', default=8000, type=int)
  parser.add_argument('--host', default='0.0.0.0', type=str)

  args = parser.parse_args()


  import os
  input_path = os.path.join(os.getcwd(), args.input)
  output_path = os.path.join(os.getcwd(), args.output)
  queues_path = os.path.join(os.getcwd(), args.queues)
  images_path = os.path.join(os.getcwd(), args.images)
  proto = args.protocol
  
  print(f'Running preprocessing...')
  print(f'Images path: "{images_path}"')
  print(f'Queues protocol: "{proto}"')
  print(f'Input path: "{input_path}"')
  print(f'Internal queues path: "{queues_path}"')
  print(f'Output path: "{output_path}"')
  
  from kv.fs import FilesystemKV
  from moveread.pipelines.preprocess import run, input_queue, output_queue, queues

  Qin = input_queue(input_path, protocol=proto)
  Qout = output_queue(output_path, protocol=proto)
  Qs = queues(queues_path, protocol=proto)
  images = FilesystemKV[bytes](images_path)
  run(Qin, Qout, Qs, images=images, images_path=images_path)

if __name__ == '__main__':
  import sys
  import os
  os.chdir('/home/m4rs/mr-github/rnd/data/moveread-pipelines/backend/preprocess/demo')
  sys.argv.extend('-i input -o output -q queues/ --images images/ --protocol sqlite'.split(' '))
  main()