from argparse import ArgumentParser

def main():
  parser = ArgumentParser()
  parser.add_argument('-i', '--input', required=True)
  parser.add_argument('-o', '--output', required=True)
  parser.add_argument('-b', '--base-path', required=True)
  parser.add_argument('--images', required=True)
  parser.add_argument('--protocol', default='sqlite', required=False, choices=['sqlite', 'fs'], help='Protocol used in queues')

  args = parser.parse_args()


  import os
  input_path = os.path.join(os.getcwd(), args.input)
  output_path = os.path.join(os.getcwd(), args.output)
  base_path = os.path.join(os.getcwd(), args.base_path)
  images_path = os.path.join(os.getcwd(), args.images)
  proto = args.protocol
  
  print(f'Running preprocessing...')
  print(f'Images path: "{images_path}"')
  print(f'Queues protocol: "{proto}"')
  print(f'Input path: "{input_path}"')
  print(f'Internal path: "{base_path}"')
  print(f'Output path: "{output_path}"')
  
  from kv.fs import FilesystemKV
  from moveread.pipelines.local_dfy import run_local, input_queue, output_queue

  Qin = input_queue(input_path, protocol=proto)
  Qout = output_queue(output_path, protocol=proto)
  images = FilesystemKV[bytes](images_path)
  run_local(Qin, Qout, base_path=base_path, images=images, images_path=images_path)

if __name__ == '__main__':
  import sys
  import os
  os.chdir('/home/m4rs/mr-github/rnd/data/moveread-pipelines/backend/local-dfy/demo')
  sys.argv.extend('-i in -o out -b internal/ --images images/ --protocol sqlite'.split(' '))
  main()