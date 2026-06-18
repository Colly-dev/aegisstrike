import os

def create_inits(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if 'src' in dirpath or 'tests' in dirpath:
            init_path = os.path.join(dirpath, '__init__.py')
            if not os.path.exists(init_path):
                with open(init_path, 'w') as f:
                    f.write('"""Init file"""\n')

if __name__ == '__main__':
    create_inits('/home/ubuntu/aegisstrike')
