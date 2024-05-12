from scoresheet_models import MODEL_IDS
from argparse import ArgumentParser

def main():
  parser = ArgumentParser()
  parser.add_argument('-i', '--input', required=True)
  parser.add_argument('-o', '--output', required=True)
  parser.add_argument('-b', '--base-path', required=True)
  parser.add_argument('-d', '--database', required=True, help='Database URL')
  parser.add_argument('-t', '--tournament', required=True, help='Tournament ID')
  parser.add_argument('-m', '--model', required=True, choices=MODEL_IDS, help='Model ID')
  parser.add_argument('--images', required=True)
  parser.add_argument('--protocol', default='sqlite', required=False, choices=['sqlite', 'fs'], help='Protocol used in queues')

  args = parser.parse_args()


  import os
  from dslog import Logger
  input_path = os.path.join(os.getcwd(), args.input)
  output_path = os.path.join(os.getcwd(), args.output)
  base_path = os.path.join(os.getcwd(), args.base_path)
  images_path = os.path.join(os.getcwd(), args.images)
  proto = args.protocol
  db_url = args.database
  tournId = args.tournament
  
  logger = Logger.click().prefix('[DFY]')
  logger(f'Running...')
  logger(f'- Tournament ID: "{tournId}"')
  logger(f'- Database URL: "{db_url}"')
  logger(f'- Images path: "{images_path}"')
  logger(f'- Queues protocol: "{proto}"')
  logger(f'- Input path: "{input_path}"')
  logger(f'- Internal path: "{base_path}"')
  logger(f'- Output path: "{output_path}"')
  
  from kv.fs import FilesystemKV
  from sqlmodel import create_engine
  from moveread.dfy import run_connect
  from moveread.pipelines.dfy import run_local, input_queue, output_queue
  from multiprocessing import Process

  Qin = input_queue(input_path, protocol=proto)
  Qout = output_queue(output_path, protocol=proto)
  engine = create_engine(db_url)
  images = FilesystemKV[bytes](images_path)
  ps = (
    Process(target=run_connect, args=(Qin, Qout), kwargs=dict(engine=engine, tournId=tournId, logger=logger.prefix('[I/O]'), model=args.model)),
    Process(target=run_local, args=(Qin, Qout), kwargs=dict(base_path=base_path, images=images, images_path=images_path, logger=logger)),
  )
  for p in ps:
    p.start()
  for p in ps:
    p.join()

if __name__ == '__main__':
  import sys
  import os
  os.chdir('/home/m4rs/mr-github/modes/dfy/moveread-dfy/')
  sys.argv.extend('-b test/internal -i test/in -o test/out -d sqlite:///db.sqlite -t llobregat -m llobregat23 --images test/images'.split(' '))
  main()